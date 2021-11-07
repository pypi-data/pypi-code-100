#!/usr/bin/python3
# -*- mode: python; coding: utf-8 -*-

import asyncio
import datetime

from gattlib import GATTRequester, GATTResponse


class Response(GATTResponse):
    def __init__(self, loop, ev, *args):
        super().__init__(*args)
        self.data = []
        self.loop = loop
        self.ev = ev
        self.done = asyncio.Event()
        self.timer = None

    def on_response(self, data):
        print('<---', data)
        self.data.append(data)

    def on_response_complete(self):
        self.loop.call_soon_threadsafe(self.done.set)
        self.loop.call_soon_threadsafe(self.ev.set)

    def get_data(self):
        if not self.done.is_set():
            raise ValueError('No data')
        self.done.clear()
        data = self.data
        self.data = []
        return data


class Requester(GATTRequester):
    def __init__(self, loop, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop = loop
        self._connection_state_changed = asyncio.Event()

    def set_state(self):
        self._connection_state_changed.set()

    def on_connect(self, mtu):
        print('connected cb!')
        print(mtu)
        self.loop.call_soon_threadsafe(self.set_state)
        return mtu


class A:
    def __init__(self) -> None:
        self.service = None
        self.ev = asyncio.Event()

    # async def _wait_for_conn(self, service):
    #     while not service.is_connected():
    #         await asyncio.sleep(0.1)

    async def _conn(self):
        loop = asyncio.get_running_loop()
        self.service = Requester(loop, '58:2D:34:32:E0:69', False)
        print('..conn')
        # with concurrent.futures.ThreadPoolExecutor(10) as pool:
        #     loop.run_in_executor(pool, self.service.connect, False, 'public')
        loop.run_in_executor(None, self.service.connect, False, 'public')
        await asyncio.sleep(0)
        # (False, 'public')
        print('..conn')
        await self.service._connection_state_changed.wait()

    async def conn(self):
        await asyncio.wait_for(self._conn(), 10)
        print('CONNECTED!')

    async def disconn(self):
        print('try to disconnect')

        asyncio.get_running_loop().run_in_executor(
            None, self.service.disconnect,
        )
        # self.service.connect(False, 'public')
        # await asyncio.wait_for(self._wait_for_conn(self.service), 10)

        print('DISCONNECTED!')

    async def get_services(self):
        print('get_services1')
        loop = asyncio.get_running_loop()
        print('get_services2')
        await asyncio.sleep(0)
        response = Response(loop, self.ev)
        print('discover_primary_async')
        await asyncio.sleep(0)
        self.service.discover_primary_async(response)
        await asyncio.sleep(0)
        print('..waiting')
        await response.done.wait()
        primary = response.get_data()
        return primary

    async def run(self):
        await self.conn()
        await asyncio.sleep(5)
        try:
            primary = await self.get_services()
            print(primary)
            # response = Response(loop)
            # self.service.discover_primary_async(response)
            # await response.done.wait()
            # primary = response.get_data()
            # print('primary', primary)
            for prim in primary:
                print(prim)
            await asyncio.sleep(0)
        finally:
            await self.disconn()


async def counter():
    while True:
        print(datetime.datetime.now().isoformat())
        await asyncio.sleep(1)


async def amain():
    a = A()
    # await a.run()

    async def b():
        await a.ev.wait()
        print('EVENT!')

    await asyncio.gather(counter(), a.run(), b(), return_exceptions=True)

asyncio.run(amain(), debug=True)
