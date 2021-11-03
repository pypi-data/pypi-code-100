from typing import Any, AnyStr, Optional, Sized, Type, Union, overload

from .typing import NUMBER_AND_BOOL_TYPES, NumberAndBoolType, \
    STRING_AND_BYTE_TYPES, ValueType

__all__ = [
    'as_int',
    'as_float',
    'as_bool',
    'as_none',
    'as_str',
]


def _as_is(
    value: ValueType,
    try_only: bool,
    exc_cls: Type[Exception] = TypeError,
) -> ValueType:
    """Function, that returns value "as is" or raises error,
    depending on ``try_only`` flag."""
    if try_only:
        return value

    raise exc_cls(value)


@overload
def _as_type(
    type_cls: Type[int],
    value: ValueType,
    try_only: bool,
) -> Union[ValueType, int]: ...


@overload
def _as_type(
    type_cls: Type[float],
    value: ValueType,
    try_only: bool,
) -> Union[ValueType, float]: ...


def _as_type(type_cls, value, try_only):
    """
    Type coercing function over it`s constructor.

    :param type_cls: Class of type to coerce.
    :param value: Original value to try to coerce.
    :param try_only: Try onle flag.
    :return: Coerced value or original value if coercing failed and try
    only flag is ``True``.
    :return: Coerced value.
    :raises: ``TypeError``, ``ValueError``
    """
    try:
        return type_cls(value)

    except (ValueError, TypeError) as err:
        return _as_is(value, try_only, exc_cls=type(err))


@overload
def _decode(value: str, try_only: bool) -> str: ...


@overload
def _decode(value: bytes, try_only: bool) -> AnyStr: ...


def _decode(value, try_only):
    """
    Decode function.

    :param value: Value of string or byte types.
    :param try_only: Try only flag.
    :return: String value.
    """
    if not isinstance(value, bytes):
        return value

    try:
        return value.decode('utf-8')

    except UnicodeDecodeError:
        if not try_only:
            raise

    return value


@overload
def as_int(
    value: NumberAndBoolType,
    try_only: bool = False,
) -> int: ...


@overload
def as_int(
    value: ValueType,
    try_only: bool = False,
) -> Union[int, ValueType]: ...


def as_int(value, try_only=False):
    """
    Coercion to type ``int``.

    :param value: Input value.
    :param try_only: Try only flag.
    :return: Integer or value as is if coercion failed and try only flag is
    ``True``.
    :raises: ``TypeError``
    """
    if isinstance(value, NUMBER_AND_BOOL_TYPES):
        return int(value)

    if isinstance(value, STRING_AND_BYTE_TYPES):
        return _as_type(int, value, try_only)

    return _as_is(value, try_only)


@overload
def as_float(
    value: NumberAndBoolType,
    try_only: bool = False,
) -> float: ...


@overload
def as_float(
    value: ValueType,
    try_only: bool = False,
) -> Union[float, ValueType]: ...


def as_float(value, try_only=False):
    """
    Coercion to type ``float``.

    :param value: Input value.
    :param try_only: Try only flag.
    :return: Float or value as is if coercion failed and try only flag is
    ``True``.
    :raises: ``TypeError``
    """
    if isinstance(value, NUMBER_AND_BOOL_TYPES):
        return float(value)

    if isinstance(value, STRING_AND_BYTE_TYPES):
        return _as_type(float, value.replace(',', '.'), try_only)

    return _as_is(value, try_only)


_NONE_TYPE_STRINGS = frozenset({'null', 'none', 'nil', 'nul'})


@overload
def as_none(
    value: None,
    try_only: bool = False,
) -> None: ...


@overload
def as_none(
    value: ValueType,
    try_only: bool = False,
) -> Optional[ValueType]: ...


def as_none(value, try_only=False):
    """
    Coercion to ``None``.

    :param value: Input value.
    :param try_only: Try only flag.
    :return: ``None`` or value as is if coercion failed and try only flag is
    ``True``.
    :raises: ``TypeError``, ``ValueError``, ``UnicodeDecodeError``
    """
    if value is None:
        return

    if not isinstance(value, STRING_AND_BYTE_TYPES):
        return _as_is(value, try_only)

    if _decode(value, try_only).lower().strip() in _NONE_TYPE_STRINGS:
        return

    # noinspection PyTypeChecker
    return _as_is(value, try_only, exc_cls=ValueError)


_FALSY_TYPE_STRINGS = frozenset({'false', '0', 'no', ''})


@overload
def as_bool(
    value: Union[str, NumberAndBoolType, None],
    try_only: bool = False,
) -> bool: ...


@overload
def as_bool(
    value: ValueType,
    none_to_false: bool = True,
    try_only: bool = False,
) -> Union[bool, ValueType]: ...


def as_bool(value, none_to_false=True, try_only=False):
    """
    Coercion to type ``bool``.

    :param value: Input value.
    :param none_to_false: Flag for deciding if ``None`` value must be
    coerced to ``False``.
    :param try_only: Try only flag.
    :return: Boolean or value as is if coercion failed and try only flag is
    ``True``.
    :raises: ``TypeError``, ``UnicodeDecodeError``
    """
    if isinstance(value, NUMBER_AND_BOOL_TYPES):
        return bool(value)

    if not isinstance(
        value, STRING_AND_BYTE_TYPES,
    ) and value is not None:

        if isinstance(value, Sized):
            return len(value) > 0

        return _as_is(value, try_only)
    
    if value is not None:
        value = _decode(value, try_only).lower().strip()
        
    if value is None or value in _NONE_TYPE_STRINGS:
        if none_to_false:
            return False

        raise TypeError(value)
    
    return value not in _FALSY_TYPE_STRINGS


def as_str(value: Any, try_only: bool = False) -> str:
    """
    Coercion to string.

    :param value: Input value.
    :param try_only: Try only flag.
    :return: String.
    :raises: ``UnicodeDecodeError``
    """
    if value is None:
        return ''

    if isinstance(value, STRING_AND_BYTE_TYPES):
        return _decode(value, try_only)

    return str(value)
