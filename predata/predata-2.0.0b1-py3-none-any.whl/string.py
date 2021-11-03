from re import M, sub
from typing import Any, AnyStr, Callable, Optional, overload

from .typing import STRING_AND_BYTE_TYPES, ValueType

__all__ = [
    'strip_string',
    'strip_text',
    'lower_string',
    'remove_spaces',
    'StripPreparerFactory',
]


def strip_text(value: Optional[Any]) -> str:
    if value is None:
        return ''

    if not isinstance(value, STRING_AND_BYTE_TYPES):
        value = str(value)

    value = sub(r'^[\s\n\t]*', '', value, M)
    value = sub(r'[\s\n\t]*$', '', value, M)
    return value


@overload
def strip_string(value: Optional[AnyStr]) -> str: ...


@overload
def strip_string(value: ValueType) -> ValueType: ...


def strip_string(value):
    if value is None:
        return ''

    if isinstance(value, STRING_AND_BYTE_TYPES):
        return value.strip()

    return value


@overload
def remove_spaces(value: None) -> None: ...


@overload
def remove_spaces(value: AnyStr) -> AnyStr: ...


@overload
def remove_spaces(value: ValueType) -> ValueType: ...


def remove_spaces(value):
    if value is None:
        return value

    if isinstance(value, STRING_AND_BYTE_TYPES):
        return sub(r'\s+', '', value, M)

    return value


@overload
def lower_string(value: AnyStr) -> AnyStr: ...


@overload
def lower_string(value: ValueType) -> ValueType: ...


def lower_string(value):
    if isinstance(value, STRING_AND_BYTE_TYPES):
        return value.lower()

    return value


class StripPreparerFactory:
    """Factory for any preparer with striping text before applying preparer."""
    def __init__(self, preparer: Callable[[str], Any]) -> None:
        self._preparer = preparer

    def __call__(self, value: Any) -> Any:
        return self._preparer(
            strip_text(value),
        )
