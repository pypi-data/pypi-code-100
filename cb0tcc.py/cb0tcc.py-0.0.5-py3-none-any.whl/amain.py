from aiohttp import ClientSession

class acb0t:
    def __init__(self, url):
        self.__url = url

    async def connect(self):
        async with ClientSession() as session:
            async with session.post("https://cb0t.cc/api/create", data = {"url": self.__url}) as r:
                self.data = await r.json()

    @property
    def url(self):
        return self.data["url"]