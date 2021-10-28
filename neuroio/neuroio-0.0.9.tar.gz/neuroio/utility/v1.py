from typing.io import BinaryIO

from httpx import Response

from neuroio.base import APIBase, APIBaseAsync, APIBaseBase
from neuroio.constants import EntryResult


class UtilityBase(APIBaseBase):
    def get_url(self, key: str) -> str:
        return self.base_url + f"/v1/utility/{key}/"


class Impl(APIBase, UtilityBase):
    def compare(
        self, image1: BinaryIO, image2: BinaryIO, result: str = EntryResult.HA
    ) -> Response:
        files = {"image1": image1, "image2": image2}
        data = {"result": result}

        with self.get_client() as client:
            return client.post(
                url=self.get_url("compare"), data=data, files=files
            )

    def asm(self, image: BinaryIO) -> Response:
        files = {"image": image}

        with self.get_client() as client:
            return client.post(url=self.get_url("asm"), files=files)


class ImplAsync(APIBaseAsync, UtilityBase):
    async def compare(
        self, image1: BinaryIO, image2: BinaryIO, result: str = EntryResult.HA
    ) -> Response:
        files = {"image1": image1, "image2": image2}
        data = {"result": result}

        async with self.get_client() as client:
            return await client.post(
                url=self.get_url("compare"), data=data, files=files
            )

    async def asm(self, image: BinaryIO) -> Response:
        files = {"image": image}

        async with self.get_client() as client:
            return await client.post(url=self.get_url("asm"), files=files)
