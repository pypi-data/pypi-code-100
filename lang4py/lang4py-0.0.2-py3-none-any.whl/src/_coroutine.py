# @Time     : 2021/11/1
# @Project  : wanba_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from asyncio import iscoroutine, isfuture, Task

from ._types import Lang


def is_coroutine(value: Lang) -> bool:
    return iscoroutine(value)


def is_future(value: Lang) -> bool:
    return isfuture(value)


def is_coroutine_task(value: Lang) -> bool:
    return isinstance(value, Task)
