from httpx import Response

from neuroio.base import IAMBase, IAMBaseAsync, IAMBaseBase


class ListsSpacesBase(IAMBaseBase):
    def get_url(self) -> str:
        return self.base_url + "/v1/lists/spaces/"


class Impl(IAMBase, ListsSpacesBase):
    def all(self) -> Response:
        with self.get_client() as client:
            return client.get(url=self.get_url())


class ImplAsync(IAMBaseAsync, ListsSpacesBase):
    async def all(self) -> Response:
        async with self.get_client() as client:
            return await client.get(url=self.get_url())
