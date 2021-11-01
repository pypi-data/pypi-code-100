#!/usr/bin/python3

import json
import os
import sys
import threading
import time
from datetime import datetime

import websocket
from log import *
from utils import *

# from loguru import logger

URL_WS = {}
URL_WS["spot"] = "wss://stream.bybit.com/spot/quote/ws/v1"
URL_WS["coin"] = "wss://stream.bytick.com/realtime"
URL_WS["usd"] = "wss://stream.bybit.com/realtime_public"
URL_WS["futures"] = "wss://stream.bybit.com/realtime"
URL_WS["trade"] = "wss://stream.bybit.com/spot/quote/ws/v1"

logger.remove(handler_id=None)

class piBybitMD:
    def __init__(self, url, symbol):
        self.url = url
        self.symbol = symbol
        self.bclose = False
        print("bybit:",url,symbol)

    def on_message(self, message):
        # buf = gzip.decompress(message).decode()
        buf = message

        if buf[2:6] == "ping":
            key = json.loads(buf)["ping"]
            pong = {}
            pong["pong"] = key
            self.ws.send(json.dumps(pong))
        # else:
            # logger.info(buf)

    def on_error(self):
        os._exit(1)

    def on_close(self):
        os._exit(1)

    def on_open(self):
        if self.url == URL_WS["spot"]:
            tradeStr=f"""{{"symbol":"{self.symbol}","topic":"depth","event":"sub","params":{{"binary":false}}}}"""
        elif self.url == URL_WS["coin"]:
            tradeStr=f"""{{ "op":"subscribe", "args": ["orderBook_200.100ms.{self.symbol}"] }}"""
        elif self.url == URL_WS["futures"]:
            tradeStr=f"""{{ "op":"subscribe", "args": ["orderBook_200.100ms.{self.symbol}"] }}"""
        elif self.url == URL_WS["usd"]:
            tradeStr=f"""{{ "op":"subscribe", "args": ["orderBook_200.100ms.{self.symbol}"] }}"""
        else:
            pass
        self.ws.send(tradeStr)
 
    def initiate(self):
        print("initiate")
        #websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(self.url,
                              on_message = self.on_message,
                              on_error = self.on_error,
                              on_close = self.on_close,
                              on_open = self.on_open)
        return self.ws

class piBybitTrade:
    def __init__(self, url, symbol):
        self.url = url
        self.symbol = symbol
        self.bclose = False
        print("bybit:",url,symbol)

    def on_message(self, message):
        # buf = gzip.decompress(message).decode()
        buf = message

        if buf[2:6] == "ping":
            key = json.loads(buf)["ping"]
            pong = {}
            pong["pong"] = key
            self.ws.send(json.dumps(pong))

    def on_error(self):
        os._exit(1)

    def on_close(self):
        os._exit(1)

    def on_open(self):
        tradeStr=f"""{{"symbol":"{self.symbol}","topic":"trade","event":"sub","params":{{"binary":false}}}}"""
        self.ws.send(tradeStr)
 
    def initiate(self):
        print("initiate")
        #websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(self.url,
                              on_message = self.on_message,
                              on_error = self.on_error,
                              on_close = self.on_close,
                              on_open = self.on_open)
        return self.ws

class piBybitKlineUsd():
    def __init__(self):
        ERROR("Bybit connected")
        self.symbols = ["BTCUSDT", "ETHUSDT"]
        self.wss = "wss://stream.bybit.com/realtime_public"
        self.turnover24h = {}
        self.volume24h = {}
        self.settle_currency = {}
        self.markpx = {}
        self.lastpx = {}
        self.update = dict(zip(self.symbols, [datetime.now() for _ in self.symbols]))

    def init(self):
        try:
            self.get_settlecurrency()

            self._err = False
            # url = self.wss + "/stream?streams="
            url = self.wss

            # for symbol in self.symbols:
            #     s = symbol.upper()
            #     url = url + f"{s.lower()}@ticker/{s.lower()}@kline_5m/"

            # url = url[:-1]
            INFO(f"Bybit USDT wss--> {url}")
            self.ws = websocket.WebSocketApp( url,
                                        on_message = self.on_message,
                                        on_error = self.on_error,
                                        on_close = self.on_close,
                                        on_open = self.on_open) 
            self.wst = threading.Thread(target=lambda: self.ws.run_forever())
            self.wst.daemon = True
            self.wst.start()

            conn_timeout = 5

            while ((not self.ws.sock or not self.ws.sock.connected) and conn_timeout and not self._err):
                time.sleep(1)
                conn_timeout -= 1

            if not conn_timeout or self._err:
                ERROR(f"Bybit USDT can not connect wss")
            
        except:
            ERROR(traceback.format_exc())
    
    def get_settlecurrency(self):
        url = f"""https://api.bybit.com/v2/public/symbols"""
        r = requests.get(url)
        if r.ok:
            a = json.loads(r.text)
            for s in a['result']:
                symbol = s['name']
                if symbol not in self.symbols:
                    continue
                # self.settle_currency[symbol] = s['quote_currency']
                self.settle_currency[symbol] = "BTC"
                INFO(f"{symbol}: {self.settle_currency[symbol]}")
        else:
            ERROR(f"Bybit USDT Https Error {r.text}")

    def on_klines(self,msg, symbol):
        try:
            # if msg['k']["x"] == False:
            #     return
            exchange = "Bybit"
            ac = 'usd'
            check_a = self.update[symbol]
            if datetime.now() - check_a < timedelta(minutes=4):
                return
            # symbol = msg['s']
            t = GetFmtTm()
            while symbol not in self.turnover24h:
                time.sleep(0.1)
            while symbol not in self.settle_currency:
                time.sleep(0.1)
            while symbol not in self.markpx:
                time.sleep(0.1)
            turnover24h = float(self.turnover24h[symbol])
            volume24h = float(self.volume24h[symbol])
            settle_currency = self.settle_currency[symbol]
            markpx = float(self.markpx.get(symbol, 0))
            lastpx = None #现货先空着吧
            # k = msg["k"]
            k = msg
            _open = float(k['open'])
            close = float(k['close'])
            high = float(k['high'])
            low = float(k['low'])
            volume = float(k['volume'])
            timestamp = GetFmtTmFromBybit(int(k['timestamp']/10**3))
            
            log = {}
            log['exchange'] = exchange
            log['ac'] = ac
            log['symbol'] = symbol
            log['t'] = GetFmtTm()
            log['turnover24h'] = turnover24h
            log['volume24h'] = volume24h
            log['settle_currency'] = "USDT"
            log['open'] = _open
            log['high'] = high
            log['low'] = low
            log['close'] = close
            log['volume'] = volume
            log['mark_price'] = markpx
            log['timestamp'] = timestamp
            
            Logf(log)
            # pprint(log)
            
            self.update[symbol] = datetime.now()
            # INFO(f"Bybit USDT {symbol} save")
        except:
            ERROR(traceback.format_exc())
        


    def on_message(self, _msg):
        try:
            msg = json.loads(_msg)
            if "topic" in msg and str(msg['topic']).startswith("instrument_info"):
                if str(msg['type']) == 'snapshot':
                    symbol = msg['data']['symbol']
                    # pprint(msg)
                    self.volume24h[symbol]   = float(msg['data']['volume_24h_e8']) / 10**8
                    self.turnover24h[symbol] = float(msg['data']['turnover_24h_e8']) / 10**8
                    self.markpx[symbol]      = float(msg['data']['mark_price'])
            elif 'topic' in msg and str(msg['topic']).startswith("candle"):
                symbol = str(msg['topic']).split('.')[-1]
                threading.Thread(target = lambda: self.on_klines(msg['data'][0], symbol)).start()
                # self.on_klines(msg['data'][0], symbol)
            else:
                return
                INFO(_msg)
        except:
            ERROR(traceback.format_exc())

    def on_error(self, err):
        # INFO(f"Bybit ERR:{err}")
        self._err = True
        
    def on_close(self):
        # INFO("Bybit close")
        self.init()

    def on_open(self):
        symbols_str = str([f"candle.5.{s}" for s in self.symbols] + [f"instrument_info.100ms.{s}" for s in self.symbols]).replace('\'', '\"')
        tradeStr=f"""{{ "op":"subscribe", "args": {symbols_str} }}"""
        self.ws.send(tradeStr)
        # symbols_str = str([f"instrument_info.100ms.{s}" for s in self.symbols])
        # tradeStr=f"""{{ "op":"subscribe", "args": {symbols_str} }}"""
        # self.ws.send(tradeStr)
        INFO("Bybit connected")

class piBybitKlineSpot():
    def __init__(self):
        ERROR("Bybit connected")
        self.symbols = ["BTCUSDT","ETHUSDT"]
        self.wss = "wss://stream.bybit.com/spot/quote/ws/v1"
        self.turnover24h = {}
        self.volume24h = {}
        self.settle_currency = {}
        self.markpx = {}
        self.lastpx = {}
        self.update = dict(zip(self.symbols, [datetime.now() for _ in self.symbols]))

    def init(self):
        try:
            self.get_settlecurrency()

            self._err = False
            # url = self.wss + "/stream?streams="
            url = self.wss

            # for symbol in self.symbols:
            #     s = symbol.upper()
            #     url = url + f"{s.lower()}@ticker/{s.lower()}@kline_5m/"

            # url = url[:-1]
            INFO(f"Bybit Spot wss--> {url}")
            self.ws = websocket.WebSocketApp( url,
                                        on_message = self.on_message,
                                        on_error = self.on_error,
                                        on_close = self.on_close,
                                        on_open = self.on_open) 
            self.wst = threading.Thread(target=lambda: self.ws.run_forever())
            self.wst.daemon = True
            self.wst.start()

            conn_timeout = 5

            while ((not self.ws.sock or not self.ws.sock.connected) and conn_timeout and not self._err):
                time.sleep(1)
                conn_timeout -= 1

            if not conn_timeout or self._err:
                ERROR(f"Bybit Spot can not connect wss")
            
        except:
            ERROR(traceback.format_exc())
    
    def get_settlecurrency(self):
        url = f"""https://api.bybit.com/spot/v1/symbols"""
        r = requests.get(url)
        if r.ok:
            a = json.loads(r.text)
            for s in a['result']:
                symbol = s['name']
                if symbol not in self.symbols:
                    continue
                self.settle_currency[symbol] = s['quoteCurrency']
                INFO(f"{symbol}: {self.settle_currency[symbol]}")
        else:
            ERROR(f"Bybit Spot Https Error {r.text}")

    def on_klines(self,msg):
        try:
            # if msg['k']["x"] == False:
            #     return
            exchange = "Bybit"
            ac = 'spot'
            symbol = msg['s']
            check_a = self.update[symbol]
            if datetime.now() - check_a < timedelta(minutes=4):
                return
            t = GetFmtTm()
            while symbol not in self.turnover24h:
                time.sleep(0.1)
            while symbol not in self.settle_currency:
                time.sleep(0.1)
            turnover24h = float(self.turnover24h[symbol])
            volume24h = float(self.volume24h[symbol])
            settle_currency = self.settle_currency[symbol]
            markpx = None #现货没有标记价格
            lastpx = None #现货先空着吧
            # k = msg["k"]
            k = msg
            _open = float(k['o'])
            close = float(k['c'])
            high = float(k['h'])
            low = float(k['l'])
            volume = float(k['v'])
            timestamp = GetFmtTmFromBybit(int(k['t']))
            
            log = {}
            log['exchange'] = exchange
            log['ac'] = ac
            log['symbol'] = symbol
            log['t'] = GetFmtTm()
            log['turnover24h'] = turnover24h
            log['volume24h'] = volume24h
            log['settle_currency'] = settle_currency
            log['open'] = _open
            log['high'] = high
            log['low'] = low
            log['close'] = close
            log['volume'] = volume
            log['timestamp'] = timestamp
            
            Logf(log)
            self.update[symbol] = datetime.now()

            # INFO(f"Bybit Spot {symbol} save")
        except:
            ERROR(traceback.format_exc())
        


    def on_message(self, _msg):
        try:
            msg = json.loads(_msg)
            if "topic" in msg and msg['topic'] == 'realtimes':
                symbol = msg['symbol']
                self.volume24h[symbol] = msg['data'][0]['v']
                self.turnover24h[symbol] = msg['data'][0]['qv']
            elif 'topic' in msg and msg['topic'] == 'kline':
                threading.Thread(target = lambda: self.on_klines(msg['data'][0])).start()
        except:
            ERROR(traceback.format_exc())

    def on_error(self, err):
        # INFO(f"Bybit ERR:{err}")
        self._err = True
        
    def on_close(self):
        # INFO("Bybit close")
        self.init()

    def on_open(self):
        symbols_str = ','.join(self.symbols)
        tradeStr=f"""{{"symbol":"{symbols_str}","topic":"kline_5m","event":"sub","params":{{"binary":false}}}}"""
        self.ws.send(tradeStr)
        tradeStr=f"""{{"symbol":"{symbols_str}","topic":"realtimes","event":"sub","params":{{"binary":false}}}}"""
        self.ws.send(tradeStr)
        INFO("Bybit connected")

class piBybitKlineCoin():
    def __init__(self):
        ERROR("Bybit connected")
        self.symbols = ["BTCUSDZ21","ETHUSDZ21", "BTCUSD", "ETHUSD", "BTCUSDH22", "ETHUSDH22"]
        self.wss = "wss://stream.bybit.com/realtime"
        self.turnover24h = {}
        self.volume24h = {}
        self.settle_currency = {}
        self.markpx = {}
        self.lastpx = {}
        self.alias = {
            "BTCUSDZ21" : "BTCUSD_211231",
            "ETHUSDZ21" : "ETHUSD_211231",
            "BTCUSD" : "BTCUSD_PERP",
            "ETHUSD" : "ETHUSD_PERP",
            "BTCUSDH22" : "BTCUSD_220325",
            "ETHUSDH22" : "ETHUSD_220325"
        }
        self.update = dict(zip(self.symbols, [datetime.now() for _ in self.symbols]))

    def init(self):
        try:
            self.get_settlecurrency()

            self._err = False
            # url = self.wss + "/stream?streams="
            url = self.wss

            # for symbol in self.symbols:
            #     s = symbol.upper()
            #     url = url + f"{s.lower()}@ticker/{s.lower()}@kline_5m/"

            # url = url[:-1]
            INFO(f"Bybit Coin wss--> {url}")
            self.ws = websocket.WebSocketApp( url,
                                        on_message = self.on_message,
                                        on_error = self.on_error,
                                        on_close = self.on_close,
                                        on_open = self.on_open)
            self.wst = threading.Thread(target=lambda: self.ws.run_forever())
            self.wst.daemon = True
            self.wst.start()

            conn_timeout = 5

            while ((not self.ws.sock or not self.ws.sock.connected) and conn_timeout and not self._err):
                time.sleep(1)
                conn_timeout -= 1

            if not conn_timeout or self._err:
                ERROR(f"Bybit Coin can not connect wss")

        except:
            ERROR(traceback.format_exc())

    def get_settlecurrency(self):
        url = f"""https://api.bybit.com/v2/public/symbols"""
        r = requests.get(url)
        if r.ok:
            a = json.loads(r.text)
            for s in a['result']:
                symbol = s['name']
                if symbol not in self.symbols:
                    continue
                # self.settle_currency[symbol] = s['quote_currency']
                self.settle_currency[symbol] = "BTC"
                INFO(f"{symbol}: {self.settle_currency[symbol]}")
        else:
            ERROR(f"Bybit Coin Https Error {r.text}")

    def on_klines(self,msg, symbol):
        try:
            # if msg['k']["x"] == False:
            #     return
            check_a = self.update[symbol]
            if datetime.now() - check_a < timedelta(minutes=4):
                return
            exchange = "Bybit"
            ac = 'coin'
            # symbol = msg['s']
            t = GetFmtTm()
            while symbol not in self.turnover24h:
                time.sleep(0.1)
            while symbol not in self.settle_currency:
                time.sleep(0.1)
            while symbol not in self.markpx:
                time.sleep(0.1)
            turnover24h = float(self.turnover24h[symbol])
            volume24h = float(self.volume24h[symbol])
            settle_currency = self.settle_currency[symbol]
            markpx = float(self.markpx.get(symbol, 0))
            lastpx = None #现货先空着吧
            # k = msg["k"]
            k = msg
            _open = float(k['open'])
            close = float(k['close'])
            high = float(k['high'])
            low = float(k['low'])
            volume = float(k['volume'])
            timestamp = GetFmtTmFromBybit(int(k['timestamp']/10**3))

            log = {}
            log['exchange'] = exchange
            log['ac'] = ac
            log['symbol'] = symbol
            log['symbol'] = self.alias.get(symbol, symbol)
            log['t'] = GetFmtTm()
            log['turnover24h'] = turnover24h
            log['volume24h'] = volume24h
            log['settle_currency'] = settle_currency
            log['open'] = _open
            log['high'] = high
            log['low'] = low
            log['close'] = close
            log['volume'] = volume
            log['mark_price'] = markpx
            log['timestamp'] = timestamp

            Logf(log)
            # pprint(log)

            self.update[symbol] = datetime.now()
            # INFO(f"Bybit Coin {symbol} save")
        except:
            ERROR(traceback.format_exc())



    def on_message(self, _msg):
        try:
            msg = json.loads(_msg)
            if "topic" in msg and str(msg['topic']).startswith("instrument_info"):
                if str(msg['type']) == 'snapshot':
                    symbol = msg['data']['symbol']
                    self.volume24h[symbol]   = msg['data']['volume_24h']
                    self.turnover24h[symbol] = msg['data']['turnover_24h_e8'] / 10**8
                    self.markpx[symbol]      = msg['data']['mark_price']
            elif 'topic' in msg and str(msg['topic']).startswith("kline"):
                symbol = str(msg['topic']).split('.')[-1]
                # threading.Thread(target = lambda: self.on_klines(msg['data'][0])).start()
                self.on_klines(msg['data'][0], symbol)
            else:
                INFO(_msg)
        except:
            ERROR(traceback.format_exc())

    def on_error(self, err):
        INFO(f"Bybit ERR:{err}")
        self._err = True

    def on_close(self):
        # ERROR("Bybit close")
        self.init()

    def on_open(self):
        symbols_str = str([f"klineV2.5.{s}" for s in self.symbols] + [f"instrument_info.100ms.{s}" for s in self.symbols]).replace('\'', '\"')
        tradeStr=f"""{{ "op":"subscribe", "args": {symbols_str} }}"""
        self.ws.send(tradeStr)
        # symbols_str = str([f"instrument_info.100ms.{s}" for s in self.symbols])
        # tradeStr=f"""{{ "op":"subscribe", "args": {symbols_str} }}"""
        # self.ws.send(tradeStr)
        INFO("Bybit connected")


if __name__ == "__main__":
    if len(sys.argv) == 3:
        
        url = URL_WS[sys.argv[1]]
        symbol = str(sys.argv[2]).upper()
        # logger.add(f"/data/md/bybit_{sys.argv[1]}_{sys.argv[2]}-{{time:YYYY-MM-DD}}.log", format="{message}",level="INFO",rotation="00:00")
        a = piBybitMD(url, symbol)
        a.initiate().run_forever()
