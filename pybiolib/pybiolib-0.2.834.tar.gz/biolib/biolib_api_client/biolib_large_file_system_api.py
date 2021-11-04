import requests

from biolib.biolib_api_client.auth import BearerAuth
from biolib.biolib_api_client import BiolibApiClient
from biolib.biolib_api_client.lfs_types import LfsVersionPresignedUploadUrlResponse, LfsUploadPartMetadata, \
    LargeFileSystemVersion, LargeFileSystem
from biolib.biolib_errors import BioLibError
from biolib.typing_utils import List


class BiolibLargeFileSystemApi:

    @staticmethod
    def create(account_uuid: str, name: str) -> LargeFileSystem:
        response = requests.post(
            f'{BiolibApiClient.get().base_url}/api/lfs/',
            auth=BearerAuth(BiolibApiClient.get().access_token),
            timeout=5,
            json={'account_uuid': account_uuid, 'name': name}
        )

        if not response.ok:
            raise BioLibError(response.content.decode())

        lfs: LargeFileSystem = response.json()
        return lfs

    @staticmethod
    def create_version(resource_uuid: str) -> LargeFileSystemVersion:
        response = requests.post(
            f'{BiolibApiClient.get().base_url}/api/lfs/versions/',
            auth=BearerAuth(BiolibApiClient.get().access_token),
            json={'resource_uuid': resource_uuid},
            timeout=5,
        )

        if not response.ok:
            raise BioLibError(response.content.decode())

        lfs_version: LargeFileSystemVersion = response.json()
        return lfs_version

    @staticmethod
    def get_upload_url(resource_version_uuid: str, part_number: int) -> LfsVersionPresignedUploadUrlResponse:
        response = requests.get(
            f'{BiolibApiClient.get().base_url}/api/lfs/versions/{resource_version_uuid}/presigned_upload_url/',
            auth=BearerAuth(BiolibApiClient.get().access_token),
            params={'part_number': part_number},
            timeout=5,
        )

        if not response.ok:
            raise BioLibError(response.content.decode())

        presigned_upload_url_response: LfsVersionPresignedUploadUrlResponse = response.json()
        return presigned_upload_url_response

    @staticmethod
    def complete_upload(
            resource_version_uuid: str,
            parts: List[LfsUploadPartMetadata],
            size_bytes: int,
    ) -> None:
        response = requests.post(
            f'{BiolibApiClient.get().base_url}/api/lfs/versions/{resource_version_uuid}/complete_upload/',
            auth=BearerAuth(BiolibApiClient.get().access_token),
            json={'parts': parts, 'size_bytes': size_bytes},
            timeout=5,
        )

        if not response.ok:
            raise BioLibError(response.content.decode())
