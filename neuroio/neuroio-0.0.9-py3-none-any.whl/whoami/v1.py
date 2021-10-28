from httpx import Response

from neuroio.base import IAMBase, IAMBaseAsync, IAMBaseBase


class WhoamiBase(IAMBaseBase):
    def get_url(self) -> str:
        return self.base_url + "/v1/whoami/"


class Impl(IAMBase, WhoamiBase):
    def me(self) -> Response:
        with self.get_client() as client:
            return client.get(url=self.get_url())


class ImplAsync(IAMBaseAsync, WhoamiBase):
    async def me(self) -> Response:
        async with self.get_client() as client:
            return await client.get(url=self.get_url())
