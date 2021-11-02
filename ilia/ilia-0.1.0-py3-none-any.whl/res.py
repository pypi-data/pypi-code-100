from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Deque, Generic, TypeAlias, TypeVar, Union

from .ref import Ref

if TYPE_CHECKING:
    from .reg import Registry

DEFAULT_DIALECT = "https://json-schema.org/draft/2020-12/schema"

DictSchema: TypeAlias = dict
BoolSchema: TypeAlias = bool
Schema = Union[DictSchema, BoolSchema]

T = TypeVar("T")
S = TypeVar("S", bound=Schema)


@dataclass(repr=False)
class Document(Generic[S]):
    schema: S
    dialect: str
    canonical_uri: str | None = None
    anchor: str | None = None
    relative_location: str = ""
    root: Document | None = None
    parent: Document | None = None
    ref: Ref | None = None
    ref_doc: Document | None = None

    def __post_init__(self):
        if self.relative_location and not self.root:
            raise Exception("relative location and root are mandatory")
        if not self.relative_location and self.root:
            raise Exception("relative location and root are mandatory")

    def __repr__(self):
        return (
            f"Document("
            f"canonical_uri={self.canonical_uri!r}, "
            f"anchor={self.anchor!r}, "
            f"relative_location={self.relative_location!r}, "
            f"ref={self.ref!r})"
        )

    @property
    def absolute_location(self):
        if self.canonical_uri:
            return self.canonical_uri
        if self.root:
            return (self.root.canonical_uri or "") + "#" + self.relative_location


def document_factory(
    schema: S,
    *,
    relative_location: str = "",
    root: Document = None,
    parent: Document = None,
    reg: Registry,
    default_dialect: str = DEFAULT_DIALECT,
) -> Document[S]:
    dialect = guess_dialect(schema, parent, default_dialect)
    doc = Document(
        schema=schema,
        relative_location=relative_location,
        root=root,
        parent=parent,
        dialect=dialect,
    )
    reg.finalize(doc)
    return doc


def guess_dialect(schema: dict | bool, parent: Document | None, default: str) -> str:
    if isinstance(schema, dict) and (dialect := schema.get("$schema")):
        return dialect
    elif parent and (dialect := parent.dialect):
        return dialect
    return default


def canonical_uri_join(base: str, canonical_uri: str) -> str:
    from urllib.parse import urljoin

    if base.startswith(("http://", "https://")):
        return urljoin(base, canonical_uri, allow_fragments=False)
    return canonical_uri


def canonical_ref_join(base: str, ref: str) -> str:
    from urllib.parse import urljoin

    if base.startswith(("http://", "https://")):
        base, *_ = base.partition("#")
        ref = urljoin(base, ref, allow_fragments=True)
    if "#" not in ref:
        ref = ref + "#"
    return ref


def resolve(schema: S, *, reg: Registry, default_dialect: str = None) -> Document[S]:
    default_dialect = default_dialect or DEFAULT_DIALECT
    doc = document_factory(schema, default_dialect=default_dialect, reg=reg)
    resolve_2(doc, reg)
    return doc


def resolve_2(doc: Document, reg: Registry):
    from collections import deque

    queue1: Deque[Document] = deque([doc])  # explore down
    queue2: Deque[Document] = deque([])  # check for $refs
    while queue1 or queue2:
        while queue1:
            doc = queue1.popleft()
            reg.documents.append(doc)
            for schema, relative_location in reg.extract(doc):
                queue1.append(
                    document_factory(
                        schema=schema,
                        relative_location=relative_location,
                        root=doc.root or doc,
                        parent=doc,
                        reg=reg,
                    )
                )
            queue2.append(doc)
        while queue2:
            doc = queue2.popleft()
            if doc.ref:
                if ref_doc := find_by_ref(reg, doc):
                    doc.ref_doc = ref_doc
                else:
                    schema, *_ = reg.load(doc.ref)
                    queue2.append(doc)
                    doc = document_factory(schema, reg=reg)
                    queue1.append(doc)
                    # doc.ref_doc = reg.load(ref)
                    raise NotImplementedError(
                        "Need to grab from outher space", reg.documents
                    )

            # raise NotImplementedError
        continue


def find_by_ref(reg: Registry, doc: Document):
    if doc.ref is None:
        raise
    uri, pointer, anchor = doc.ref.decomposed
    relative_location = pointer or ""
    if uri:
        documents = list(d for d in reg.documents if d.canonical_uri == uri)
    elif root := doc.root:
        documents = [d for d in reg.documents if d.root == root] + [root]
    elif doc.relative_location == "":
        documents = [d for d in reg.documents if d.root == doc] + [doc]
    else:
        raise
    if anchor:
        for document in reg.documents:
            if document.anchor == anchor:
                return document
    else:
        for document in documents:
            if document.relative_location == relative_location:
                return document
