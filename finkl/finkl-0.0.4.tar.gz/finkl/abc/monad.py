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

from abc import ABCMeta, abstractmethod
from typing import Callable, Generic, TypeVar


__all__ = ["Monad"]


a = TypeVar("a")
b = TypeVar("b")


class Monad(Generic[a], metaclass=ABCMeta):
    """ Abstract base class for monads """
    @classmethod
    @abstractmethod
    def retn(cls, v:a) -> Monad[a]:
        """ return :: a -> m a """

    @abstractmethod
    def bind(self, rhs:Callable[[a], Monad[b]]) -> Monad[b]:
        """ (>>=) :: m a -> (a -> m b) -> m b """

    def __ge__(self, rhs:Callable[[a], Monad[b]]) -> Monad[b]:
        """ We use `x >= y` as Haskell's `x >>= y`; beware precedence rules """
        return self.bind(rhs)

    def then(self, rhs:Monad[b]) -> Monad[b]:
        """ (>>) :: m a -> m b -> m b """
        return self.bind(lambda _: rhs)

    def __rshift__(self, rhs:Monad[b]) -> Monad[b]:
        return self.then(rhs)

    @staticmethod
    def fail(msg:str) -> Monad[a]:
        """ fail :: String -> m a """
        raise Exception(msg)

    # TODO do notation analogue...maybe with context managers
