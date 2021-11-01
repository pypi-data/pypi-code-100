# @Time     : 2021/11/1
# @Project  : wanba_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from asyncio import iscoroutinefunction
from collections.abc import Callable

from ._types import Lang


def is_function(value: Lang) -> bool:
    return isinstance(value, Callable)


def is_async_function(value: Lang) -> bool:
    return iscoroutinefunction(value)
