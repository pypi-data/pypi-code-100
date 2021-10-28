import asyncio
import aiohttp
import tqdm
import sys
from .ratelimiter import RateLimiter


class APICaller:
    def __init__(self, software_api_key=None, user_api_key=None):
        self.aiohttp_basic_auth = aiohttp.BasicAuth(software_api_key, user_api_key)

    async def __get_from_url_async(self, url, session):
        while(1):
            try:
                async with await session.get(url) as response:
                    # print("Made API call to", urllib.parse.unquote(url))

                    if response.status != 429:
                        # print(response.status)
                        return await response.json()
            except aiohttp.ClientConnectionError as e:
                print('Connection error: ', str(e))

            # print("Too many requests (async).", url)
            await asyncio.sleep(1)

    async def __url_list_task_handler(self, url_list):
        tasks = []

        async with aiohttp.ClientSession(auth=self.aiohttp_basic_auth) as session:
            session = RateLimiter(session)

            for url in url_list:
                task = asyncio.ensure_future(self.__get_from_url_async(url, session))
                tasks.append(task)

            # return await asyncio.gather(*tasks, return_exceptions=True)
            responses = []
            for f in tqdm.tqdm(asyncio.as_completed(tasks), total=len(tasks), unit='reqs', file=sys.stdout):
                responses.append(await f)

            return responses

    def get_from_url_list(self, url_list):
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.__url_list_task_handler(url_list))
        responses = loop.run_until_complete(future)

        return responses
