# @Time     : 2021/11/1
# @Project  : wanba_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from ._types import Lang
from ._null import is_null

TAG = list

collections = {
    "dict": dict,
    "list": list,
    "set": set,
    "tup": tuple
}


def is_collection(value: Lang, type_: str = None) -> bool:
    t = collections.get(type_, None)
    if is_null(t):
        types = tuple(collections.values())
        return isinstance(value, types)
    return isinstance(value, t)


def is_dict(value: Lang) -> bool:
    return is_collection(value, "dict")


def is_list(value: Lang) -> bool:
    return is_collection(value, "list")


def is_set(value: Lang) -> bool:
    return is_collection(value, "set")


def is_tuple(value: Lang) -> bool:
    return is_collection(value, "tup")
