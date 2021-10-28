from typing import List, Union

from httpx import Response

from neuroio.base import APIBase, APIBaseAsync, APIBaseBase
from neuroio.constants import (
    EntryLiveness,
    EntryMood,
    EntryResult,
    HttpMethod,
    Sex,
    sentinel,
)
from neuroio.utils import request_dict_processing, request_query_processing


class NotificationsBase(APIBaseBase):
    def get_url(self, key: str = None) -> str:
        if key:
            return self.base_url + f"/v1/notifications/{key}/"
        else:
            return self.base_url + "/v1/notifications/"


class Impl(APIBase, NotificationsBase):
    def create(
        self,
        name: str,
        http_method: HttpMethod,
        destination_url: str,
        is_active: bool = True,
        moods: Union[List[EntryMood], object] = sentinel,
        results: Union[List[EntryResult], object] = sentinel,
        liveness: Union[List[EntryLiveness], object] = sentinel,
        age_from: Union[int, object] = sentinel,
        age_to: Union[int, object] = sentinel,
        sex: Union[List[Sex], object] = sentinel,
        sources: Union[List[int], object] = sentinel,
        persons_groups: Union[List[int], object] = sentinel,
    ) -> Response:
        data = request_dict_processing(locals(), ["self"])

        with self.get_client() as client:
            return client.post(url=self.get_url(), json=data)

    def list(
        self,
        q: Union[str, object] = sentinel,
        spaces_ids: Union[List[int], object] = sentinel,
        limit: int = 20,
        offset: int = 0,
    ) -> Response:
        data = request_query_processing(locals(), ["self"])

        with self.get_client() as client:
            return client.get(url=self.get_url(), params=data)

    def get(self, id: int) -> Response:
        with self.get_client() as client:
            return client.get(url=self.get_url(f"{id}"))

    def update(
        self,
        id: int,
        name: str,
        http_method: HttpMethod,
        destination_url: str,
        is_active: bool = True,
        moods: Union[List[EntryMood], object] = sentinel,
        results: Union[List[EntryResult], object] = sentinel,
        liveness: Union[List[EntryLiveness], object] = sentinel,
        age_from: Union[int, object] = sentinel,
        age_to: Union[int, object] = sentinel,
        sex: Union[List[Sex], object] = sentinel,
        sources: Union[List[int], object] = sentinel,
        persons_groups: Union[List[int], object] = sentinel,
    ) -> Response:
        data = request_dict_processing(locals(), ["self", "id"])

        with self.get_client() as client:
            return client.patch(url=self.get_url(f"{id}"), json=data)

    def delete(self, id: int) -> Response:
        with self.get_client() as client:
            return client.delete(url=self.get_url(f"{id}"))


class ImplAsync(APIBaseAsync, NotificationsBase):
    async def create(
        self,
        name: str,
        http_method: HttpMethod,
        destination_url: str,
        is_active: bool = True,
        moods: Union[List[EntryMood], object] = sentinel,
        results: Union[List[EntryResult], object] = sentinel,
        liveness: Union[List[EntryLiveness], object] = sentinel,
        age_from: Union[int, object] = sentinel,
        age_to: Union[int, object] = sentinel,
        sex: Union[List[Sex], object] = sentinel,
        sources: Union[List[int], object] = sentinel,
        persons_groups: Union[List[int], object] = sentinel,
    ) -> Response:
        data = request_dict_processing(locals(), ["self"])

        async with self.get_client() as client:
            return await client.post(url=self.get_url(), json=data)

    async def list(
        self,
        q: Union[str, object] = sentinel,
        spaces_ids: Union[List[int], object] = sentinel,
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
        http_method: HttpMethod,
        destination_url: str,
        is_active: bool = True,
        moods: Union[List[EntryMood], object] = sentinel,
        results: Union[List[EntryResult], object] = sentinel,
        liveness: Union[List[EntryLiveness], object] = sentinel,
        age_from: Union[int, object] = sentinel,
        age_to: Union[int, object] = sentinel,
        sex: Union[List[Sex], object] = sentinel,
        sources: Union[List[int], object] = sentinel,
        persons_groups: Union[List[int], object] = sentinel,
    ) -> Response:
        data = request_dict_processing(locals(), ["self", "id"])
        async with self.get_client() as client:
            return await client.patch(url=self.get_url(f"{id}"), json=data)

    async def delete(self, id: int) -> Response:
        async with self.get_client() as client:
            return await client.delete(url=self.get_url(f"{id}"))
