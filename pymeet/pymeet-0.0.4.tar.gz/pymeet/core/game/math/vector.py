from typing import Tuple


class Vector:
    def __init__(self, x: float, y: float):
        self._x: float = x
        self._y: float = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def get_tuple(self) -> Tuple[float, float]:
        return self._x, self._y

    def __add__(self, other: 'Vector'):
        return Vector(self._x + other._x, self._y + other._y)

    def __mul__(self, other: float):
        return Vector(self._x * other, self._y * other)
