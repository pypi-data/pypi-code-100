# @Time     : 2021/11/5
# @Project  : wanba_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import Union
from .const import SECOND, MILLISECOND, MICROSECOND

FloatOrInt = Union[float, int]


class Base:

    @classmethod
    def second(cls, t: FloatOrInt) -> float:
        return cls.convert(t, SECOND)

    @classmethod
    def millisecond(cls, t: FloatOrInt) -> float:
        return cls.convert(t, MILLISECOND)

    @classmethod
    def microsecond(cls, t: FloatOrInt) -> float:
        return cls.convert(t, MICROSECOND)

    @classmethod
    def convert(cls, t: FloatOrInt, unt: float) -> float:
        raise NotImplementedError
