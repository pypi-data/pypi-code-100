from typing import List, Optional, Union

from httpx import Response

from neuroio.base import APIBase, APIBaseAsync, APIBaseBase
from neuroio.constants import sentinel
from neuroio.utils import request_dict_processing, request_query_processing


class SourcesBase(APIBaseBase):
    def get_url(self, key: str = None) -> str:
        if key:
            return self.base_url + f"/v1/sources/{key}/"
        else:
            return self.base_url + "/v1/sources/"


class Impl(APIBase, SourcesBase):
    def create(
        self,
        name: str,
        license_id: Optional[Union[str, object]] = sentinel,
        identify_facesize_threshold: int = 7000,
        use_pps_time: bool = False,
        manual_create_facesize_threshold: int = 25000,
        manual_create_on_ha: bool = False,
        manual_create_on_junk: bool = False,
        manual_identify_asm: bool = True,
        auto_create_persons: bool = False,
        auto_create_facesize_threshold: int = 25000,
        auto_create_check_blur: bool = True,
        auto_create_check_exposure: bool = True,
        auto_create_on_ha: bool = False,
        auto_create_on_junk: bool = False,
        auto_check_face_angle: bool = True,
        auto_check_liveness: bool = False,
        auto_create_liveness_only: bool = True,
        auto_identify_asm: bool = True,
        store_images_for_results: Union[
            Optional[List[str]], object
        ] = sentinel,
    ) -> Response:
        data = request_dict_processing(locals(), ["self"])

        with self.get_client() as client:
            return client.post(url=self.get_url(), json=data)

    def list(
        self,
        q: str = None,
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
        name: Optional[Union[str, object]] = sentinel,
        license_id: Optional[Union[str, object]] = sentinel,
        identify_facesize_threshold: Union[int, object] = sentinel,
        use_pps_time: Union[bool, object] = sentinel,
        manual_create_facesize_threshold: Union[int, object] = sentinel,
        manual_create_on_ha: Union[bool, object] = sentinel,
        manual_create_on_junk: Union[bool, object] = sentinel,
        manual_identify_asm: Union[bool, object] = sentinel,
        auto_create_persons: Union[bool, object] = sentinel,
        auto_create_facesize_threshold: Union[int, object] = sentinel,
        auto_create_check_blur: Union[bool, object] = sentinel,
        auto_create_check_exposure: Union[bool, object] = sentinel,
        auto_create_on_ha: Union[bool, object] = sentinel,
        auto_create_on_junk: Union[bool, object] = sentinel,
        auto_check_face_angle: Union[bool, object] = sentinel,
        auto_check_liveness: Union[bool, object] = sentinel,
        auto_create_liveness_only: Union[bool, object] = sentinel,
        auto_identify_asm: Union[bool, object] = sentinel,
        store_images_for_results: Union[List[str], object] = sentinel,
    ) -> Response:
        data = request_dict_processing(locals(), ["id", "self"])

        with self.get_client() as client:
            return client.patch(url=self.get_url(f"{id}"), json=data)

    def delete(self, id: int) -> Response:
        with self.get_client() as client:
            return client.delete(url=self.get_url(f"{id}"))


class ImplAsync(APIBaseAsync, SourcesBase):
    async def create(
        self,
        name: str,
        license_id: Optional[Union[str, object]] = sentinel,
        identify_facesize_threshold: int = 7000,
        use_pps_time: bool = False,
        manual_create_facesize_threshold: int = 25000,
        manual_create_on_ha: bool = False,
        manual_create_on_junk: bool = False,
        manual_identify_asm: bool = True,
        auto_create_persons: bool = False,
        auto_create_facesize_threshold: int = 25000,
        auto_create_check_blur: bool = True,
        auto_create_check_exposure: bool = True,
        auto_create_on_ha: bool = False,
        auto_create_on_junk: bool = False,
        auto_check_face_angle: bool = True,
        auto_check_liveness: bool = False,
        auto_create_liveness_only: bool = True,
        auto_identify_asm: bool = True,
        store_images_for_results: Union[
            Optional[List[str]], object
        ] = sentinel,
    ) -> Response:
        data = request_dict_processing(locals(), ["self"])

        async with self.get_client() as client:
            return await client.post(url=self.get_url(), json=data)

    async def list(
        self,
        q: str = None,
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
        name: Optional[Union[str, object]] = sentinel,
        license_id: Optional[Union[str, object]] = sentinel,
        identify_facesize_threshold: Union[int, object] = sentinel,
        use_pps_time: Union[bool, object] = sentinel,
        manual_create_facesize_threshold: Union[int, object] = sentinel,
        manual_create_on_ha: Union[bool, object] = sentinel,
        manual_create_on_junk: Union[bool, object] = sentinel,
        manual_identify_asm: Union[bool, object] = sentinel,
        auto_create_persons: Union[bool, object] = sentinel,
        auto_create_facesize_threshold: Union[int, object] = sentinel,
        auto_create_check_blur: Union[bool, object] = sentinel,
        auto_create_check_exposure: Union[bool, object] = sentinel,
        auto_create_on_ha: Union[bool, object] = sentinel,
        auto_create_on_junk: Union[bool, object] = sentinel,
        auto_check_face_angle: Union[bool, object] = sentinel,
        auto_check_liveness: Union[bool, object] = sentinel,
        auto_create_liveness_only: Union[bool, object] = sentinel,
        auto_identify_asm: Union[bool, object] = sentinel,
        store_images_for_results: Union[List[str], object] = sentinel,
    ) -> Response:
        data = request_dict_processing(locals(), ["id", "self"])

        async with self.get_client() as client:
            return await client.patch(url=self.get_url(f"{id}"), json=data)

    async def delete(self, id: int) -> Response:
        async with self.get_client() as client:
            return await client.delete(url=self.get_url(f"{id}"))
