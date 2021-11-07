import aiohttp


class HTTPClient:
    def __init__(self, authorization: str):
        self.__key__ = authorization
        self.__base__ = 'https://api.pgamerx.com/v5'

    async def request(self, endpoint, *, params = None):
        if params is None:
            params = {}

        session = aiohttp.ClientSession()
        async with session.get(f"{self.__base__}/{endpoint}", headers = {'Authorization': self.__key__}, params=params) as response:

            try:
                response = await response.json()
                await session.close()
                return response
            except aiohttp.client_exceptions.ContentTypeError:
                await session.close()
                return await response.text()

    async def post(self, endpoint, *, params = None):
        if params is None:
            params = {}

        session = aiohttp.ClientSession()
        async with session.post(f"{self.__base__}/{endpoint}", headers = {'Authorization': self.__key__}, params=params) as response:

            try:
                await session.close()
                return await response.json()
            except aiohttp.client_exceptions.ContentTypeError:
                await session.close()
                return await response.text()