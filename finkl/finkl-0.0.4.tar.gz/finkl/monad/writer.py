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

from typing import Callable, ClassVar, Generic, Optional, Tuple, Type, TypeVar

from finkl.abc import Monad, Monoid


__all__ = ["Writer"]


a = TypeVar("a")
b = TypeVar("b")
m = TypeVar("m", bound=Monoid)

class Writer(Generic[a, m], Monad[a]):
    """ Writer monad """
    _v:a
    _w:m

    writer:ClassVar[Type[m]]

    def __init__(self, v:a, w:Optional[m] = None) -> None:
        self._v = v
        self._w = self.writer.mempty() if w is None else w

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self._v)}, {repr(self._w)})"

    def run_writer(self) -> Tuple[a, m]:
        """ runWriter :: Writer w a -> (a, w) """
        return self._v, self._w

    @classmethod
    def retn(cls, v:a) -> Writer[a, m]:
        return cls(v)

    def bind(self, rhs:Callable[[a], Writer[b, m]]) -> Writer[b, m]:
        new = rhs(self._v)
        return self.__class__(new._v, self._w.mappend(new._w))
