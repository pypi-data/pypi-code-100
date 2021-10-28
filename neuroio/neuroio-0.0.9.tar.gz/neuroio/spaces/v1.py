from httpx import Response

from neuroio.base import IAMBase, IAMBaseAsync, IAMBaseBase


class SpacesBase(IAMBaseBase):
    def get_url(self, key: str = None) -> str:
        if key:
            return self.base_url + f"/v1/spaces/{key}/"
        else:
            return self.base_url + "/v1/spaces/"


class Impl(IAMBase, SpacesBase):
    def create(self, name: str) -> Response:
        data = {"name": name}

        with self.get_client() as client:
            return client.post(url=self.get_url(), json=data)

    def list(
        self, q: str = None, limit: int = 20, offset: int = 0
    ) -> Response:
        data = {"q": q, "limit": limit, "offset": offset}

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

    def token(self, id: int, permanent: bool = False) -> Response:
        data = {"permanent": permanent}

        with self.get_client() as client:
            return client.post(url=self.get_url(f"{id}/tokens"), json=data)


class ImplAsync(IAMBaseAsync, SpacesBase):
    async def create(self, name: str) -> Response:
        data = {"name": name}

        async with self.get_client() as client:
            return await client.post(url=self.get_url(), json=data)

    async def list(
        self, q: str = None, limit: int = 20, offset: int = 0
    ) -> Response:
        data = {"q": q, "limit": limit, "offset": offset}

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

    async def token(self, id: int, permanent: bool = False) -> Response:
        data = {"permanent": permanent}
        async with self.get_client() as client:
            return await client.post(
                url=self.get_url(f"{id}/tokens"), json=data
            )
