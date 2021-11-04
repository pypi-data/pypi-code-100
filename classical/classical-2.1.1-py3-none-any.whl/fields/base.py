import abc
from typing import Any, Dict, Generic, List, NoReturn, TypeVar


class ClassField:
    """
    Representation of a data field.
    """

    __slots__ = ('init_name', 'attr_name')

    def __init__(self, init_name: str, attr_name: str):
        # self.init_name = init_name
        super().__setattr__('init_name', init_name)
        # self.attr_name = attr_name
        super().__setattr__('attr_name', attr_name)

    def __hash__(self) -> int:
        return hash((self.init_name, self.attr_name))

    def __setattr__(self, key, value) -> None:
        raise AttributeError

    def __eq__(self, other) -> bool:
        if isinstance(other, ClassField):
            return self.init_name == other.init_name and self.attr_name == other.attr_name
        return False

    @property
    def name(self) -> str:
        """
        Name of the field (attribute name, may be different from the init name).
        """
        return self.attr_name

    def get_value(self, obj: Any) -> Any:
        """
        Get value of object's field.

        :param obj: source object
        :return: value of field

        ::

            import attr

            class FieldedNT(NamedTuple):
                size: int
                color: str

            @attr.s
            class FieldedAttrs:
                size: int = attr.ib()
                color: str = attr.ib()

            field_size = ClassField(init_name='size', attr_name='size')
            nt_obj = FieldedNT(size=12, color='red')
            attrs_obj = FieldedAttrs(size=34, color='green')

            # via get_value method
            field_size.get_value(nt_obj)  # == 12
            # via __getitem__
            field_size[attrs_obj]  # == 34

        """
        try:
            return getattr(obj, self.attr_name)
        except AttributeError:
            if isinstance(obj, dict):
                return obj[self.attr_name]
            raise

    def set_value(self, obj: Any, value: Any) -> None:
        """
        Set value for object's field.

        :param obj: target object
        :param value: value for field
        :return: ``None``

        ::

            import attr

            @attr.s
            class FieldedAttrs:
                size: int = attr.ib()
                color: str = attr.ib()

            field_size = ClassField(init_name='size', attr_name='size')
            field_color = ClassField(init_name='color', attr_name='color')
            attrs_obj = FieldedAttrs(size=56, color='green')

            # via get_value method
            field_size.set_value(attrs_obj, 78)  # attrs_obj.size == 78
            # via __getitem__
            field_color[attrs_obj] = 'blue'  # attrs_obj.color == 'blue'

        """
        try:
            setattr(obj, self.attr_name, value)
        except AttributeError:
            if isinstance(obj, dict):
                obj[self.attr_name] = value
            raise

    def __getitem__(self, obj: Any) -> Any:
        """
        Alias for :func:`~classical.fields.base.ClassField.get_value`
        """
        return self.get_value(obj=obj)

    def __setitem__(self, obj: Any, value: Any) -> None:
        """
        Alias for :func:`~classical.fields.base.ClassField.set_value`
        """
        self.set_value(obj=obj, value=value)


_ClassFieldType = TypeVar('_ClassFieldType', bound='ClassField')


class FieldSchema(List[_ClassFieldType]):
    def get_field_dict(self, obj: Any) -> Dict[_ClassFieldType, Any]:
        result = {}  # type: Dict[_ClassFieldType, Any]
        for field in self:
            result[field] = field[obj]
        return result

    def set_field_dict(self, obj: Any, values: Dict[_ClassFieldType, Any]) -> None:
        for field in self:
            if field in values:
                field[obj] = values[field]

    def __getitem__(self, obj: Any) -> Dict[_ClassFieldType, Any]:
        return self.get_field_dict(obj=obj)

    def __setitem__(self, obj: Any, values: Dict[_ClassFieldType, Any]) -> None:
        self.set_field_dict(obj=obj, values=values)


class FieldInspector(abc.ABC, Generic[_ClassFieldType]):
    @classmethod
    def _raise_unsupported_field_class(cls, insp_cls: type) -> NoReturn:
        raise TypeError(
            'Unsupported class {insp_cls.__name__} for {cls.__name__}'.format(
                insp_cls=insp_cls, cls=cls,
            )
        )

    @classmethod
    def get_fields(cls, cls_or_obj: type) -> FieldSchema[_ClassFieldType]:
        """
        Return list of fields for the given fielded class or object.

        :param cls_or_obj: class or instance to inspect.
        :return: list of :class:`~classical.fielded.base.ClassField` instances
        """
        if isinstance(cls_or_obj, type):
            return cls._get_class_fields(cls_or_obj)
        return cls._get_instance_fields(cls_or_obj)

    @classmethod
    @abc.abstractmethod
    def _get_class_fields(cls, insp_cls: type) -> FieldSchema[_ClassFieldType]:
        raise NotImplementedError

    @classmethod
    def _get_instance_fields(cls, obj: Any) -> FieldSchema[_ClassFieldType]:
        return cls._get_class_fields(type(obj))

    @classmethod
    def get_field_dict(cls, obj: Any) -> Dict[_ClassFieldType, Any]:
        """
        Return dict of ``obj``'s fields and their values

        :param obj: fielded instance
        :return: dict with :class:`~classical.fielded.base.ClassField` instances
            as keys
        """
        field_schema = cls._get_instance_fields(obj)
        return field_schema[obj]

    @classmethod
    def get_name_dict(
            cls, obj: Any,
            attr_mode: bool = False,
            init_mode: bool = False,
    ) -> Dict[str, Any]:
        """
        Return dict of ``obj``'s field names and their values.

        :param obj: fielded instance
        :param attr_mode: use fields' ``attr_name`` as the dict's keys;
            mutually exclusive with ``init_mode``
        :param init_mode: use fields' ``init_name`` as the dict's keys;
            mutually exclusive with ``attr_mode``
        :return: dict with :class:`~classical.fielded.base.ClassField` instances
            as keys
        """
        if attr_mode is False and init_mode is False:
            attr_mode = True
        if attr_mode is True and init_mode is True:
            raise ValueError('attr_mode and init_mode cannot both be True')

        result = {}  # type: Dict[str, Any]
        for field in cls._get_instance_fields(obj):
            key = field.attr_name if attr_mode else field.init_name
            result[key] = field[obj]
        return result

    @classmethod
    def get_name_list(
            cls, obj: Any,
            attr_mode: bool = False,
            init_mode: bool = False,
    ) -> List[str]:
        """
        Return list of ``obj``'s field names.

        :param obj: fielded instance
        :param attr_mode: use fields' ``attr_name``;
            mutually exclusive with ``init_mode``
        :param init_mode: use fields' ``init_name``;
            mutually exclusive with ``attr_mode``
        :return: dict with :class:`~classical.fielded.base.ClassField` instances
            as keys
        """
        if attr_mode is False and init_mode is False:
            attr_mode = True
        if attr_mode is True and init_mode is True:
            raise ValueError('attr_mode and init_mode cannot both be True')

        result = []  # type: List[str]
        for field in cls._get_instance_fields(obj):
            key = field.attr_name if attr_mode else field.init_name
            result.append(key)
        return result
