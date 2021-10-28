from typing import Union

from httpx import Response

from neuroio.base import APIBase, APIBaseAsync, APIBaseBase
from neuroio.constants import EntryResult, sentinel
from neuroio.utils import (
    ImageType,
    prepare_image_processing,
    request_dict_processing,
    request_form_processing,
)


class PersonsBase(APIBaseBase):
    def get_url(self, key: str = None) -> str:
        if key:
            return self.base_url + f"/v1/persons/{key}/"
        else:
            return self.base_url + "/v1/persons/"


class Impl(APIBase, PersonsBase):
    def create(
        self,
        image: ImageType,
        source: str,
        facesize: Union[int, object] = sentinel,
        create_on_ha: Union[bool, object] = sentinel,
        create_on_junk: Union[bool, object] = sentinel,
        identify_asm: Union[bool, object] = sentinel,
    ) -> Response:
        data = request_form_processing(locals(), ["self", "image"])
        files = prepare_image_processing(image)

        with self.get_client() as client:
            return client.post(url=self.get_url(), data=data, files=files)

    def create_by_entry(
        self, id: int, create_on_ha: bool, create_on_junk: bool
    ) -> Response:
        data = request_dict_processing(locals(), ["self"])

        with self.get_client() as client:
            return client.post(url=self.get_url("entry"), json=data)

    def reinit(self, id: int) -> Response:
        with self.get_client() as client:
            return client.post(url=self.get_url("reinit"), json={"id": id})

    def reinit_by_photo(
        self,
        pid: str,
        image: ImageType,
        source: str,
        facesize: Union[int, object] = sentinel,
        identify_asm: Union[bool, object] = sentinel,
        result: str = EntryResult.HA,
    ) -> Response:
        data = request_form_processing(locals())
        files = prepare_image_processing(image)

        with self.get_client() as client:
            return client.post(
                url=self.get_url(f"reinit/{pid}"), data=data, files=files
            )

    def search(
        self,
        image: ImageType,
        identify_asm: bool = False,
    ) -> Response:
        files = prepare_image_processing(image)
        data = {"identify_asm": str(identify_asm)}

        with self.get_client() as client:
            return client.post(
                url=self.get_url("search"), data=data, files=files
            )

    def delete(self, pid: str) -> Response:
        with self.get_client() as client:
            return client.delete(url=self.get_url(f"{pid}"))


class ImplAsync(APIBaseAsync, PersonsBase):
    async def create(
        self,
        image: ImageType,
        source: str,
        facesize: Union[int, object] = sentinel,
        create_on_ha: Union[bool, object] = sentinel,
        create_on_junk: Union[bool, object] = sentinel,
        identify_asm: Union[bool, object] = sentinel,
    ) -> Response:
        data = request_form_processing(locals(), ["self", "image"])
        files = prepare_image_processing(image)

        async with self.get_client() as client:
            return await client.post(
                url=self.get_url(), data=data, files=files
            )

    async def create_by_entry(
        self, id: int, create_on_ha: bool, create_on_junk: bool
    ) -> Response:
        data = request_dict_processing(locals(), ["self"])

        async with self.get_client() as client:
            return await client.post(url=self.get_url("entry"), json=data)

    async def reinit(self, id: int) -> Response:
        async with self.get_client() as client:
            return await client.post(
                url=self.get_url("reinit"), json={"id": id}
            )

    async def reinit_by_photo(
        self,
        pid: str,
        image: ImageType,
        source: str,
        facesize: Union[int, object] = sentinel,
        identify_asm: Union[bool, object] = sentinel,
        result: str = EntryResult.HA,
    ) -> Response:
        data = request_form_processing(locals(), ["self", "image", "pid"])
        files = prepare_image_processing(image)

        async with self.get_client() as client:
            return await client.post(
                url=self.get_url(f"reinit/{pid}"), data=data, files=files
            )

    async def search(
        self,
        image: ImageType,
        identify_asm: bool = False,
    ) -> Response:
        files = prepare_image_processing(image)
        data = {"identify_asm": str(identify_asm)}

        async with self.get_client() as client:
            return await client.post(
                url=self.get_url("search"), data=data, files=files
            )

    async def delete(self, pid: str) -> Response:
        async with self.get_client() as client:
            return await client.delete(url=self.get_url(f"{pid}"))
