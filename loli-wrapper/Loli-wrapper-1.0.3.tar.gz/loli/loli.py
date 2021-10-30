import asyncio
import httpx
import requests
from typing import Union

from .handler import EndpointNotFound

BASE_URL = "https://loli-api.ml"

class BaseClass:

    def __init__(self):
        self._ahttp = httpx.AsyncClient()
        self._http = requests

class LoliAsync(BaseClass):

    def __init__(self):
        super().__init__()
    
    async def get_point(self, category, endpoint):
        category = category or 'sfw'
        if not endpoint:
            raise EndpointNotFound()
        else:
            async with self._ahttp as session:
                data = await session.get(f'{BASE_URL}/{category}/{endpoint}')
            return data.json()

    async def random_image(self):
        async with self._ahttp as session:
            ends = await session.get(f'{BASE_URL}/endpoints')
            ends.json()
        async with self._ahttp as session:
            data = await session.get(f'{BASE_URL}/sfw/{__import__("random").choice(ends["sfw"])}')
        return data.json()

class LoliSync(BaseClass):

    def __init__(self):
        super().__init__()

    def get_point(self, category, endpoint):
        category = category or 'sfw'
        if not endpoint:
            raise EndpointNotFound()
        else:
            data = self._http.get(f'{BASE_URL}/{category}/{endpoint}')
            return data.json()
        

    def random_image(self):
        ends = self._http.get(f'{BASE_URL}/endpoints').json()
        data = self._http.get(f'{BASE_URL}/sfw/{__import__("random").choice(ends["sfw"])}').json()
        return data
