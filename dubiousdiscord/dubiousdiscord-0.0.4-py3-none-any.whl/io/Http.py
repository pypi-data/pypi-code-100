
from __future__ import annotations

from typing import Awaitable, Callable, Generic, Optional, TypeVar

import requests
import dubious.objects as data
import aiohttp
import asyncio

_VERSION = "v9"
BASE_URL = f"https://discord.com/api/{_VERSION}"

def removeNonDicts(l: list) -> list[dict]:
    if not isinstance(l, list):
        return []
    i = 0
    while i < len(l):
        c = l[i]
        if not isinstance(c, dict):
            l.pop(i)
        else:
            i += 1
    return l

class HTTPError(Exception):
    """ Something went wrong with an HTTP request."""

class PermissionError(HTTPError):
    """ The request failed because the bot's header was missing permissions. """

class EmptyMessageError(HTTPError):
    """ The request failed because the given raw message didn't have one of a "content", "embeds", or "files" field. """

t_ch = TypeVar("t_ch", bound=data.HasID)
class Cache(Generic[t_ch]):
    def __init__(self, cast: type[t_ch], maxSize: int=1000):
        self.cast = cast
        self.maxSize = maxSize
        self.items: dict[data.Snowflake, t_ch] = {}
        self.order: list[data.Snowflake] = []
    
    def _add(self, item: t_ch):
        if item.id in self.items:
            return self.items[item.id]
        if len(self.items) + 1 > self.maxSize:
            self.items.pop(self.order[0])
            self.order.pop(0)
        self.items[item.id] = item
        self.order.append(item.id)
        return item
    
    def add(self, j: dict | list):
        if isinstance(j, list):
            items = [self.cast(**item) for item in removeNonDicts(j)]
            for item in items:
                self._add(item)
        item = self.cast(**j)
        item = self._add(item)
        return item
    
    def get(self, oID: data.Snowflake):
        return self.items.get(oID)
    
    def __call__(self, **kwargs):
        return self.add(kwargs)

t_req = TypeVar("t_req", bound=data.Data)
class Requester(Generic[t_req]):
    def __init__(self, session: aiohttp.ClientSession, cast: type[t_req] | Cache[t_req], endpoint: str, headers: dict=None):
        self.session = session
        self.cast = cast
        self.endpoint = endpoint
        self.headers = headers

    async def request(self, func: Callable[[str], Awaitable[aiohttp.ClientResponse]], j: dict=None, params: dict=None):
        kwargs = {"headers": self.headers}
        if j: kwargs["json"] = j
        if params: kwargs["params"] = params

        async with func(self.endpoint, **kwargs) as res:
            if not res.status in range(200, 300):
                err: dict = await res.json()
                code = err.get("code", res.status)
                message = err.get("message", res.text)
                raise HTTPError(f"Encountered error ({code}): {message}")
            if await res.text():
                got = await res.json()
                if isinstance(got, list):
                    return [self.cast(**item) for item in removeNonDicts(got)]
                return self.cast(**got)
            else:
                return None

    async def get(self, params: dict=None): return await self.request(self.session.get, params=params)
    async def put(self, j: dict, params: dict=None): return await self.request(self.session.put, j, params)
    async def post(self, j: dict, params: dict=None): return await self.request(self.session.post, j, params)
    async def patch(self, j: dict, params: dict=None): return await self.request(self.session.patch, j, params)
    async def delete(self, params: dict=None): return await self.request(self.session.delete, params=params)

class Http:
    def __init__(self, appID: data.Snowflake, appToken: str, session: aiohttp.ClientSession):
        self.appID = appID
        self.appToken = appToken
        self.session = session

        self.commandsCache = Cache(data.ApplicationCommand)
        self.guildsCache = Cache(data.Guild)
        self.channelsCache = Cache(data.Channel)
        self.messagesCache = Cache(data.Message)
        self.webhooksCache = Cache(data.Webhook)

        self.applications = f"/applications/{self.appID}"

        self.auth = {
            "Authorization": f"Bot {self.appToken}"
        }
    
    def commands(self, commandID: Optional[data.Snowflake]=None, guildID: Optional[data.Snowflake]=None):
        guilds = f"/guilds/{guildID}" if guildID else ""
        commands = f"/commands/{commandID}" if commandID else "/commands"
        return Requester(self.session, self.commandsCache, BASE_URL + self.applications + guilds + commands, self.auth)

    def interactions(self, ixnID: data.Snowflake, ixnToken: str):
        interactions = f"/interactions/{ixnID}/{ixnToken}/callback"
        return Requester(self.session, None, BASE_URL + interactions, self.auth)
    
    def guilds(self, guildID: data.Snowflake):
        guilds = f"/guilds/{guildID}"
        return Requester(self.session, self.guildsCache, BASE_URL + guilds, self.auth)
    
    def channels(self, channelID: data.Snowflake):
        channels = f"/channels/{channelID}"
        return Requester(self.session, self.channelsCache, BASE_URL + channels, self.auth)
    
    def messages(self, channelID: data.Snowflake, messageID: Optional[data.Snowflake]=None):
        channels = f"/channels/{channelID}"
        messages = f"/messages/{messageID}" if messageID else f"/messages"
        return Requester(self.session, self.messagesCache, BASE_URL + channels + messages, self.auth)
    
    def webhooks(self, webhookID: Optional[data.Snowflake], webhookToken: Optional[str]):
        webhooks = f"/webhooks/"
        wid = f"/{webhookID}" if webhookID else ""
        token = f"/{webhookToken}" if webhookID and webhookToken else ""
        return Requester(self.session, self.webhooksCache, BASE_URL + webhooks + wid + token, self.auth)
    
    def webhookMessages(self, webhookID: data.Snowflake, webhookToken: str, messageID: Optional[data.Snowflake]=None):
        webhooks = f"/webhooks/{webhookID}/{webhookToken}"
        messages = f"/messages/{messageID}" if messageID else ""
        return Requester(self.session, self.messagesCache, BASE_URL + webhooks + messages, self.auth)