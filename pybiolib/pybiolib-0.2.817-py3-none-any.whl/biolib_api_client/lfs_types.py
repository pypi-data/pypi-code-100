from biolib.typing_utils import TypedDict


class LargeFileSystemVersion(TypedDict):
    uri: str
    uuid: str


class LargeFileSystem(TypedDict):
    uri: str
    uuid: str


class LfsVersionPresignedUploadUrlResponse(TypedDict):
    presigned_upload_url: str


class LfsUploadPartMetadata(TypedDict):
    PartNumber: int
    ETag: str
