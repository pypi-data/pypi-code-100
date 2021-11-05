"""
Main API used for jarvis' server.
This API uses aiohttp rather than the requests module for asynchronous programming.
"""

from dataclasses import dataclass
from typing import Tuple, Union

import aiohttp
import requests  # Used for validating if the server has started

from .exceptions import *
from .structure import Context


@dataclass
class APIResponse:
    status: int
    reason: str
    contentType: str
    json: dict


class API:
    def __init__(self, url: str, logging: object, **kwargs) -> None:
        self.origin = kwargs.get("origin", "discord")

        self.logging = logging
        self.url = url
        self.key = kwargs.get("key", ".")

        # Validate if the server is up
        try:
            r = requests.get(self.endpoint, json={"__key__": self.key})
            if r.status_code in [401, 403]:
                raise APIKeyError(self.key)
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to connect to jarvis' server. Please check your url. ({e})")
    
    @property
    def endpoint(self) -> str:
        return self.url + "/api/"
    
    def changeBase(self, url: str) -> None:
        """
        Change the base url.

        Parameters
        ----------
        `host` : str
        `port` : str
        `protocol` : str = "http"

        Raises
        ------
        `ConnectionError` : When changing the base url failed because it is not valid or available.
        """
        
        try:
            requests.get(url)
        except requests.exceptions.RequestException:
            raise ConnectionError(f"Failed to change base url to {url}")
        
        self.url = url
    
    async def request(self, url: str, method: str = "post", **kwargs) -> APIResponse:
        """
        Perform a request using aiohttp.

        Parameters
        ----------
        `url` : str
        `method` : str

        Returns
        -------
        APIResponse object

        Raises
        ------
        `APIRequestFailed` : When attempting to send a request fails.
        `InvalidMethod` : When the method provided is invalid.
        """

        def mappings(s):
            return {
                "post": s.post,
                "get": s.get
            }
        
        json_ = kwargs.pop("json", {})
        json_["__key__"] = self.key

        async with aiohttp.ClientSession() as session:
            method_ = mappings(session).get(method)
            if not method_:
                raise InvalidMethod(f"{method} is not a valid method.")
            
            try:
                async with method_(url, json=json_, **kwargs) as r:
                    r = APIResponse(
                        r.status,
                        r.reason,
                        r.content_type,
                        await r.json()
                    )

                    if r.status in [401, 403]:
                        raise APIKeyError(self.key)
                    
                    return r

            except Exception as e:
                raise APIRequestFailed(f"URL: {url} ({e})")
            
    async def play(self, name: str, cls: str = None, **kwargs) -> dict:
        """
        Play a piece of audio that is stored in the api.player library of jarvis.

        Parameters
        ----------
        `name` : str
        `cls` : str
            Which class inside the api.player library to choose from.
            If a class is not provided, you can provide a file path via the `name` parameter. File must exist on the server side.
        `c` : int
            How many times to repeat the audio

        Returns
        -------
        json response of the api as a `dict`.

        Raises
        -------
        `FileNotFoundError` : 
            If the file provided via `name` is not found. File names will be ignored if `cls` is provided.
        `AttributeError` :
            If the attribute name provided via `name` is not found.
        `ValueError` :
            If the class provided via `cls` is not valid. (i.e., not found)
        `UnknownServerError` :
            If an error has occured in the server side and that error is unknown.
        """

        exceptions = {
            "FileNotFoundError": FileNotFoundError,
            "AttributeError": AttributeError,
            "ValueError": ValueError
        }

        payload = {"cls": cls, "name": name, **kwargs}
        response = await self.request(self.endpoint + "audio/play", json=payload)
        response = response.json

        if response["status"] != 200:
            exception = exceptions.get(response["msg"], UnknownServerError)
            raise exception
        
        return response
        
    async def stopAudio(self) -> dict:
        """
        Stop all audio being played by the server.

        Returns
        -------
        json response of the api as a `dict`.
        """

        response = await self.request(self.endpoint + "audio/stop")
        return response.json
    
    async def say(self, text: Union[str, list]) -> dict:
        """
        Make jarvis say something.

        Parameters
        ----------
        `text` : Union[str, list]
            If a string is provided, jarvis will just say whatever that string is.
            If a list of strings is provided, jarvis will randomly choose from those list of strings.
        
        Returns
        -------
        json response of the api as a `dict`
        """

        payload = {"text": text}
        response = await self.request(self.endpoint +  "say", json=payload)
        return response.json
    
    async def preprocess(self, text: str, **kwargs) -> Tuple[bool, str, str]:
        """
        Preprocess the given text.
        Preprocessing basically checks if the text given starts with the prefixes. Will also clean up the text such as removing the prefix if it starts with one.

        Parameters
        ----------
        `text` : str
            Text to preprocess.
        `situation` : str
            The current situation when calling this function. By default this is None.
            If this is None, jarvis will attempt to figure out its current situation in the server side.
        `origin` : str
            The current origin. By default this is self.origin
        `prefixes` : list
            A list of prefixes to choose from. By default, jarvis will create a list of its own from the wakewords inside the config.json in the server.
        
        Returns
        -------
        Tuple : [bool, str, str]
            first value is whether the text passed the preprocessing.(i.e., checking if the text starts with the prefix or not)

            second value is just the passed text but str.stripped()

            third value is the cleaned text (i.e., no prefix). If preprocessing didn't pass, this will be the same as the second value.
        """

        origin = kwargs.get("origin", self.origin)
        situation = kwargs.get("situation", "default")

        payload = {"text": text, "origin": origin, "situation": situation}
        response = await self.request(self.endpoint + "preprocess", json=payload)
        response = response.json

        if response["data"]:
            return (
                response["data"]["passed"],
                response["data"]["text"],
                response["data"]["modified"]
            )

        return (False, text, text)
    
    async def process(self,  text: str, **kwargs) -> Context:
        """
        Process text and run the command connected to the processed text.

        Parameters
        ----------
        `text` : str
            Text to process.
        `origin` : str
            Where the text came from. By defaults this is self.origin
        `situation` : str
            The current situation when calling "process". By default this is None.
            If this is None, then the current situation will be processed within jarvis itself. (Most likely current default value is 'default')
        `intents` : List[str]
            Take a list of intents to choose from. By default this would be None and jarvis would choose from all intents in its current possesion.
        `bypassPreprocess` : bool
            If true, bypass preprocessing. (Will ignore if the text starts with a wakeword or not).
        `requirements` : List[float]
            List with 2 items corresponding to the probability requirements of jarvis. First value is the regular probability and second is the followup probability.
        `prefixes` : List[str]
            A list of prefixes to preprocess from. By default a list of prefixes will automaticlally be generated from jarvis' config.json
        
        Returns
        -------
        `Context` object
        """

        origin = kwargs.get("origin", self.origin)
        payload = {"text": text, "origin": origin, **kwargs}

        response = await self.request(self.endpoint + "process", json=payload)
        response = response.json

        if not response["data"]:
            return None
        
        return Context(
            self,
            response["data"],
            origin,
            response["data"]["situation"],
            self.logging
        )

