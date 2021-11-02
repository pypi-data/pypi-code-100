from decimal import Decimal
from functools import wraps
from typing import Any, Callable


def get_type(obj):
    if obj is None:
        return "null"
    if isinstance(obj, str):
        return "string"
    if isinstance(obj, bool):
        return "boolean"
    if isinstance(obj, list):
        return "array"
    if isinstance(obj, dict):
        return "object"
    if isinstance(obj, int | float | Decimal):
        return "number"
    raise TypeError


def when(type: str):
    def inner(func: Callable[[Any], bool]):
        @wraps(func)
        def decorated(obj: str):
            if is_type(obj, type):
                return func(obj)
            return NotImplemented

        decorated.__wrapped__ = func  # type: ignore
        return decorated

    return inner


def is_type(obj, *types: str) -> bool:
    obj_type = get_type(obj)
    print("grre", obj_type, types)
    if obj_type in types:
        return True
    if obj_type == "number" and "integer" in types and is_integer(obj):
        return True
    return False


def is_integer(obj) -> bool:
    return obj == int(obj)


@when("string")
def is_date_time(obj: str) -> bool:
    pass


@when("string")
def is_date(obj: str) -> bool:
    pass


@when("string")
def is_time(obj: str) -> bool:
    pass


@when("string")
def is_duration(obj: str) -> bool:
    pass


@when("string")
def is_email(obj: str) -> bool:
    pass


@when("string")
def is_idn_email(obj: str) -> bool:
    pass


@when("string")
def is_hostname(obj: str) -> bool:
    pass


@when("string")
def is_idn_hostname(obj: str) -> bool:
    pass


@when("string")
def is_ipv4(obj: str) -> bool:
    pass


@when("string")
def is_ipv6(obj: str) -> bool:
    pass


@when("string")
def is_uri(obj: str) -> bool:
    pass


@when("string")
def is_uri_reference(obj: str) -> bool:
    pass


@when("string")
def is_iri(obj: str) -> bool:
    pass


@when("string")
def is_iri_reference(obj: str) -> bool:
    pass


@when("string")
def is_uuid(obj: str) -> bool:
    pass


@when("string")
def is_uri_template(obj: str) -> bool:
    pass


@when("string")
def is_json_pointer(obj: str) -> bool:
    pass


@when("string")
def is_relative_json_pointer(obj: str) -> bool:
    pass


@when("string")
def is_regex(obj: str) -> bool:
    pass
