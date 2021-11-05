from typing import List

from ..pyzio_settings import PyzioSettings


class MQTTConfig:

    def __init__(self, settings: PyzioSettings):
        self._settings = settings

    def host(self) -> str:
        return self._settings.mqtt_host()

    def ports(self) -> List[int]:
        return self._settings.mqtt_ports()
