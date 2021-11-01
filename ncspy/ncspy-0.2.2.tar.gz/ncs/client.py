import asyncio
import aiohttp
import typing
from urllib.parse import quote_plus as urlencode

from .song import SearchResults, Song
from .parser import parse_search_results, parse_song, get_title


class Client:
    def __init__(self, loop=None, session=None, *, close_session=True):
        self.loop = loop or asyncio.get_event_loop()
        self.session = session or aiohttp.ClientSession(loop=self.loop)
        self.created_session = session is None and close_session

    async def get_song(self, id: str, close=True):
        if (self.created_session and close) and self.session == None:
            self.session = aiohttp.ClientSession(loop=self.loop)

        title_req = await self.session.get(f"https://ncs.io/{id}")
        title_req.raise_for_status()

        title_content = await title_req.content.read()
        title = await self.loop.run_in_executor(None, lambda: get_title(title_content))

        search = await self.search(
            title["title"], artists=title["artists"], get=False, close=False
        )
        info: Song = None
        for item in search.items:
            await asyncio.sleep(0)
            if item.title == title["title"]:
                info = item
                break

        req = await self.session.get(
            f"https://ncs.lnk.to/{id}/widget?view=clickthrough"
        )
        req.raise_for_status()

        content = await req.content.read()
        data = await self.loop.run_in_executor(
            None, lambda: parse_song(content, searched=info.data)
        )

        if self.created_session and close:
            await self.session.close()
            self.session = None
        return Song(**data)

    async def search(
        self,
        query: str = None,
        *,
        genre: str = None,
        mood: str = None,
        artists: typing.List[str] = [],
        artist: str = None,
        version=-1,
        page: int = 1,
        get: bool = True,
        close=True,
    ) -> SearchResults:
        versions = {-1: "", 0: "regular-instrumental", 1: "regular", 2: "instrumental"}
        if not query and not genre and not mood and not artists and not artist:
            raise ValueError("Please give at least query.")

        genre = genre or ""
        mood = mood or ""
        artist = artist or ""

        if not isinstance(artists, list):
            raise ValueError("Artists must be a list.")

        if not isinstance(artist, str):
            raise ValueError("Artist must be one string.")

        if not isinstance(page, int):
            raise ValueError("Page must be an integer (number).")

        if not version in versions.keys() and not version.lower() in versions.values():
            vs = []
            for k, v in versions.items():
                vs.append(f'"{k}" or "{v}"')

            vs = ";\n".join(vs)
            raise ValueError(f"Version must be one of those:\n{vs}")
        else:
            version = versions[version] if isinstance(version, int) else version.lower()

        if artists and artist:
            artists = set(artists)
            artists.add(artist)
            artists = list(artists)

        if (self.created_session and close) and self.session == None:
            self.session = aiohttp.ClientSession(loop=self.loop)

        page = await self.session.get(
            "https://ncs.io/music-search?"
            f"q={urlencode(query)}&"
            f"genre={urlencode(genre)}&"
            f"mood={urlencode(mood)}&"
            f"version={urlencode(version)}&"
            f"page={page}"
        )
        page.raise_for_status()
        data = await page.content.read()
        data = await self.loop.run_in_executor(
            None, lambda: parse_search_results(data, wanted_artists=artists)
        )

        items = []
        if get:
            for item in data["items"]:
                items.append((await self.get_song(item["id"], close=False)).data)
        
            data["items"] = items

        if self.created_session and close:
            await self.session.close()
            self.session = None

        return SearchResults(**data)
