# @Time     : 2021/11/1
# @Project  : wanba_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from ._types import Lang


def is_bytes(value: Lang) -> bool:
    return isinstance(value, bytes)


def is_bytearray(value: Lang) -> bool:
    return isinstance(value, bytearray)
