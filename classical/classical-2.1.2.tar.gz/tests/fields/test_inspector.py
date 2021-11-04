from collections import namedtuple
from typing import Any, ClassVar, Dict, List, NamedTuple, Optional, Tuple, Type

try:
    # New in Python 3.7
    import dataclasses
except ImportError:
    dataclasses = None

try:
    # New in Python 3.8
    from typing import TypedDict
except ImportError:
    TypedDict = None


from unittest import TestCase

import attr
import schematics
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

from classical.fields.base import FieldInspector, ClassField
from classical.fields.namedtuple import NamedTupleFieldInspector
from classical.fields.dict import DictFieldInspector
from classical.fields.attrs import AttrsFieldInspector
from classical.fields.dataclass import DataclassFieldInspector
from classical.fields.schematics import SchematicsFieldInspector
from classical.fields.sqlalchemy import SQLAlchemyModelFieldInspector


class BaseTestFieldInspector(TestCase):
    FieldedClass = None  # type: ClassVar[Optional[type]]

    _field_class = ClassField  # type: Type[ClassField]
    _supports_diverging_names = None  # type: ClassVar[Optional[bool]]
    _names_and_values = (
        ('color', 'red'),
        ('size', 2),
        ('weight', 34.56),
    )  # type: ClassVar[Tuple[str, ...]]

    def _get_expected_fields(self) -> List[ClassField]:
        return [
            self._field_class(
                init_name=name,
                attr_name='_'+name if self._supports_diverging_names else name
            )
            for name, _ in self._names_and_values
        ]

    def _get_expected_init_dict(self) -> Dict[str, Any]:
        return {name: value for name, value in self._names_and_values}

    def _get_expected_attr_dict(self) -> Dict[str, Any]:
        return {
            ('_'+name if self._supports_diverging_names else name): value
            for name, value in self._names_and_values
        }

    def _get_expected_field_dict(self) -> Dict[FieldedClass, Any]:
        return {
            self._field_class(
                init_name=name,
                attr_name='_'+name if self._supports_diverging_names else name
            ): value
            for name, value in self._names_and_values
        }

    def _get_inspector(self) -> FieldInspector:
        raise NotImplementedError

    def _get_fielded_obj(self) -> Any:
        assert self.FieldedClass is not None
        return self.FieldedClass(**self._get_expected_init_dict())

    def test_get_fields(self) -> None:
        inspector = self._get_inspector()

        expected_fields = self._get_expected_fields()
        actual_fields = inspector.get_fields(self.FieldedClass)
        self.assertListEqual(actual_fields, expected_fields)

    def test_get_field_dict(self) -> None:
        obj = self._get_fielded_obj()
        inspector = self._get_inspector()

        expected_dict = self._get_expected_field_dict()
        actual_dict = inspector.get_field_dict(obj)
        self.assertDictEqual(actual_dict, expected_dict)

    def test_get_name_dict(self) -> None:
        obj = self._get_fielded_obj()
        inspector = self._get_inspector()

        expected_dict = self._get_expected_init_dict()
        actual_dict = inspector.get_name_dict(obj, init_mode=True)
        self.assertDictEqual(actual_dict, expected_dict)

        expected_dict = self._get_expected_attr_dict()
        actual_dict = inspector.get_name_dict(obj, attr_mode=True)
        self.assertDictEqual(actual_dict, expected_dict)


class TestClassicalNamedTupleFieldInspector(BaseTestFieldInspector):
    _supports_diverging_names = False

    FieldedClass = namedtuple('FieldedClass', ('color', 'size', 'weight'))

    def _get_inspector(self) -> FieldInspector:
        return NamedTupleFieldInspector()


class TestTypingNamedTupleFieldInspector(BaseTestFieldInspector):
    _supports_diverging_names = False

    # Python 3.5-compatible syntax
    FieldedClass = NamedTuple('FieldedClass', (('color', str), ('size', int), ('weight', float)))

    def _get_inspector(self) -> FieldInspector:
        return NamedTupleFieldInspector()


class TestClassicalDictFieldInspector(BaseTestFieldInspector):
    _supports_diverging_names = False

    FieldedClass = dict

    def _get_inspector(self) -> FieldInspector:
        return DictFieldInspector()

    def _get_expected_fields(self) -> List[ClassField]:
        return []


if TypedDict is not None:
    # Python 3.8 and above

    class TestTypedDictTupleFieldInspector(BaseTestFieldInspector):
        _supports_diverging_names = False

        # Python 3.5-compatible syntax
        FieldedClass = TypedDict('FieldedClass', {'color': str, 'size': int, 'weight': float})

        def _get_inspector(self) -> FieldInspector:
            return DictFieldInspector()


class TestAttrsFieldInspector(BaseTestFieldInspector):
    _supports_diverging_names = True

    @attr.s
    class FieldedClass:
        _color = attr.ib()
        _size = attr.ib()
        _weight = attr.ib()

    def _get_inspector(self) -> FieldInspector:
        return AttrsFieldInspector()


if dataclasses is not None:
    # Python 3.7 and above

    class TestDataclassFieldInspector(BaseTestFieldInspector):
        _supports_diverging_names = False

        # Python 3.5-compatible syntax
        FieldedClass = dataclasses.make_dataclass(
            'FieldedClass', (('color', str), ('size', int), ('weight', float)))

        def _get_inspector(self) -> FieldInspector:
            return DataclassFieldInspector()


class TestSchematicsFieldInspector(BaseTestFieldInspector):
    _supports_diverging_names = False

    class FieldedClass(schematics.Model):
        color = schematics.types.StringType()
        size = schematics.types.IntType()
        weight = schematics.types.FloatType()

    def _get_inspector(self) -> FieldInspector:
        return SchematicsFieldInspector()

    def _get_fielded_obj(self) -> Any:
        assert self.FieldedClass is not None
        return self.FieldedClass(self._get_expected_init_dict())


class TestSQLAlchemyModelFieldInspector(BaseTestFieldInspector):
    _supports_diverging_names = False

    class FieldedClass(declarative_base()):
        __tablename__ = 'table'

        color = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
        size = sqlalchemy.Column(sqlalchemy.Integer)
        weight = sqlalchemy.Column(sqlalchemy.Float)

    def _get_inspector(self) -> FieldInspector:
        return SQLAlchemyModelFieldInspector()


del BaseTestFieldInspector
