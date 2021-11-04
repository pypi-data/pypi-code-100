from typing import Any

from classical.fields.base import ClassField, FieldInspector, FieldSchema


class DictFieldInspector(FieldInspector[ClassField]):
    @classmethod
    def _validate_cls(cls, insp_cls: type) -> None:
        if not (issubclass(insp_cls, dict)):
            cls._raise_unsupported_field_class(insp_cls=insp_cls)

    @classmethod
    def _get_class_fields(cls, insp_cls: type) -> FieldSchema[ClassField]:
        cls._validate_cls(insp_cls)
        result = FieldSchema()
        if hasattr(insp_cls, '__annotations__'):
            # TypedDict
            for name in insp_cls.__annotations__:  # noqa
                result.append(ClassField(init_name=name, attr_name=name))
        return result

    @classmethod
    def _get_instance_fields(cls, obj: Any) -> FieldSchema[ClassField]:
        return FieldSchema([
            ClassField(attr_name=name, init_name=name)
            for name in obj
        ])
