from datetime import datetime
from typing import Union

from httpx import Response

from neuroio.base import IAMBase, IAMBaseAsync, IAMBaseBase
from neuroio.constants import sentinel
from neuroio.utils import request_dict_processing, request_query_processing


class LicensesBase(IAMBaseBase):
    def get_url(self, key: str = None) -> str:
        if key:
            return self.base_url + f"/v1/licenses/sources/{key}/"
        else:
            return self.base_url + "/v1/licenses/sources/"


class Impl(IAMBase, LicensesBase):
    def create(self, name: str, entry_storage_days: int = 1) -> Response:
        data = request_dict_processing(locals(), ["self"])

        with self.get_client() as client:
            return client.post(url=self.get_url(), json=data)

    def list(
        self,
        q: str = "",
        date_from: Union[datetime, object] = sentinel,
        date_to: Union[datetime, object] = sentinel,
        is_bound: Union[bool, object] = sentinel,
        limit: int = 20,
        offset: int = 0,
    ) -> Response:
        data = request_query_processing(locals(), ["self"])

        with self.get_client() as client:
            return client.get(url=self.get_url(), params=data)

    def get(self, id: str) -> Response:
        with self.get_client() as client:
            return client.get(url=self.get_url(f"{id}"))

    def update(
        self,
        id: int,
        name: str,
        is_active: bool = True,
        entry_storage_days: int = 1,
    ) -> Response:
        data = request_dict_processing(locals(), ["self", "id"])

        with self.get_client() as client:
            return client.patch(url=self.get_url(f"{id}"), json=data)


class ImplAsync(IAMBaseAsync, LicensesBase):
    async def create(self, name: str, entry_storage_days: int = 1) -> Response:
        data = request_dict_processing(locals(), ["self"])

        async with self.get_client() as client:
            return await client.post(url=self.get_url(), json=data)

    async def list(
        self,
        q: str = "",
        date_from: Union[datetime, object] = sentinel,
        date_to: Union[datetime, object] = sentinel,
        is_bound: Union[bool, object] = sentinel,
        limit: int = 20,
        offset: int = 0,
    ) -> Response:
        data = request_query_processing(locals(), ["self"])

        async with self.get_client() as client:
            return await client.get(url=self.get_url(), params=data)

    async def get(self, id: int) -> Response:
        async with self.get_client() as client:
            return await client.get(url=self.get_url(f"{id}"))

    async def update(
        self,
        id: int,
        name: str,
        is_active: bool = True,
        entry_storage_days: int = 1,
    ) -> Response:
        data = request_dict_processing(locals(), ["self", "id"])
        async with self.get_client() as client:
            return await client.patch(url=self.get_url(f"{id}"), json=data)
