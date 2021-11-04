try:
    # New in Python 3.7
    import dataclasses
except ImportError:
    dataclasses = None

from classical.fields.base import ClassField, FieldInspector, FieldSchema


if dataclasses is not None:

    class DataclassFieldInspector(FieldInspector[ClassField]):
        @classmethod
        def _validate_cls(cls, insp_cls: type) -> None:
            if not dataclasses.is_dataclass(insp_cls):
                cls._raise_unsupported_field_class(insp_cls=insp_cls)

        @classmethod
        def _get_class_fields(cls, insp_cls: type) -> FieldSchema[ClassField]:
            cls._validate_cls(insp_cls)
            result = FieldSchema()
            for field in dataclasses.fields(insp_cls):  # noqa
                init_name = field.name.lstrip("_")
                result.append(ClassField(init_name=init_name, attr_name=field.name))
            return result

else:
    DataclassFieldInspector = None
