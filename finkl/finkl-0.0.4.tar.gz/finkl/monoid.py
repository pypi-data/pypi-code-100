"""
Copyright (c) 2021 Christopher Harrison

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License for more details.

You should have received a copy of the GNU General Public License along
with this program. If not, see https://www.gnu.org/licenses/
"""

from __future__ import annotations

from abc import ABCMeta
from numbers import Number
from typing import Generic, TypeVar

from finkl.abc import Eq, Monoid


__all__ = ["Sum", "Product", "Any", "All"]


a = TypeVar("a")
m = TypeVar("m")


class _BaseMonoid(Generic[m], Eq, Monoid[m], metaclass=ABCMeta):
    """ We use inheritance to avoid too much boilerplate """
    _m:m

    def __init__(self, value:m) -> None:
        self._m = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self._m)})"

    def __eq__(self, rhs:_BaseMonoid) -> bool:
        return self._m == rhs._m


class Sum(_BaseMonoid[Number]):
    """ Numeric sum monoid """
    @staticmethod
    def mempty():
        return Sum(0)

    def mappend(self, rhs:Sum) -> Sum:
        return Sum(self._m + rhs._m)


class Product(_BaseMonoid[Number]):
    """ Numeric product monoid """
    @staticmethod
    def mempty():
        return Product(1)

    def mappend(self, rhs:Product) -> Product:
        return Product(self._m * rhs._m)


class Any(_BaseMonoid[bool]):
    """ Any monoid """
    @staticmethod
    def mempty():
        return Any(False)

    def mappend(self, rhs:Any) -> Any:
        return Any(self._m or rhs._m)


class All(_BaseMonoid[bool]):
    """ All monoid """
    @staticmethod
    def mempty():
        return All(True)

    def mappend(self, rhs:All) -> All:
        return All(self._m and rhs._m)
