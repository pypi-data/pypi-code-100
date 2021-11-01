import enum
import hashlib
import lzma
from dataclasses import dataclass
from string import Template
from typing import Optional, Callable


class APIEnv(enum.Enum):
    local = 'local'
    dev = 'dev'
    release = 'release'


@dataclass
class Env:
    api_url: str
    chunk_url_template: Template
    chunk_bucket_name: str = 'cdn.dev.vankrupt.io'
    upload_bucket_name: Optional[str] = None
    modprocessing_url: Optional[str] = None

    decompress_func: Callable = lzma.decompress
    hash_func: Callable = hashlib.sha3_256


_env_map = {
    APIEnv.local: Env(
        api_url='http://localhost:8000',
        chunk_url_template=Template('http://localhost:8081/storage/v1/b/cdn.dev.vankrupt.io/o/$mod_id/$hash'),
        modprocessing_url='http://localhost:9000/uploaded',
        upload_bucket_name='upload.dev.vankrupt.io',
    ),
    APIEnv.dev: Env(
        api_url='https://api.dev.vankrupt.io/',
        chunk_url_template=Template('https://storage.googleapis.com/cdn.dev.vankrupt.io/$mod_id/$hash')
    ),
    APIEnv.release: Env(
        api_url='https://api.vankrupt.io/',
        chunk_url_template=Template('https://storage.googleapis.com/cdn.dev.vankrupt.io/$mod_id/$hash')
    ),
}
