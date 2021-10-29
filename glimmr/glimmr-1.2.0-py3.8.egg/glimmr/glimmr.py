from __future__ import annotations

import asyncio
import json
import logging
import socket
from dataclasses import dataclass
from typing import Any, Dict, List

import aiohttp
import async_timeout
import backoff
from requests import Session
from signalrcore.hub.auth_hub_connection import AuthHubConnection
from signalrcore.hub.base_hub_connection import BaseHubConnection
from signalrcore.hub_connection_builder import HubConnectionBuilder
from signalrcore.subject import Subject
from signalrcore.transport.websockets.connection import ConnectionState
from yarl import URL

from .exceptions import (
    GlimmrConnectionError,
    GlimmrRConnectionTimeoutError,
    GlimmrEmptyResponseError,
    GlimmrError,
)
from .models import SystemData, StatData


@dataclass
class Glimmr:
    """
    Main class for handling connections with Glimmr.
    this is presently an incomplete implementation of the
    Glimmr api, focusing primarily on features relevant to
    Home Assistant.
    """
    host: str
    ambient_scenes: Dict[str, int]
    audio_scenes: Dict[str, int]
    request_timeout: float = 8.0
    session: aiohttp.ClientSession | None = None
    socket: AuthHubConnection | BaseHubConnection | None = None
    system_data: SystemData | None = None
    stats: StatData | None = None
    _close_session: bool = False
    LOGGER = logging.getLogger(__name__)

    def __init__(self, host: str):
        self.host = host
        with Session():
            url = "http://" + self.host + "/socket"
            self.LOGGER.debug("Websocket url: " + url)
            self.socket = HubConnectionBuilder() \
                .with_url(url) \
                .build()
            self.socket.on('olo', self.ws_olo)
            self.socket.on('mode', self.set_mode)

    async def __aenter__(self) -> Glimmr:
        """Async enter."""
        return self

    async def __aexit__(self, *_exc_info) -> None:
        """Async exit."""
        await self.socket.stop()

    @property
    def connected(self) -> bool:
        """Return if we are connect to the WebSocket of a Glimmr device.

        Returns:
            True if we are connected to the WebSocket of a Glimmr device,
            False otherwise.
        """
        return self.socket.transport.state == ConnectionState.connected

    def ws_olo(self, data) -> None:
        """
        Handler for websocket store data.
        @param data: Glimmr StoreData object.
        """
        self.LOGGER.debug("OLO FIRED: ", data[0]["systemData"])
        self.system_data = SystemData.from_dict(data[0]["systemData"])
        self.load_scenes(data[0]["ambientScenes"])
        self.stats = StatData.from_dict(data[0]["stats"])

    def ws_mode(self, mode: {}) -> None:
        """
        Update the stored mode from websocket.
        @param mode: The new device mode
        """
        if self.system_data is not None:
            self.LOGGER.debug("Registering dev mode change from ws: ", mode[0])
            self.system_data.device_mode = mode[0]

    @backoff.on_exception(backoff.expo, GlimmrConnectionError, max_tries=3, logger=None)
    async def request(
            self,
            uri: str = "",
            method: str = "GET",
            data: Any | None = None,
    ) -> Any:
        """Handle a request to a Glimmr device.

        A generic method for sending/handling HTTP requests done gainst
        the Glimmr device.

        Args:
            uri: Request URI, for example `/json/si`.
            method: HTTP method to use for the request.E.g., "GET" or "POST".
            data: Integer, string, or SystemData object to send to the endpoint.

        Returns:
            A Python dictionary (JSON decoded) with the response from the
            Glimmr device.

        Raises:
            GlimmrConnectionError: An error occurred while communitcation with
                the Glimmr device.
            GlimmrConnectionTimeoutError: A timeout occurred while communicating
                with the Glimmr device.
            GlimmrError: Received an unexpected response from the Glimmr device.
        """
        path = "/api/Glimmr/" + uri
        url = URL.build(scheme="http", host=self.host, port=80, path=path)
        self.LOGGER.debug("URL: %s", url)
        headers = {
            "Accept": "application/json, text/plain, */*",
        }

        if self.session is None:
            self.LOGGER.debug("Setting session...")
            self.session = aiohttp.ClientSession()
            self._close_session = True

        try:
            with async_timeout.timeout(self.request_timeout):
                self.LOGGER.debug("Awaiting response...")
                response = await self.session.request(
                    method,
                    url,
                    json=data,
                    headers=headers,
                )
        except asyncio.TimeoutError as exception:
            raise GlimmrRConnectionTimeoutError(
                f"Timeout occurred while connecting to Glimmr device at {self.host}"
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise GlimmrConnectionError(
                f"Error occurred while communicating with Glimmr device at {self.host}"
            ) from exception

        content_type = response.headers.get("Content-Type", "")
        if (response.status // 100) in [4, 5]:
            contents = await response.read()
            response.close()

            if content_type == "application/json":
                raise GlimmrError(response.status, json.loads(contents.decode("utf8")))
            raise GlimmrError(response.status, {"message": contents.decode("utf8")})

        if "application/json" in content_type:
            response_data = await response.json()
            if (
                    method == "POST"
                    and uri == "systemData"
                    and self.system_data is not None
                    and data is not None
            ):
                self.system_data.from_dict(data={"glimmr_data": response_data})
            return response_data
        return await response.text()

    @backoff.on_exception(
        backoff.expo, GlimmrEmptyResponseError, max_tries=3, logger=None
    )
    async def update(self):
        """Get all information about the device in a single call.

        This method updates all Glimmr information available with a single API
        call.

        Returns:
            Glimmr Device data.

        Raises:
            GlimmrEmptyResponseError: The Glimmr device returned an empty response.
        """
        if self.connected:
            subject = Subject()
            self.LOGGER.debug("Requesting store data via websocket.")
            self.socket.send("store", subject)
            return

        else:
            self.LOGGER.debug("Updating via GET")
            data = await self.request("store")
            if not data:
                raise GlimmrEmptyResponseError(
                    f"Glimmr device at {self.host} returned an empty API"
                    " response on full update"
                )
            self.LOGGER.debug("GOT: %s", data["systemData"])
            self.system_data = SystemData.from_dict(data["systemData"])
            self.load_scenes(data["ambientScenes"])

    async def update_scenes(self):
        scenes = await self.request("ambientScenes")
        if scenes:
            self.load_scenes(scenes)

    async def set_mode(self, mode: int) -> None:
        """
        Set the new device mode.
        Args:
            mode: New target device mode.
        """
        await self.request(
            "mode", method="POST", data=mode
        )

    async def set_ambient_scene(self, scene: int) -> None:
        """
        Update the ambient scene.
        Args:
            scene: Scene ID to change to.
        """
        await self.request(
            "ambientScene", method="POST", data=scene
        )

    async def set_audio_scene(self, scene: int) -> None:
        """
        Update the ambient scene.
        Args:
            scene: Scene ID to change to.
        """
        await self.request(
            "ambientScene", method="POST", data=scene
        )

    async def set_ambient_color(self, color: str) -> None:
        """
        Update the ambient scene.
        Args:
            color: Ambient color to set in a hex formatted string
            with no '#'.
        """
        self.LOGGER.debug("Setting ambient color: " + color)
        await self.request(
            "ambientColor", method="POST", data=color
        )

    async def set_system_data(self):
        """
        Push current settings to Glimmr for update.
        """
        self.LOGGER.debug("Updating sd object.")
        await self.request("systemData", method="POST", data=self.system_data.to_dict())

    async def reboot(self) -> None:
        """
        Reboot Glimmr device.
        """
        self.LOGGER.debug("Reboot requested.")
        await self.request("systemControl", method="POST", data="reboot")

    def get_scene_id_from_name(self, name) -> int | None:
        """
        Fetch ambient scene id by name.
        @param name: Scene name to look up.
        @return Scene id if found or None
        """
        if self.ambient_scenes is not None:
            for i in self.ambient_scenes.items():
                if i[0] == name:
                    return i[1]
        return None

    def get_scene_name_from_id(self, scene) -> str | None:
        """
        Fetch ambient scene name by id.
        @param scene:
        @return: A string with the scene name if found or None.
        """
        if self.ambient_scenes is not None:
            for i in self.ambient_scenes.items():
                if i[1] == scene:
                    return i[0]
        return None

    def load_scenes(self, scenes: List[Dict[str, int]]):
        """
        Load scenes from store data.
        @param scenes: Data from store object/api.
        """
        #  Sneaky way of hiding mode controls in the scene selection
        scene_dict = {"Video": -2, "Audio": -3, "Ambient": -4, "Audio/Video": -5, "Streaming": -6}
        for item in scenes:
            scene_id = item.get("id", 0)
            scene_name = item.get("name", "")
            scene_dict[scene_name] = scene_id

        self.LOGGER.debug("Scene dict: ", scene_dict)
        self.ambient_scenes = scene_dict
