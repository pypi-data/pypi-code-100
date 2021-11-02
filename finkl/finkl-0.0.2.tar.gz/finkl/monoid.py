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

from abc import ABCMeta
from numbers import Number
from typing import Generic, List as ListT, TypeVar

from finkl.data import Monoid


__all__ = ["List", "Sum", "Product", "Any", "All"]


m = TypeVar("m")

class _BaseMonoid(Generic[m], Monoid[m], metaclass=ABCMeta):
    """ We use inheritance to avoid too much boilerplate """
    _m:m

    def __init__(self, value:m) -> None:
        self._m = value

    def __repr__(self) -> str:
        return repr(self._m)


class List(_BaseMonoid[ListT]):
    """ List monoid """
    mempty = []

    def mappend(self, rhs:ListT) -> ListT:
        return self._m + rhs


class Sum(_BaseMonoid[Number]):
    """ Numeric sum monoid """
    mempty = 0

    def mappend(self, rhs:Number) -> Number:
        return self._m + rhs


class Product(_BaseMonoid[Number]):
    """ Numeric product monoid """
    mempty = 1

    def mappend(self, rhs:Number) -> Number:
        return self._m * rhs


class Any(_BaseMonoid[bool]):
    """ Any monoid """
    mempty = False

    def mappend(self, rhs:bool) -> bool:
        return self._m or rhs


class All(_BaseMonoid[bool]):
    """ All monoid """
    mempty = True

    def mappend(self, rhs:bool) -> bool:
        return self._m and rhs
