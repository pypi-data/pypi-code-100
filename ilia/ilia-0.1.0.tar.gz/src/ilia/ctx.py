from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from typing import TYPE_CHECKING, Any, Callable, Iterator

from .ref import push_fragments

if TYPE_CHECKING:
    from types import NotImplementedType

    from .evaluators import Evaluate
    from .reg import Registry
    from .res import Document

    relative_location: str
    formats: dict[str, Callable[[Any], bool | NotImplementedType]]

reg_var: ContextVar[Registry] = ContextVar("reg_var")
relative_location_var: ContextVar[str] = ContextVar("relative_location_var", default="")


def find(doc: Document, key: str) -> Document | None:
    return reg_var.get().find(doc, key)


def find_sequence(doc: Document, key: str) -> list[tuple[int, Document]] | None:
    return reg_var.get().find_sequence(doc, key)


def find_mapping(doc: Document, key: str) -> list[tuple[str, Document]] | None:
    return reg_var.get().find_mapping(doc, key)


def compile_schema(doc: Document) -> Evaluate:
    return reg_var.get().compile_schema(doc)


@contextmanager
def push_relative_location(*fragments: int | str) -> Iterator[str]:
    relative_location = push_fragments(relative_location_var.get(), *fragments)
    try:
        token = relative_location_var.set(relative_location)
        yield relative_location
    finally:
        relative_location_var.reset(token)


@contextmanager
def push_registry(reg: Registry):
    try:
        token = reg_var.set(reg)
        yield
    finally:
        reg_var.reset(token)


def __getattr__(name):
    if name == "relative_location":
        return relative_location_var.get()
    if name == "formats":
        return reg_var.get().formats
    raise AttributeError
