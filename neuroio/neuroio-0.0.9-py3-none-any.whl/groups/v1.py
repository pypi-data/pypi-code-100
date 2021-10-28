from typing import List, Union

from httpx import Response

from neuroio.base import APIBase, APIBaseAsync, APIBaseBase
from neuroio.constants import sentinel
from neuroio.utils import request_query_processing


class GroupsBase(APIBaseBase):
    def get_url(self, key: str = None) -> str:
        if key:
            return self.base_url + f"/v1/groups/persons/{key}/"
        else:
            return self.base_url + "/v1/groups/persons/"


class Impl(APIBase, GroupsBase):
    def create(self, name: str) -> Response:
        data = {"name": name}
        with self.get_client() as client:
            return client.post(url=self.get_url(), json=data)

    def list(
        self,
        q: Union[str, object] = sentinel,
        pids_include: Union[List[str], object] = sentinel,
        pids_exclude: Union[List[str], object] = sentinel,
        groups_ids: Union[List[int], object] = sentinel,
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

    def update(self, id: int, name: str) -> Response:
        data = {"name": name}
        with self.get_client() as client:
            return client.patch(url=self.get_url(f"{id}"), json=data)

    def delete(self, id: int) -> Response:
        with self.get_client() as client:
            return client.delete(url=self.get_url(f"{id}"))

    def persons(
        self,
        id: int,
        pids: Union[List[str], object] = sentinel,
        limit: int = 20,
        offset: int = 0,
    ) -> Response:
        data = request_query_processing(locals(), ["self", "id"])

        with self.get_client() as client:
            return client.get(url=self.get_url(f"{id}/pids"), params=data)

    def add(self, pids: List[str], groups_ids: List[int]) -> Response:
        data = {"pids": pids, "groups_ids": groups_ids}
        with self.get_client() as client:
            return client.post(url=self.get_url("pids"), json=data)

    def remove(self, pids: List[str], groups_ids: List[int]) -> Response:
        data = {"pids": pids, "groups_ids": groups_ids}
        with self.get_client() as client:
            return client.request(
                "DELETE", url=self.get_url("pids"), json=data
            )


class ImplAsync(APIBaseAsync, GroupsBase):
    async def create(self, name: str) -> Response:
        data = {"name": name}
        async with self.get_client() as client:
            return await client.post(url=self.get_url(), json=data)

    async def list(
        self,
        q: Union[str, object] = sentinel,
        pids_include: Union[List[str], object] = sentinel,
        pids_exclude: Union[List[str], object] = sentinel,
        groups_ids: Union[List[int], object] = sentinel,
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

    async def update(self, id: int, name: str) -> Response:
        data = {"name": name}
        async with self.get_client() as client:
            return await client.patch(url=self.get_url(f"{id}"), json=data)

    async def delete(self, id: int) -> Response:
        async with self.get_client() as client:
            return await client.delete(url=self.get_url(f"{id}"))

    async def persons(
        self,
        id: int,
        pids: Union[List[str], object] = sentinel,
        limit: int = 20,
        offset: int = 0,
    ) -> Response:
        data = request_query_processing(locals(), ["self", "id"])
        async with self.get_client() as client:
            return await client.get(
                url=self.get_url(f"{id}/pids"), params=data
            )

    async def add(self, pids: List[str], groups_ids: List[int]) -> Response:
        data = {"pids": pids, "groups_ids": groups_ids}
        async with self.get_client() as client:
            return await client.post(url=self.get_url("pids"), json=data)

    async def remove(self, pids: List[str], groups_ids: List[int]) -> Response:
        data = {"pids": pids, "groups_ids": groups_ids}
        async with self.get_client() as client:
            return await client.request(
                "DELETE", url=self.get_url("pids"), json=data
            )
