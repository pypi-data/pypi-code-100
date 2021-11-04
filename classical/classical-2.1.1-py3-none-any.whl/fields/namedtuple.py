from classical.fields.base import ClassField, FieldInspector, FieldSchema


class NamedTupleFieldInspector(FieldInspector[ClassField]):
    @classmethod
    def _validate_cls(cls, insp_cls: type) -> None:
        if not (issubclass(insp_cls, tuple) and hasattr(insp_cls, '_fields')):
            cls._raise_unsupported_field_class(insp_cls=insp_cls)

    @classmethod
    def _get_class_fields(cls, insp_cls: type) -> FieldSchema[ClassField]:
        cls._validate_cls(insp_cls)
        result = FieldSchema()
        for name in insp_cls._fields:  # noqa
            result.append(ClassField(init_name=name, attr_name=name))
        return result
