from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Generic, Iterable, TypeVar

from .ref import push_fragments

if TYPE_CHECKING:
    from .evaluators import Evaluate
    from .loaders import Loader
    from .res import Document, Schema

T = TypeVar("T")


def registry_factory() -> Registry:
    from ilia.dialects import draft202021

    from .loaders import Loader

    extractor: MultiMethod[Iterable[tuple[dict | bool, str]]] = MultiMethod()
    extractor.register(draft202021.DIALECT, draft202021.extract)

    finalizer: MultiMethod[Document] = MultiMethod()
    finalizer.register(draft202021.DIALECT, draft202021.finalize)

    schema_compiler: MultiMethod[Evaluate] = MultiMethod()
    schema_compiler.register(draft202021.DIALECT, draft202021.compile_schema)

    loader = Loader([])
    return Registry(
        finalizer=finalizer,
        extractor=extractor,
        schema_compiler=schema_compiler,  # type:ignore
        loader=loader,
    )


class Registry:
    formats: dict

    def __init__(
        self,
        finalizer: Callable[[Document], None],
        extractor: Callable[[Document], Iterable[Document]],
        schema_compiler: Callable[[Document], Evaluate],
        loader: Loader = None,
    ):
        self.documents: list[Document] = []
        self.finalizer = finalizer
        self.extractor = extractor
        self.schema_compiler = schema_compiler
        self.formats = {}
        self.loader = loader

    def load(self, uri: str) -> tuple[Schema, str]:
        if self.loader:
            return self.loader.get(uri)
        raise

    def finalize(self, doc: Document):
        return self.finalizer(doc)

    def extract(self, doc: Document):
        return self.extractor(doc)

    def compile_schema(self, doc: Document):
        return self.schema_compiler(doc)

    def find(self, parent: Document, key: str) -> Document | None:
        relative_location = push_fragments(parent.relative_location, key)
        for doc in self.documents:
            if doc.parent is parent and doc.relative_location == relative_location:
                return doc
        return None

    def find_sequence(
        self, parent: Document[dict], key: str
    ) -> list[tuple[int, Document]] | None:
        z: list[Any] | None
        if (z := parent.schema.get(key)) is not None:
            sequence = []
            for index, _ in enumerate(z):
                relative_location = push_fragments(parent.relative_location, key, index)
                for doc in self.documents:
                    if (
                        doc.parent is parent
                        and doc.relative_location == relative_location
                    ):
                        sequence.append((index, doc))
                        break
                else:
                    raise
            return sequence
        return None

    def find_mapping(
        self, parent: Document[dict], key: str
    ) -> list[tuple[str, Document]] | None:
        z: dict[str, Any] | None
        if (z := parent.schema.get(key)) is not None:
            sequence = []
            for index in z:
                relative_location = push_fragments(parent.relative_location, key, index)
                for doc in self.documents:
                    if (
                        doc.parent is parent
                        and doc.relative_location == relative_location
                    ):
                        sequence.append((index, doc))
                        break
                else:
                    raise
            return sequence
        return None


class MultiMethod(Generic[T]):
    def __init__(self):
        self.methods: dict[str, Callable[[Document], T]] = {}

    def __call__(self, doc: Document):
        return self[doc.dialect](doc)

    def __getitem__(self, dialect):
        return self.methods[dialect]

    def register(self, dialect: str, func: Callable[[Document], T] = None):
        def inner(func: Callable[[Document], T]):
            self.methods[dialect] = func
            return func

        if func:
            return inner(func)
        return inner
