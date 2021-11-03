from decimal import Decimal
from typing import TypeVar, Union

__all__ = [
    'STRING_AND_BYTE_TYPES',
    'NUMBER_AND_BOOL_TYPES',
    'ValueType',
    'NumberAndBoolType',
]

STRING_AND_BYTE_TYPES = str, bytes
NUMBER_AND_BOOL_TYPES = bool, int, float, Decimal

ValueType = TypeVar('ValueType')
NumberAndBoolType = Union[bool, int, float, Decimal]
