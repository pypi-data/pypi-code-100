# @Time     : 2021/11/1
# @Project  : wanba_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from ._collection import collections
from ._lang import lang
from ._null import is_null
from ._types import Lang

py_objs = {**collections, **lang}
py_objs.pop("set", None)


def is_py_obj(value: Lang) -> bool:
    if is_null(value):
        return True
    return isinstance(value, tuple(py_objs.values()))
