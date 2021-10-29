import aiohttp
import aiohttp.client_exceptions
from urllib.parse import urljoin
from aiomeilisearch.config import Config
from aiomeilisearch.error import AioMeiliSearchApiError, AioMeiliSearchTimeoutError
import asyncio
from functools import wraps

def ExceptionCacher(func):
    @wraps(func)
    async def wrapper(client, *args, **kwargs):
        try:
            return await func(client, *args, **kwargs)
        except asyncio.TimeoutError:
            msg = "Http Request {0}: {1}{2} Timeout. " \
                  "Check config param 'timeout' in <aiomeilisearch.Client()> ".format(func.__name__, client.config.url, args[0] )
            raise AioMeiliSearchTimeoutError( msg )
        except aiohttp.client_exceptions.ClientConnectorError as err:
            raise AioMeiliSearchTimeoutError(str(err))
    return wrapper

class HttpClient():
    def __init__(self, config: Config) -> None:
        self.config = config
        if config.api_key:
            self.headers = {
                'X-Meili-Api-Key': config.api_key,
            }
        else:
            self.headers = {}

    async def _handle_resp(self, response):
        if response.content_type == 'application/json':
            resp = await response.json()
        else:
            resp = response.content
        try:
            response.raise_for_status()
        except aiohttp.client_exceptions.ClientResponseError as err:
            raise AioMeiliSearchApiError(str(err), resp)
        return resp

    @ExceptionCacher
    async def get(self, path, args=None):
        url = urljoin(self.config.url, path)
        params = {}
        if self.config.timeout:
            params['timeout'] = self.config.timeout
        if self.headers:
            params['headers'] = self.headers
        if args:
            params['params'] = args
        async with aiohttp.ClientSession() as session:
            async with session.get(url, **params) as response:
                return await self._handle_resp(response)

    @ExceptionCacher
    async def post(self, path, json_=None):
        url = urljoin(self.config.url, path)
        params = {}
        if self.config.timeout:
            params['timeout'] = self.config.timeout
        if self.headers:
            params['headers'] = self.headers
        if json_:
            params["json"] = json_
        async with aiohttp.ClientSession() as session:
            async with session.post(url, **params) as response:
                return await self._handle_resp(response)

    @ExceptionCacher
    async def put(self, path, json_=None):
        url = urljoin(self.config.url, path)
        params = {}
        if self.config.timeout:
            params['timeout'] = self.config.timeout
        if self.headers:
            params['headers'] = self.headers
        if json_:
            params["json"] = json_
        async with aiohttp.ClientSession() as session:
            async with session.put(url, **params) as response:
                return await self._handle_resp(response)

    @ExceptionCacher
    async def delete(self, path):
        url = urljoin(self.config.url, path)
        params = {}
        if self.config.timeout:
            params['timeout'] = self.config.timeout
        if self.headers:
            params['headers'] = self.headers
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, **params) as response:
                return  await self._handle_resp(response)
