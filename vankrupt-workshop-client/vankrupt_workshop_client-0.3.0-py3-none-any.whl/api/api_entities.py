import enum
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, TypeVar, Generic


class GamingPlatform(str, enum.Enum):
    linux = 'linux'
    windows = 'windows'
    android = 'android'
    ps5 = 'ps5'


@dataclass
class Chunk:
    id: int
    true_size_bytes: int
    storage_used_bytes: int
    custom_hash: str
    created_at: str


@dataclass
class SequencedChunk:
    chunk_sequence: int
    chunk: Chunk


@dataclass
class ModFileUploadRequest:
    platform: str
    update_message: str
    size: int


@dataclass
class ModFileUploadResponse:
    platform: str
    update_message: str
    size: int
    id: int
    user_id: int
    signed_policy: dict
    mod_file_id: int
    status: str
    error_message: Optional[str]
    created_at: str


@dataclass
class _ModFile:
    platform: 'GamingPlatform'
    version: int
    true_size_bytes: int
    storage_used_bytes: int
    file_md5_hash: str
    created_at: str


@dataclass
class ModFileList(_ModFile):
    ...


@dataclass
class ModFileDownload(_ModFile):
    chunks: List['SequencedChunk']


@dataclass
class ModCreate:
    name: str
    description: str


@dataclass
class ModBase:
    name: str
    description: str
    creator_id: int
    id: int
    created_at: str


@dataclass
class ModList(ModBase):
    ...


@dataclass
class ModInspect(ModBase):
    files: List['ModFileList']


@dataclass
class ModDownload(ModBase):
    files: List['ModFileDownload']


@dataclass
class User:
    name: str
    email: str
    id: int
    is_active: bool
    email_verified: bool


T = TypeVar('T')


@dataclass
class Page(Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
