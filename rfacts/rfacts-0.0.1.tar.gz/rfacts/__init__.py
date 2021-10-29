import requests
import aiohttp
from typing import Union

url = "https://uselessfacts.jsph.pl/random.json?language="

class InvalidLangauge(Exception):
    pass

class fact():
    def __init__(self, *, json: bool=False, language: str="en") -> None:
        self.json: bool = json
        self.id: str = None
        self.source: str = None
        if language not in ("en", "de"): 
            raise InvalidLangauge(f"'{language}' is not a valid language, valid languages are 'en' and 'de'")
        self.language: str = language
        self.permalink: str = None
        self.text: str = None

    def get(self) -> Union[str, dict]:
        data = requests.get(url+self.language).json()
        self.id = data['id']
        self.source = data['source']
        self.permalink = data['permalink']
        self.text = data['text']
        if self.json:
            return data
        return self.text

    async def aget(self) -> Union[str, dict]:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.get(url+self.language) as resp:
                data = await resp.json()
        self.id = data['id']
        self.source = data['source']
        self.permalink = data['permalink']
        self.text = data['text']
        if self.json:
            return data
        return self.text