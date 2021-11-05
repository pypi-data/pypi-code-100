# @Time     : 2021/11/5
# @Project  : wanba_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from operator import truediv
from .base import Base, FloatOrInt


class Timeunt(Base):

    @classmethod
    def convert(cls, t: FloatOrInt, unt: float) -> float:
        if any([not t, not unt]):
            return 0.0
        try:
            return float(truediv(t, unt))
        except ZeroDivisionError:
            return 0.0
