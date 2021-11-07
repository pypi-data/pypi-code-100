#!/usr/bin/python3
# -*- mode: python; coding: utf-8 -*-

import asyncio
import datetime

from gattlib import DiscoveryService


class A:
    def cb(self, address, data):
        print(address, data)

    async def scan(self):
        service = DiscoveryService("hci0")

        def cb(*args):
            return self.cb(*args)

        # cb1 = self.cb
        # service.set_callback(cb)
        # service.set_callback(lambda *args: self.cb(*args))
        service.set_callback(self.cb)
        try:
            service.start()
        except RuntimeError:
            service.stop()
            service.start()
        try:
            while True:
                r = service.do_step()
                await asyncio.sleep(0)
                print(r)
        finally:
            service.stop()


async def amain():
    a = A()
    asyncio.ensure_future(a.scan())
    while True:
        print(datetime.datetime.now().isoformat())
        await asyncio.sleep(1)

asyncio.run(amain())
