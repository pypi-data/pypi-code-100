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

from typing import Any, Generic, Type, TypeVar, Union

from finkl.data import Eq, Applicative, Monad


__all__ = ["Maybe", "Just", "Nothing"]


a = TypeVar("a")
b = TypeVar("b")


class _Nothing:
    """ Nothing sentinel class """

class Maybe(Generic[a, b], Eq, Applicative[a, b], Monad[a]):
    """ Maybe """
    _v:Union[a, Type[_Nothing]]

    def __init__(self, v:Union[a, Type[_Nothing]]):
        self._v = v

    def __repr__(self):
        return "Nothing" if self._nothing else f"Just({repr(self._v)})"

    def __eq__(self, rhs:Maybe[a, Any]) -> bool:
        return self._v == rhs._v

    @property
    def _nothing(self):
        return self._v is _Nothing

    def fmap(self, fn:Callable[[a], b]) -> Maybe[b, Any]:
        return Maybe(_Nothing if self._nothing else fn(self._v))

    @staticmethod
    def pure(v:Union[a, Type[_Nothing]]) -> Maybe[a, Any]:
        if v is _Nothing:
            raise ValueError

        return Maybe(v)

    def applied_over(self, rhs:Maybe[a, Any]) -> Maybe[b, Any]:
        return Maybe(_Nothing) if self._nothing else rhs.fmap(self._v)

    retn = pure

    def bind(self, rhs:Callable[[a], Maybe[b, Any]]) -> Maybe[b, Any]:
        return Maybe(_Nothing) if self._nothing else rhs(self._v)

    @staticmethod
    def fail(msg:str) -> Maybe[a, Any]:
        return Maybe(_Nothing)

Just = Maybe.pure
Nothing = Maybe(_Nothing)
