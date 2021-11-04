import sqlalchemy.orm
import sqlalchemy.orm.util
import sqlalchemy.exc

from classical.fields.base import ClassField, FieldInspector, FieldSchema


class SQLAlchemyModelFieldInspector(FieldInspector[ClassField]):
    @classmethod
    def _validate_cls(cls, insp_cls: type) -> None:
        try:
            sqlalchemy.orm.util.class_mapper(insp_cls)
        except sqlalchemy.orm.exc.UnmappedClassError:
            cls._raise_unsupported_field_class(insp_cls=insp_cls)

    @classmethod
    def _get_class_fields(cls, insp_cls: type) -> FieldSchema[ClassField]:
        cls._validate_cls(insp_cls)
        result = FieldSchema()
        for name in insp_cls.__mapper__.attrs.keys():  # noqa
            result.append(ClassField(init_name=name, attr_name=name))
        return result
