# @Time     : 2021/11/1
# @Project  : wanba_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from ._null import is_null
from ._types import Lang

lang = {
    "boolean": bool,
    "int": int,
    "float": float,
    "str": str
}


def is_lang(value: Lang, type_: str = None) -> bool:
    t = lang.get(type_, None)
    if is_null(t):
        types = tuple(lang.values())
        return isinstance(value, types)
    return isinstance(value, t)


def is_boolean(value: Lang) -> bool:
    return is_lang(value, "boolean")


def is_float(value: Lang) -> bool:
    return is_lang(value, "float")


def is_integer(value: Lang) -> bool:
    return is_lang(value, "int")


def is_number(value: Lang) -> bool:
    return is_integer(value) or is_float(value)


def is_string(value: Lang) -> bool:
    return is_lang(value, "str")
