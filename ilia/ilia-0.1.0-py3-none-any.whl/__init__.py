from __future__ import annotations

from .reg import Registry, registry_factory
from .res import Document, Schema, resolve
from .validators import Validator
from . import ctx

__all__ = [
    "Document",
    "Registry",
    "registry_factory",
    "resolve",
]


def load(schema: Schema, reg: Registry = None):
    reg = reg or registry_factory()
    with ctx.push_registry(reg):
        doc = resolve(schema, reg=reg)
        evaluator = reg.compile_schema(doc)
        return Validator(doc, evaluator)
