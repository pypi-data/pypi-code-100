from contextlib import asynccontextmanager

import aiohttp


@asynccontextmanager
async def client():
    async with aiohttp.ClientSession() as session:
        yield session
