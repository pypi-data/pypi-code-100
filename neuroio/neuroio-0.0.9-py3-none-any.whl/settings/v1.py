from httpx import Response

from neuroio.base import APIBase, APIBaseAsync, APIBaseBase
from neuroio.constants import (
    DEFAULT_EXACT_THRESHOLD,
    DEFAULT_HA_THRESHOLD,
    DEFAULT_JUNK_THRESHOLD,
)
from neuroio.utils import request_dict_processing


class SettingsBase(APIBaseBase):
    def get_url(self, key: str = None) -> str:
        if key:
            return self.base_url + f"/v1/settings/thresholds/{key}/"
        else:
            return self.base_url + "/v1/settings/thresholds/"


class Impl(APIBase, SettingsBase):
    def get(self) -> Response:
        with self.get_client() as client:
            return client.get(url=self.get_url())

    def update(
        self,
        exact: float = DEFAULT_EXACT_THRESHOLD,
        ha: float = DEFAULT_HA_THRESHOLD,
        junk: float = DEFAULT_JUNK_THRESHOLD,
    ) -> Response:
        data = request_dict_processing(locals(), ["self"])

        with self.get_client() as client:
            return client.patch(url=self.get_url(), data=data)

    def reset(self) -> Response:
        with self.get_client() as client:
            return client.post(url=self.get_url("reset"))


class ImplAsync(APIBaseAsync, SettingsBase):
    async def get(self) -> Response:
        async with self.get_client() as client:
            return await client.get(url=self.get_url())

    async def update(
        self,
        exact: float = DEFAULT_EXACT_THRESHOLD,
        ha: float = DEFAULT_HA_THRESHOLD,
        junk: float = DEFAULT_JUNK_THRESHOLD,
    ) -> Response:
        data = request_dict_processing(locals(), ["self"])

        async with self.get_client() as client:
            return await client.patch(url=self.get_url(), data=data)

    async def reset(self) -> Response:
        async with self.get_client() as client:
            return await client.post(url=self.get_url("reset"))
