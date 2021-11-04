from classical.fields.base import ClassField, FieldInspector, FieldSchema


class AttrsFieldInspector(FieldInspector[ClassField]):
    @classmethod
    def _validate_cls(cls, insp_cls: type) -> None:
        attrs = getattr(insp_cls, "__attrs_attrs__", None)
        if attrs is None:
            cls._raise_unsupported_field_class(insp_cls=insp_cls)

    @classmethod
    def _get_class_fields(cls, insp_cls: type) -> FieldSchema[ClassField]:
        cls._validate_cls(insp_cls)
        result = FieldSchema()
        for field in insp_cls.__attrs_attrs__:  # noqa
            init_name = field.name.lstrip("_")  # same logic as attrs uses internally
            result.append(ClassField(init_name=init_name, attr_name=field.name))
        return result
