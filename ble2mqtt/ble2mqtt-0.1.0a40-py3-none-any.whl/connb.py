#!/usr/bin/python3
# -*- mode: python; coding: utf-8 -*-

import asyncio
import logging
import uuid

# from ble2mqtt.bleak_blupy import add_bluepy_backend
# add_bluepy_backend()
from ble2mqtt.bleak_gattlib import add_gattlib_backend

add_gattlib_backend()

from bleak import BleakClient  # noqa

MJHT_DATA = uuid.UUID('226caa55-6476-4566-7562-66734470666d')
DEVICE_NAME = uuid.UUID('00002a00-0000-1000-8000-00805f9b34fb')
BATTERY = uuid.UUID('00002a19-0000-1000-8000-00805f9b34fb')


def callback(desc, data):
    print(desc, data)


async def amain():
    logging.basicConfig(level='DEBUG')
    client = BleakClient('58:2D:34:32:E0:69', address_type='public')
    try:
        await asyncio.wait_for(client.connect(), 30)
        await client.start_notify(MJHT_DATA, callback)
        print(await client.read_gatt_char(DEVICE_NAME))
        print(await client.read_gatt_char(BATTERY))
        await asyncio.sleep(10)
    finally:
        await client.disconnect()

asyncio.run(amain(), debug=True)
