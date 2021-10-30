import asyncio
from contextlib import asynccontextmanager
from uuid import UUID
from typing import AsyncContextManager, List, Union

from bleak import BleakScanner, BleakClient
from bleak.backends.device import BLEDevice


async def find_devices() -> List[BLEDevice]:
    return await BleakScanner.discover()


async def find_gopros() -> List[BLEDevice]:
    return [device for device in await find_devices() if "gopro" in device.name.lower()]


async def find_device_by_address(address: str) -> BLEDevice:
    devices = await find_devices()
    for device in devices:
        if address == device.address:
            return device


async def find_gopro_by_id(id: str) -> BLEDevice:
    gopros = await find_gopros()
    for gopro in gopros:
        if id in gopro.name.lower():
            return gopro
