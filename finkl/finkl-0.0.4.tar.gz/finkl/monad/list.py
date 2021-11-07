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

from typing import Callable, Generic, List as _List, TypeVar

from finkl.abc import Eq, Functor, Monad, Monoid


__all__ = ["List"]


a = TypeVar("a")
b = TypeVar("b")

class List(Generic[a], Eq, Functor[_List[a]], Monad[_List[a]], Monoid[_List[a]]):
    """ List functor, monad and monoid """
    _v:_List[a]

    def __init__(self, *vs:a) -> None:
        self._v = list(vs)

    def __eq__(self, rhs:List[a]) -> bool:
        return self._v == rhs._v

    def __repr__(self) -> str:
        return repr(self._v)

    def fmap(self, fn:Callable[[a], b]) -> List[b]:
        return List(*[fn(v) for v in self._v])

    @classmethod
    def retn(cls, v:a) -> List[a]:
        return List(v)

    def bind(self, rhs:Callable[[a], List[b]]) -> List[b]:
        return List.mconcat(*self.fmap(rhs)._v)

    @staticmethod
    def fail(msg:str) -> List[a]:
        return List()

    @staticmethod
    def mempty():
        return List()

    def mappend(self, rhs:List[a]) -> List[a]:
        return List(*(self._v + rhs._v))
