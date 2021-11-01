import datetime
import threading

import jsonpickle

import websocket

from .algorum_types import *
from .concurrent_collections import *
from .remote_indicator_evaluator import *


class QuantEngineClient:
    MultiplyFactor = ((60 * 24) / 405)

    def __init__(self, url, apikey, launchmode, sid):
        self.Url = url
        self.ApiKey = apikey
        self.LaunchMode = launchmode
        self.StrategyId = sid
        self.MessageHandlerMap = {}
        self.CorIdMessageMap = {}
        self.ws = None
        self.CorIdCounter = FastReadCounter()
        self.TickQueue = BoundedBlockingQueue(1000000)
        self.stop_event = threading.Event()
        self.open_event = threading.Event()
        self.BacktestStartDate: datetime = datetime.utcnow()
        self.BacktestEndDate: datetime = datetime.utcnow()
        self.Evaluator = None
        self.LastProcessedTick = None
        self.ProgressPercent: float = 0.0
        self.Thread1 = None
        self.Thread2 = None

        self.add_message_handler("tick", self.tick_handler)
        self.add_message_handler("order_update", self.order_update_handler)
        self.add_message_handler("stop", self.stop_handler)

        self.Evaluator: RemoteIndicatorEvaluator

        self.initialize()

    def execute_async(self,
                      algorum_websocket_message: AlgorumWebsocketMessage) -> \
            AlgorumWebsocketMessage:
        async_waiter = AsyncWaiter()
        self.CorIdMessageMap[algorum_websocket_message.CorId] = async_waiter
        self.ws.send(jsonpickle.encode(algorum_websocket_message, False))
        async_waiter.WaiterEvent.wait()
        return async_waiter.Message

    def send_async(self, algorum_websocket_message: AlgorumWebsocketMessage):
        self.ws.send(jsonpickle.encode(algorum_websocket_message, False))

    def publish_stats(self, stats):
        self.send_async(AlgorumWebsocketMessage(
            "publish_stats",
            AlgorumMessageType.Oneway,
            self.CorIdCounter.increment(),
            jsonpickle.encode(stats, False),
            None
        ))

    def add_message_handler(self, name, handler):
        self.MessageHandlerMap[name] = handler

    def tick_handler(self, algorum_websocket_message):
        tick_data = jsonpickle.decode(algorum_websocket_message.JsonData)
        tick_data_obj = TickData(**tick_data)
        tick_data_obj.AlgorumMessage = algorum_websocket_message
        self.TickQueue.enqueue(tick_data_obj)

    def order_update_handler(self, algorum_websocket_message):
        order_dict = jsonpickle.decode(algorum_websocket_message.JsonData)
        order = Order(**order_dict)
        self.on_order_update(order)

        algorum_websocket_message.MessageType = AlgorumMessageType.Response
        algorum_websocket_message.JsonData = ""
        self.ws.send(jsonpickle.encode(algorum_websocket_message))

    def stop_handler(self, algorum_websocket_message):
        algorum_websocket_message.MessageType = AlgorumMessageType.Response
        algorum_websocket_message.JsonData = ""
        self.ws.send(jsonpickle.encode(algorum_websocket_message))
        self.stop_event.set()

    def wait(self):
        self.stop_event.wait()

    def subscribe_symbols(self, symbols):
        sub_symbols_request = \
            AlgorumWebsocketMessage('sub_symbols',
                                    AlgorumMessageType.Request,
                                    self.CorIdCounter.increment(),
                                    jsonpickle.encode(symbols, False), None)
        # print(sub_symbols_request)
        response = self.execute_async(sub_symbols_request)

        if response.MessageType == AlgorumMessageType.ErrorResponse:
            raise Exception(response.Error['ErrorMessage'])
        # print(response)

    def log(self, log_level: str, message: str):
        request = AlgorumWebsocketMessage('log',
                                          AlgorumMessageType.Oneway,
                                          self.CorIdCounter.increment(),
                                          jsonpickle.encode({
                                              'LogLevel': log_level,
                                              'Message': message
                                          }, False), None)
        self.send_async(request)

    def backtest(self, backtest_request: BacktestRequest):
        self.BacktestStartDate = backtest_request.StartDate
        self.BacktestEndDate = backtest_request.EndDate

        msg_request = \
            AlgorumWebsocketMessage('backtest',
                                    AlgorumMessageType.Request,
                                    self.CorIdCounter.increment(),
                                    jsonpickle.encode(backtest_request, False), None)
        # print(msg_request)
        response = self.execute_async(msg_request)

        if response.MessageType == AlgorumMessageType.ErrorResponse:
            raise Exception(response.Error['ErrorMessage'])

        # print(response)

    def start_trading(self, trading_request: TradingRequest):
        msg_request = \
            AlgorumWebsocketMessage('start_trading',
                                    AlgorumMessageType.Request,
                                    self.CorIdCounter.increment(),
                                    jsonpickle.encode(trading_request, False), None)
        # print(msg_request)
        response = self.execute_async(msg_request)

        if response.MessageType == AlgorumMessageType.ErrorResponse:
            raise Exception(response.Error['ErrorMessage'])

    def place_order(self, place_order_request: PlaceOrderRequest):
        request = AlgorumWebsocketMessage('place_order',
                                          AlgorumMessageType.Request,
                                          self.CorIdCounter.increment(),
                                          jsonpickle.encode(place_order_request, False), None)
        # print(request)
        response = self.execute_async(request)

        if response.MessageType == AlgorumMessageType.ErrorResponse:
            raise Exception(response.Error['ErrorMessage'])

        # print(response)
        order_id = jsonpickle.decode(response.JsonData)
        # print(order_id)
        return order_id

    def create_indicator_evaluator(self, create_indicator_request: CreateIndicatorRequest) \
            -> RemoteIndicatorEvaluator:
        request = AlgorumWebsocketMessage('create_indicator_evaluator',
                                          AlgorumMessageType.Request,
                                          self.CorIdCounter.increment(),
                                          jsonpickle.encode(create_indicator_request, False), None)
        # print(request)
        response = self.execute_async(request)

        if response.MessageType == AlgorumMessageType.ErrorResponse:
            raise Exception(response.Error['ErrorMessage'])

        # print(response)

        uid = jsonpickle.decode(response.JsonData)
        # print(uid)

        self.Evaluator = RemoteIndicatorEvaluator(
            self,
            create_indicator_request.Symbol, uid)
        return self.Evaluator

    def get_stats(self, tick_data: TickData):
        raise NotImplementedError(self)

    def send_progress_async(self, tick_data: TickData):
        t_seconds = (self.BacktestEndDate - self.BacktestStartDate).total_seconds() * (70 / 100)
        processed_seconds = (datetime.strptime(tick_data.Timestamp, "%Y-%m-%dT%H:%M:%SZ") -
                             datetime.strptime(self.LastProcessedTick.Timestamp,
                                               "%Y-%m-%dT%H:%M:%SZ")).total_seconds() * QuantEngineClient.MultiplyFactor

        progress_percent = (processed_seconds / t_seconds) * 100

        if (self.ProgressPercent + progress_percent >= 100) and not tick_data.LastTick:
            progress_percent = 0
        else:
            if tick_data.LastTick:
                self.ProgressPercent = 100

        if progress_percent >= 1 or tick_data.LastTick:
            if not tick_data.LastTick:
                self.ProgressPercent += progress_percent

            self.send_async(AlgorumWebsocketMessage(
                'publish_progress',
                AlgorumMessageType.Oneway,
                self.CorIdCounter.increment(),
                jsonpickle.encode(self.ProgressPercent, False), None))

            stats = self.get_stats(tick_data)
            self.publish_stats(stats)

            print('>>>>>>>>> Progress: ' + str(self.ProgressPercent))

            for k, v in stats.items():
                print('Key: ' + str(k) + ', Value: ' + str(v))

            self.LastProcessedTick = tick_data

        if self.ProgressPercent >= 100:
            self.log(LogLevel.Information, "100% Progress")
            self.stop_event.set()
            self.ws.close()

    def run(self):
        self.ws.run_forever()

    def on_tick(self, tick_data: TickData):
        raise NotImplementedError(self)

    def on_order_update(self, order: Order):
        raise NotImplementedError(self)

    def process_tick(self):

        while 1:
            tick_data = self.TickQueue.dequeue()
            algorum_websocket_message = tick_data.AlgorumMessage
            tick_data.AlgorumMessage = None

            if tick_data is not None:
                last_processed_tick: TickData = self.LastProcessedTick

                if (self.LastProcessedTick is None) or \
                        (datetime.strptime(last_processed_tick.Timestamp, "%Y-%m-%dT%H:%M:%SZ").day !=
                         datetime.strptime(tick_data.Timestamp, "%Y-%m-%dT%H:%M:%SZ").day):
                    self.LastProcessedTick = tick_data

                self.on_tick(tick_data)

                algorum_websocket_message.MessageType = AlgorumMessageType.Response
                algorum_websocket_message.JsonData = ""
                self.ws.send(jsonpickle.encode(algorum_websocket_message))
            else:
                break

    def initialize(self):
        def on_message(ws, message):
            # diagnostic message
            # print(message)

            msg_dict = jsonpickle.decode(message)
            msg = AlgorumWebsocketMessage(**msg_dict)

            if msg.Name in self.MessageHandlerMap:
                handler = self.MessageHandlerMap[msg.Name]
            else:
                handler = None

            if handler is None:
                if msg.MessageType == AlgorumMessageType.Request:
                    msg.MessageType = AlgorumMessageType.Response
                    msg.JsonData = ""
                    self.ws.send(jsonpickle.encode(msg))
                else:
                    if msg.MessageType == AlgorumMessageType.Response or \
                            msg.MessageType == AlgorumMessageType.ErrorResponse:
                        if msg.CorId in self.CorIdMessageMap:
                            async_waiter = self.CorIdMessageMap[msg.CorId]
                            async_waiter.Message = msg
                            del self.CorIdMessageMap[msg.CorId]
                            async_waiter.WaiterEvent.set()
            else:
                handler(msg)

        def on_error(ws, error):
            print(error)

        def on_close(ws):
            print('websockets closed')
            self.stop_event.set()

        def on_open(ws):
            print('open')
            self.open_event.set()

        websocket.enableTrace(False)
        self.ws = websocket.WebSocketApp(self.Url,
                                         on_message=on_message,
                                         on_error=on_error,
                                         on_close=on_close)
        self.ws.on_open = on_open

        self.Thread1 = threading.Thread(target=self.run, daemon=True)
        self.Thread1.start()
        self.Thread2 = threading.Thread(target=self.process_tick, daemon=True)
        self.Thread2.start()

        self.open_event.wait()
