from datetime import datetime
from typing import List, Union

from httpx import Response

from neuroio.base import APIBase, APIBaseAsync, APIBaseBase
from neuroio.constants import EntryLiveness, EntryMood, EntryResult, sentinel
from neuroio.utils import request_query_processing


class EntriesBase(APIBaseBase):
    def get_url(self, key: str = None) -> str:
        if key:
            return self.base_url + f"/v1/entries/{key}/"
        else:
            return self.base_url + "/v1/entries/"


class Impl(APIBase, EntriesBase):
    def list(
        self,
        pid: Union[List[str], object] = sentinel,
        result: Union[List[EntryResult], object] = sentinel,
        age_from: Union[int, object] = sentinel,
        age_to: Union[int, object] = sentinel,
        sex: Union[int, object] = sentinel,
        mood: Union[List[EntryMood], object] = sentinel,
        liveness: Union[List[EntryLiveness], object] = sentinel,
        sources_ids: Union[List[int], object] = sentinel,
        spaces_ids: Union[List[int], object] = sentinel,
        date_from: Union[datetime, object] = sentinel,
        date_to: Union[datetime, object] = sentinel,
        limit: int = 20,
        offset: int = 0,
    ) -> Response:
        data = request_query_processing(locals(), ["self"])
        with self.get_client() as client:
            return client.get(url=self.get_url(), params=data)

    def get(self, pid: str) -> Response:
        with self.get_client() as client:
            return client.get(url=self.get_url(f"stats/pid/{pid}"))

    def delete(self, id: int) -> Response:
        with self.get_client() as client:
            return client.delete(url=self.get_url(f"{id}"))


class ImplAsync(APIBaseAsync, EntriesBase):
    async def list(
        self,
        pid: Union[List[str], object] = sentinel,
        result: Union[List[EntryResult], object] = sentinel,
        age_from: Union[int, object] = sentinel,
        age_to: Union[int, object] = sentinel,
        sex: Union[int, object] = sentinel,
        mood: Union[List[EntryMood], object] = sentinel,
        liveness: Union[List[EntryLiveness], object] = sentinel,
        sources_ids: Union[List[int], object] = sentinel,
        spaces_ids: Union[List[int], object] = sentinel,
        date_from: Union[datetime, object] = sentinel,
        date_to: Union[datetime, object] = sentinel,
        limit: int = 20,
        offset: int = 0,
    ) -> Response:
        data = request_query_processing(locals(), ["self"])
        async with self.get_client() as client:
            return await client.get(url=self.get_url(), params=data)

    async def get(self, pid: str) -> Response:
        async with self.get_client() as client:
            return await client.get(url=self.get_url(f"stats/pid/{pid}"))

    async def delete(self, id: int) -> Response:
        async with self.get_client() as client:
            return await client.delete(url=self.get_url(f"{id}"))
