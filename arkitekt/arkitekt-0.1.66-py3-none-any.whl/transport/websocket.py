from pydantic.main import BaseModel
from arkitekt.config import TransportProtocol
from arkitekt.transport.base import Transport, TransportConfig
from arkitekt.messages.utils import expandToMessage
from arkitekt.messages.base import MessageMetaExtensionsModel, MessageModel
from arkitekt.transport.registry import register_transport
from herre.herre import get_current_herre
from enum import Enum
import websockets
import json
import asyncio
from arkitekt.legacy.utils import create_task
import logging

logger = logging.getLogger(__name__)


class WebsocketTransportConfig(BaseModel):
    host: str
    port: int
    secure: bool = False
    route: str

    @property
    def protocol(self):
        return "wss" if self.secure else "ws"


class ConnectionFailedError(Exception):
    pass

@register_transport(TransportProtocol.WEBSOCKET)
class WebsocketTransport(Transport):
    configClass = WebsocketTransportConfig
    config: WebsocketTransportConfig


    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.retries = 5
        self.time_between_retries = 5
        self.connection_alive = False
        self.connection_dead = False


    async def aconnect(self):
        if not self.herre.logged_in:
            await self.herre.alogin()

        self.send_queue = asyncio.Queue()
        self.connection_task =  create_task(self.websocket_loop())


    async def adisconnect(self):
        self.connection_task.cancel()

        try:
            await self.connection_task
        except asyncio.CancelledError:
            logger.info(f"Websocket Transport {self} succesfully disconnected")
    


    async def websocket_loop(self, retry=0):
        send_task = None
        receive_task = None

        assert retry < self.retries, "Exceeded number of retries! Postman is disconnected"
        try:
            try:
                async with websockets.connect(f"{self.config.protocol}://{self.config.host}:{self.config.port}{self.config.route}/?token={self.herre.state.access_token}") as client:

                    send_task = create_task(self.sending(client))
                    receive_task = create_task(self.receiving(client))

                    self.connection_alive = True
                    self.connection_dead = False
                    done, pending = await asyncio.wait(
                        [send_task, receive_task],
                        return_when=asyncio.FIRST_EXCEPTION,
                    )
                    self.connection_alive = True

                    for task in pending:
                        task.cancel()

                    raise ConnectionFailedError("Connection failed")

            except Exception as e:
                raise ConnectionFailedError from e

        except ConnectionFailedError as e:
            logger.error("Connection to failed Retrying")
            await asyncio.sleep(self.time_between_retries)
            await self.connection_task(retry=retry + 1)

        except AssertionError as e:
            logger.error("Connection failed Definetly. Postman will fail on next call!")
            self.connection_dead = False

        except asyncio.CancelledError as e:
            logger.info("Got Canceleld")
            if send_task and receive_task:
                 send_task.cancel()
                 receive_task.cancel()

            cancellation = await asyncio.gather(send_task, receive_task, return_exceptions=True)
            raise e


    async def sending(self, client):
        try:
            while True:
                message = await self.send_queue.get()
                logger.debug("Websocket: >>>>>> " + message)
                await client.send(message)
                self.send_queue.task_done()
        except asyncio.CancelledError as e:
            logger.debug("Sending Task sucessfully Cancelled")


    async def receiving(self, client):
        try:
            async for message in client:
                logger.debug("Websocket: <<<<<<< " + message)
                message = expandToMessage(json.loads(message))
                await self.broadcast(message)
        except asyncio.CancelledError as e:
            logger.debug("Receiving Task sucessfully Cancelled")


    async def forward(self, message: MessageModel):
        assert not self.connection_dead, "Connection is definetly dead. Retries have been exceeded. Error"
        await self.send_queue.put(json.dumps(message.dict()))
        


    