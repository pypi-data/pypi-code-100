from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from .backends import Backend
    from .res import Schema


class Loader:
    def __init__(self, backends: list[Backend]):
        self.backends = backends

    def get(self, uri: str):
        for backend in self.backends:
            if backend.applicable(uri):
                return backend.get(uri)
        raise
