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

from typing import Any, Callable, ClassVar, Generic, Type, TypeVar

from finkl.abc import Monad, Monoid


__all__ = ["Writer"]


a = TypeVar("a")
b = TypeVar("b")

class Writer(Generic[a, b], Monad[a]):
    """ Writer monad """
    _v:a
    _w:Monoid[b]

    monoid:ClassVar[Monoid[b]]

    def __init__(self, v:a, w:Monoid[b]) -> None:
        self._v = v
        self._w = w

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self.value)}, {repr(self.writer)})"

    @property
    def value(self) -> a:
        return self._v

    @property
    def writer(self) -> Monoid[b]:
        return self._w

    @classmethod
    def retn(cls, v:a) -> Writer[a, b]:
        return cls(v, cls.monoid.mempty())

    def bind(self, rhs:Callable[[a], Writer[b, Any]]) -> Writer[b, Any]:
        new = rhs(self.value)
        return self.__class__(new.value, self.writer.mappend(new.writer))
