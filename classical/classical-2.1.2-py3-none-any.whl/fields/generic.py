from typing import Any, Optional, Type

from classical.fields.base import ClassField, FieldInspector, FieldSchema
from classical.fields.namedtuple import NamedTupleFieldInspector
from classical.fields.dict import DictFieldInspector
from classical.fields.attrs import AttrsFieldInspector
from classical.fields.dataclass import DataclassFieldInspector

try:
    from classical.fields.schematics import SchematicsFieldInspector
except ImportError:
    SchematicsFieldInspector = None

try:
    from classical.fields.sqlalchemy import SQLAlchemyModelFieldInspector
except ImportError:
    SQLAlchemyModelFieldInspector = None


INSPECTOR_REGISTRY = [
    cls for cls in (
        NamedTupleFieldInspector,
        DictFieldInspector,
        AttrsFieldInspector,
        DataclassFieldInspector,
        SchematicsFieldInspector,
        SQLAlchemyModelFieldInspector,
    ) if cls is not None
]


class GenericFieldInspector(FieldInspector[ClassField]):
    @classmethod
    def _resolve_specific_inspector_cls(cls, insp_cls: type) -> Optional[Type[FieldInspector]]:
        for inspector_cls in INSPECTOR_REGISTRY:
            try:
                inspector_cls._validate_cls(insp_cls)
                return inspector_cls
            except TypeError:
                pass

        return None

    @classmethod
    def _validate_cls(cls, insp_cls: type) -> None:
        inspector_cls = cls._resolve_specific_inspector_cls(insp_cls)
        if inspector_cls is None:
            cls._raise_unsupported_field_class(insp_cls=insp_cls)

    @classmethod
    def _get_class_fields(cls, insp_cls: type) -> FieldSchema[ClassField]:
        inspector_cls = cls._resolve_specific_inspector_cls(insp_cls)
        if inspector_cls is None:
            cls._raise_unsupported_field_class(insp_cls=insp_cls)
        return inspector_cls._get_class_fields(insp_cls=insp_cls)

    @classmethod
    def _get_instance_fields(cls, obj: Any) -> FieldSchema[ClassField]:
        inspector_cls = cls._resolve_specific_inspector_cls(type(obj))
        if inspector_cls is None:
            cls._raise_unsupported_field_class(insp_cls=type(obj))
        return inspector_cls._get_instance_fields(obj=obj)
