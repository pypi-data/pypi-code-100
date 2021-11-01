# @Time     : 2021/11/1
# @Project  : wanba_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from ._types import Lang


def is_null(value: Lang) -> bool:
    return value is None


def is_not_null(value: Lang) -> bool:
    return not is_null(value)
