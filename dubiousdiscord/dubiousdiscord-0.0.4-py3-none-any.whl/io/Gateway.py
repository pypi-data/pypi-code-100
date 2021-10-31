
import asyncio
import datetime as dt
import json
from typing import Optional

from websockets import client
from websockets import exceptions as wsExceptions

from dubious.objects import Payload

GATEWAY_URI = "wss://gateway.discord.gg/?v=9&encoding=json"

def printWithTime(text: str):
    print(f"[{str(dt.datetime.now().time())[:-7]}] {text}")

class Gateway:
    def __init__(self, uri: Optional[str]=None):
        self.uri = uri if uri else GATEWAY_URI

        self.sendQ: asyncio.Queue[Payload] = asyncio.Queue()
        self.recvQ: asyncio.Queue[Payload] = asyncio.Queue()
        self.running = asyncio.Event()
        self.ws: client.WebSocketClientProtocol = None
        self.closedCoro: Optional[asyncio.Task] = None
        self.recvCoro: Optional[asyncio.Task] = None
        self.sendCoro: Optional[asyncio.Task] = None
    
    def getStartingCoros(self):
        #print("staring gateway connection")
        self.recvCoro = self.loopRecv()
        self.sendCoro = self.loopSend()
        self.closedCoro = self.loopClosed()
        connectCoro = self.connect()
        return self.recvCoro, self.sendCoro, self.closedCoro, connectCoro
    
    async def connect(self):
        self.ws = await client.connect(self.uri)
        self.running.set()
        #print("gateway connected")
    
    async def loopClosed(self):
        await self.running.wait()
        await self.ws.wait_closed()
        try:
            printWithTime("websocket closed\n" + f"  code: {self.ws.close_code}" + "\n" + f"  reason: {self.ws.close_reason}")
        except AttributeError:
            printWithTime("websocket closed due to error")
    
    async def loopRecv(self):
        await self.running.wait()
        #print("Gateway loopRecv entered")
        while self.running.is_set():
            try:
                data = await asyncio.wait_for(self.ws.recv(), timeout=1)
            except asyncio.TimeoutError:
                continue
            except wsExceptions.ConnectionClosedError:
                self.running.clear()
                #print("Gateway loopRecv's connection was closed")
                continue
            except wsExceptions.ConnectionClosedOK:
                self.ws = await client.connect(self.uri)
            payload: dict = Payload(**json.loads(data))
            #printWithTime(f"R: {payload}")
            await self.recvQ.put(payload)
        #print("Gateway loopRecv exited")

    async def loopSend(self):
        await self.running.wait()
        #print("Gateway loopSend entered")
        while self.running.is_set():
            try:
                payload = await asyncio.wait_for(self.sendQ.get(), timeout=1)
            except asyncio.TimeoutError:
                continue
            data = json.dumps(payload)
            #printWithTime(f"S: {payload}")
            await self.ws.send(data)
        #print("Gateway loopSend exited")
    
    async def recv(self):
        return await self.recvQ.get()
    
    async def send(self, payload: dict):
        await self.sendQ.put(payload)
    
    async def stop(self, code=1000):
        #print("stopping gateway connection")
        self.running.clear()
        await self.recvCoro
        await self.sendCoro
        await self.ws.close(code)
        await self.closedCoro

    async def restart(self, loop: asyncio.AbstractEventLoop):
        #print("attempting gateway restart")
        if self.running.is_set():
            await self.stop()
        self.getStartingCoros(loop)