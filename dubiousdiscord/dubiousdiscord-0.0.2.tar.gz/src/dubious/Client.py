
from __future__ import annotations

import asyncio
import sys
from typing import Optional
from dubious.Bot import Bot
from dubious.Dispatch import Dispatch, createDispatch

from dubious.io.Gateway import Gateway
import dubious.enums.events as events
from dubious.objects import Ready

class Client:
    # The client's secret.
    token: str
    # The intents for the client.
    intents: int
    # The connection to the websocket through which to recieve and request information.
    gateway: Gateway

    # Whether or not the running loops are supposed to be stopped.
    stopped: asyncio.Event

    # The time between heartbeats in milliseconds.
    beatTime: Optional[int]
    # Whether or not the latest heartbeat has been acknowledged.
    beatAcked: asyncio.Event
    # Whether or not the heartbeat loop is active.
    beating: asyncio.Event
    # The last sequence number gotten with a recieved payload.
    sequence: Optional[int]

    # Whether or not the Client has recieved the Ready event.
    #  Signifies that each of the below fields are not None.
    ready: asyncio.Event
    # The session ID (used to reconnect).
    sessionID: Optional[str]
    # The operating Bot object.
    bot: Bot

    def __init__(self, token: str, intents: int, botClass: Bot, gateway: Optional[Gateway]=None):
        super().__init__()
        self.token = token
        self.intents = intents
        self.botClass = botClass
        self.gateway = gateway if gateway else Gateway()

        self.stopped = asyncio.Event()

        self.beatTime = None
        self.beatAcked = asyncio.Event()
        self.beating = asyncio.Event()
        self.sequence = None

        self.ready = asyncio.Event()
        self.sessionID = None
        self.bot = botClass(self.token)

        self.beatAcked.set()

    ###
    # Asyncio stuff
    ###

    def start(self):
        """ Starts the listen loop and the beat loop for the Client.
            Starts the Gateway's loops.
            Runs the asyncio loop forever. """
        try:
            loop = asyncio.get_event_loop()
            coros = []
            coros += self.gateway.getStartingCoros()
            self._taskRecv = self.loopRecv()
            self._taskBeat = self.loopBeat()
            coros += (self._taskRecv, self._taskBeat)
            future = asyncio.gather(
                *coros
            )
            loop.run_until_complete(future)
        except KeyboardInterrupt:
            print("Interrupted, stopping tasks")
            self.stopped.set()
            future.cancel()
            try:
                loop.run_until_complete(future)
            except asyncio.CancelledError:
                pass
        finally:
            print("Done")
    
    async def loopRecv(self):
        #print("Client loopRecv entered")
        while not self.stopped.is_set():
            try:
                payload = await asyncio.wait_for(self.gateway.recv(), timeout=1)
            except asyncio.TimeoutError:
                if not self.gateway.running.is_set():
                    self.stopped.set()
                continue
            self.sequence = payload.s if payload.s != None else self.sequence

            if payload.op == events.onHello:
                self.beatTime = payload.d["heartbeat_interval"]
                self.beating.set()
                await self.sendBeat()
                await self.sendIdentify()
            elif payload.op == events.onBeat:
                await self.sendBeat()
            elif payload.op == events.onBeatAck:
                self.beatAcked.set()
            elif payload.op == events.onReconnect:
                await self.reconnect()
            elif payload.op == events.onInvalidSession:
                if payload.d:
                    await self.reconnect()
            elif payload.t == events.onReady:
                dispatch: Dispatch[Ready] = createDispatch(payload)
                if not dispatch: raise Exception("Ready dispatch couldn't be created.")
                self.sessionID = dispatch.data.session_id
            if payload.t:
                dispatch = createDispatch(payload)
                if not dispatch: continue
                await self.bot.trigger(dispatch.event, dispatch.data)
        #print("Client loopRecv exited")
        
    async def loopBeat(self):
        #print("Client loopBeat entered")
        while not self.stopped.is_set():
            try:
                await asyncio.wait_for(self.beating.wait(), timeout=1)
            except asyncio.TimeoutError:
                continue
            _, toCancel = await asyncio.wait({
                asyncio.sleep(self.beatTime / 1000),
                self.stopped.wait()
            }, return_when=asyncio.FIRST_COMPLETED)
            task: asyncio.Task
            for task in toCancel:
                task.cancel()
            if self.stopped.is_set():
                continue
            if self.beatAcked.is_set():
                self.beatAcked.clear()
                await self.sendBeat()
            else:
                await self.reconnect()
        #print("Client loopBeat exited")
        
    ###
    # Payload sending
    ###

    async def sendBeat(self):
        """ Sends a heartbeat payload. """
        await self.gateway.send({
            "op": 1,
            "d": self.sequence
        })
    
    async def sendIdentify(self):
        """ Sends an identify payload. """
        await self.gateway.send({
            "op": 2,
            "d": {
                "token": self.token,
                "intents": self.intents,
                "properties": {
                    "$os": sys.platform,
                    "$browser": "dubious",
                    "$device": "dubious"
                }
            }
        })
    
    async def reconnect(self):
        """ Clears the ready flag.
            Restarts the gateway's websocket connection.
            Sends a reconnect payload. """
        
        self.stopped.set()
        
        await self.gateway.send({
            "op": 6,
            "d": {
                "token": self.token,
                "session_id": self.sessionID,
                "seq": self.sequence
            }
        })
