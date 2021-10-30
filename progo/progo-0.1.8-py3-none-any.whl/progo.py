import attr
import atexit
import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Union, List
from uuid import UUID

from requests import exceptions
from loguru import logger

from bleak import BleakClient
from bleak.backends.device import BLEDevice
import requests
from requests.exceptions import ConnectionError
from wireless import Wireless

from progo.ble.constants import (
    CHARACTERISTIC_WIFI_ACCESS_POINT_PASSWORD,
    CHARACTERISTIC_WIFI_ACCESS_POINT_SSID,
    CONTROL_QUERY_COMMAND_UUID,
    UTF_8,
)
from progo.ble.util import find_gopros
from progo.constants import (
    OPEN_GOPRO_BASE_URL,
    THUMBNAIL_DIR,
    SCREENNAIL_DIR,
    GPMF_DIR,
    MEDIA_INFO_DIR,
    TELEMETRY_DIR,
    DCIM_DIR
)
from progo.exceptions import NoGoprosFoundException
from progo.params import (
    FPS,
    AutoOff,
    MaxLensMode,
    MultishotFOV,
    PhotoFOV,
    PresetGroup,
    Resolution,
    VideoFOV,
    LED,
    Toggle,
)
from progo.settings import SETTINGS_ATTR_INT_MAP, CameraSettings
from progo.status import CameraStatus


def update_state(func):
    def wrap(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self._set_progo_state()
        return result

    return wrap


def turbo_enabled(func):
    def wrap(self, *args, **kwargs):
        self.enable_turbo_mode()
        result = func(self, *args, **kwargs)
        self.disable_turbo_mode()
        return result

    return wrap


@attr.s
class MediaFile:
    directory: str = attr.ib()
    name: str = attr.ib()
    created: int = attr.ib(converter=int)
    modified: int = attr.ib(converter=int)
    glrv: int = attr.ib()
    ls: int = attr.ib()
    size: int = attr.ib(converter=int)

    @property
    def camera_path(self):
        return Path(self.directory, self.name)

    @property
    def gpmf_name(self):
        """Add gpmf extension to the filename"""
        return f"{self.name}.gpmf"

    @property
    def thumbnail_name(self):
        """Add a jpg extension to the filename"""
        return f"{self.name}.jpg"

    @property
    def screennail_name(self):
        return self.thumbnail_name


def run_async_function_synchronously(async_func: Callable, *args, **kwargs):
    """Because I want to use `bleak` but actively don't care about async."""
    coroutine = async_func(*args, **kwargs)
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coroutine)


def get_gopro(id: str = None) -> BLEDevice:
    gopros = run_async_function_synchronously(find_gopros)
    if not gopros:
        raise NoGoprosFoundException(
            "No Gopros found! Please set 'Wireless Connections' to 'On' or get closer to your camera."
        )
    if id:
        logger.debug(f"Discovering gopro {id}")
        for gopro in gopros:
            if id == gopro.name[-4:]:
                logger.debug(f"Found gopro {id}")
                return gopro
    return gopros[0]


class Progo:
    def __init__(self, gopro_id: str = None) -> None:
        self._gopro_id: str = gopro_id
        self._gopro: BLEDevice = None
        self._ble_client: BleakClient = None
        self._wireless = Wireless()
        self._open_gopro_base_url = OPEN_GOPRO_BASE_URL
        self.status = None
        self.settings = None
        atexit.register(self._adios)

    def _adios(self):
        logger.debug("Disconnecting ble client")
        if self._ble_client:
            run_async_function_synchronously(self._ble_client.disconnect)

    def _ensure_ble_connection(self):
        logger.debug(f"Ensuring BLE connection to {self._gopro}")
        connected = self._ble_client.is_connected
        while not connected:
            logger.debug("BLE client not connected - connecting")
            connected = run_async_function_synchronously(self._ble_client.connect)
        logger.debug("BLE client connected")

    def _write_ble_gatt_char(self, char_uuid: Union[str, UUID], cmd: int):
        data = bytearray([cmd])
        data.insert(0, len(data))
        self._ensure_ble_connection()
        logger.debug(f"Writing data {data} to {char_uuid}")
        return run_async_function_synchronously(
            self._ble_client.write_gatt_char, char_uuid, data
        )

    def _write_ble_gatt_char_with_param(
        self, char_uuid: Union[str, UUID], cmd: int, param: int
    ):
        data = bytearray([cmd])
        param = bytearray([param])
        data.extend([len(param), *param])
        data.insert(0, len(data))
        self._ensure_ble_connection()
        logger.debug(f"Writing data {data} to {char_uuid}")
        return run_async_function_synchronously(
            self._ble_client.write_gatt_char, char_uuid, data
        )

    def _http_get(self, url: str):
        url = f"{self._open_gopro_base_url}/{url}"
        response = requests.get(url, stream=True)
        return response

    @turbo_enabled
    def _http_get_contents_to_file(self, url: str, output_file: Path):
        if output_file.exists():
            logger.debug(f"{output_file} already exists - not downloading.")
        else:
            logger.debug(f"Writing {url} response contents to file {output_file}")
            response = self._http_get(url)
            output_file.parents[0].mkdir(parents=True, exist_ok=True)
            output_file.write_bytes(response.content)

    def _get_json(self, url: str):
        response = self._http_get(url)
        return response.json()

    # BLE commands

    def power_down(self):
        logger.debug("Powering down camera")
        return self._write_ble_gatt_char(CONTROL_QUERY_COMMAND_UUID, 0x04)

    def sleep(self):
        logger.debug("Putting camera into standby")
        return self._write_ble_gatt_char(CONTROL_QUERY_COMMAND_UUID, 0x05)

    def enable_wifi_ap(self):
        logger.debug("Enabling wifi access point")
        return self._write_ble_gatt_char_with_param(
            CONTROL_QUERY_COMMAND_UUID, 0x17, Toggle.ON.value
        )

    def disable_wifi_ap(self):
        logger.debug("Disabling wifi access point")
        return self._write_ble_gatt_char_with_param(
            CONTROL_QUERY_COMMAND_UUID, 0x17, Toggle.OFF.value
        )

    def get_wifi_ssid(self):
        logger.debug("Getting wifi ssid")
        ssid = run_async_function_synchronously(
            self._ble_client.read_gatt_char, CHARACTERISTIC_WIFI_ACCESS_POINT_SSID
        )
        return ssid.decode(UTF_8)

    def get_wifi_password(self):
        logger.debug("Getting wifi password")
        password = run_async_function_synchronously(
            self._ble_client.read_gatt_char, CHARACTERISTIC_WIFI_ACCESS_POINT_PASSWORD
        )
        return password.decode(UTF_8)

    # Wifi commands

    @update_state
    def set_third_party_client_info(self):
        # 2.0 only
        return self._get_json("gopro/camera/analytics/set_client_info")

    @update_state
    def start_encoding(self):
        # 2.0 only
        return self._http_get("gopro/camera/shutter/start")

    @update_state
    def set_shutter_on(self):
        # 2.0 only
        return self.start_encoding()

    @update_state
    def stop_encoding(self):
        # 2.0 only
        return self._http_get("gopro/camera/shutter/stop")

    def set_shutter_off(self):
        # 2.0 only
        return self.stop_encoding()

    @update_state
    def set_digital_zoom(self, zoom_percent: int):
        return self._get_json(f"gopro/camera/digital_zoom?percent={zoom_percent}")

    def get_camera_state(self):
        return self._get_json("gopro/camera/state")

    def set_keep_alive(self):
        return self._get_json("gopro/camera/keep_alive")

    def get_media_list(self) -> List[MediaFile]:
        response = self._get_json("gopro/media/list")
        media_list = []
        for directory in response["media"]:
            directory_name = directory["d"]
            for file in directory["fs"]:
                media_list.append(
                    MediaFile(
                        directory=directory_name,
                        name=file["n"],
                        created=file["cre"],
                        modified=file["mod"],
                        glrv=file.get("glrv"),
                        ls=file.get("ls"),
                        size=file["s"],
                    )
                )
        return media_list

    def get_file(self, media_file: MediaFile, output_path: Path = None):
        if not output_path:
            output_path = DCIM_DIR.joinpath(media_file.name)
        self._http_get_contents_to_file(
            f"videos/DCIM/{media_file.camera_path}", output_path
        )

    def get_gpmf_data(self, media_file: MediaFile, output_path: Path = None):
        if not output_path:
            output_path = GPMF_DIR.joinpath(media_file.gpmf_name)
        self._http_get_contents_to_file(
            f"gopro/media/gpmf?path={media_file.camera_path}", output_path
        )

    def get_media_info(self, media_file: MediaFile, output_path: Path = None):
        if not output_path:
            output_path = MEDIA_INFO_DIR.joinpath(media_file.name)
        self._http_get_contents_to_file(
            f"gopro/media/info?path={media_file.camera_path}", output_path
        )

    def get_screennail(self, media_file: MediaFile, output_path: Path = None):
        if not output_path:
            output_path = SCREENNAIL_DIR.joinpath(media_file.screennail_name)
        self._http_get_contents_to_file(
            f"gopro/media/screennail?path={media_file.camera_path}", output_path
        )

    def get_thumbnail(self, media_file: MediaFile, output_path: Path = None):
        if not output_path:
            output_path = THUMBNAIL_DIR.joinpath(media_file.thumbnail_name)
        self._http_get_contents_to_file(
            f"gopro/media/thumbnail?path={media_file.camera_path}", output_path
        )

    def get_telemetry(self, media_file: MediaFile, output_path: Path = None):
        if not output_path:
            output_path = TELEMETRY_DIR.joinpath(media_file.telemetry_name)
        self._http_get_contents_to_file(
            f"gopro/media/telemetry?path={media_file.camera_path}", output_path
        )

    def get_open_gopro_api_version(self):
        return self._get_json("gopro/version")['version']

    def get_preset_status(self):
        return self._get_json("gopro/camera/presets/get")

    @update_state
    def set_preset(self, preset: int) -> dict:
        resp = self._get_json(f"gopro/camera/presets/load?id={preset}")
        return resp

    @update_state
    def set_preset_group(self, preset_group: PresetGroup) -> dict:
        return self._get_json(f"gopro/camera/presets/set_group?id={preset_group.value}")

    @update_state
    def start_preview_stream(self):
        return self._get_json("gopro/camera/stream/start")

    @update_state
    def stop_preview_stream(self):
        return self._get_json("gopro/camera/stream/stop")

    @update_state
    def enable_turbo_mode(self):
        return self._get_json(f"gopro/media/turbo_transfer?p={Toggle.ON.value}")

    @update_state
    def disable_turbo_mode(self):
        return self._get_json(f"gopro/media/turbo_transfer?p={Toggle.OFF.value}")

    @update_state
    def _update_camera_setting(self, setting: int, option: int):
        return self._get_json(f"gopro/camera/setting?setting={setting}&option={option}")

    def set_resolution(self, resolution: Resolution):
        resolution_id = SETTINGS_ATTR_INT_MAP["resolution"]
        return self._update_camera_setting(resolution_id, resolution.value)

    def set_fps(self, fps: FPS):
        fps_id = SETTINGS_ATTR_INT_MAP["fps"]
        return self._update_camera_setting(fps_id, fps.value)

    def set_auto_off(self, auto_off: AutoOff):
        auto_off_id = SETTINGS_ATTR_INT_MAP["auto_off"]
        return self._update_camera_setting(auto_off_id, auto_off.value)

    def set_led(self, led: LED):
        led_id = SETTINGS_ATTR_INT_MAP["led"]
        return self._update_camera_setting(led_id, led.value)

    def set_video_fov(self, fov: VideoFOV):
        video_fov_id = SETTINGS_ATTR_INT_MAP["video_fov"]
        return self._update_camera_setting(video_fov_id, fov.value)

    def set_photo_fov(self, fov: PhotoFOV):
        photo_fov_id = SETTINGS_ATTR_INT_MAP["photo_fov"]
        return self._update_camera_setting(photo_fov_id, fov.value)

    def set_multi_shot_fov(self, fov: MultishotFOV):
        multi_shot_fov_id = SETTINGS_ATTR_INT_MAP["multi_shot_fov"]
        return self._update_camera_setting(multi_shot_fov_id, fov.value)

    def set_max_lens_mode(self, max_lens_mode: MaxLensMode):
        max_lens_mode_id = SETTINGS_ATTR_INT_MAP["max_lens_mode"]
        return self._update_camera_setting(max_lens_mode_id, max_lens_mode.value)

    # General

    def connect_to_wifi_ap(self):
        logger.info("Connecting to wap")
        connection_attempt = 1
        connected = False
        while not connected:
            logger.debug(f"WAP connection attempt {connection_attempt}")
            connected = self._wireless.connect(
                ssid=self.get_wifi_ssid(), password=self.get_wifi_password()
            )
            connection_attempt += 1
        return connected

    def _set_progo_state(self) -> bool:
        state_set = False
        attempt_num = 1
        while not state_set:
            try:
                state = self.get_camera_state()
                self.settings = CameraSettings.from_dict(state["settings"])
                self.status = CameraStatus.from_dict(state["status"])
                state_set = True
            except ConnectionError:
                attempt_num += 1
        return state_set

    def initialize(self):
        logger.info("Initializing progo")
        self._gopro = get_gopro(self._gopro_id)
        self._gopro_id = self._gopro.name[-4:]
        self._ble_client = BleakClient(self._gopro)
        self._ensure_ble_connection()
        self.enable_wifi_ap()
        self.connect_to_wifi_ap()
        self._set_progo_state()
        logger.info("Progo initialized")
