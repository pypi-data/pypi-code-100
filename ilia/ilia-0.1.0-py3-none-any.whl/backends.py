from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urljoin

import httpx


class Backend:
    def applicable(self, document_uri: str) -> bool:
        ...

    def get(self, document_uri: str) -> tuple[dict, str]:
        ...


class BackendError(Exception):
    pass


class FileSystemBackend(Backend):
    def __init__(self, dirname: Path, prefix: str = ""):
        self.dirname = dirname
        self.prefix = prefix

    def applicable(self, document_uri: str) -> bool:
        return document_uri.startswith(self.prefix)

    def get(self, document_uri: str) -> tuple[dict, str]:
        uri, *_ = document_uri.partition("#")
        path = self.dirname / (uri.removeprefix(self.prefix) + ".json")
        try:
            return json.loads(path.read_text()), uri
        except FileNotFoundError as error:
            raise BackendError(f"unable to load {document_uri}") from error


class HTTPBackend(Backend):
    def __init__(self, base_url: str, prefix: str = ""):
        self.base_url = base_url
        self.prefix = prefix

    def applicable(self, document_uri: str) -> bool:
        return document_uri.startswith(self.prefix)

    def get(self, document_uri: str) -> tuple[dict, str]:
        uri, *_ = document_uri.partition("#")
        url = urljoin(self.base_url, uri.removeprefix(self.prefix))
        try:
            response = httpx.get(url)
            response.raise_for_status()
            return json.loads(response.text), uri
        except httpx.HTTPStatusError as error:
            raise BackendError(f"unable to load {document_uri}") from error
