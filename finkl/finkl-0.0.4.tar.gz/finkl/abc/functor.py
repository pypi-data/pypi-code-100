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


__all__ = ["Functor", "Applicative"]


a = TypeVar("a")
b = TypeVar("b")


class Functor(Generic[a], metaclass=ABCMeta):
    """ Abstract base class for functors """
    @abstractmethod
    def fmap(self, fn:Callable[[a], b]) -> Functor[b]:
        """ fmap :: f a -> (a -> b) -> f b """


class Applicative(Generic[a, b], Functor[Callable[[a], b]], metaclass=ABCMeta):
    """ Abstract base class for applicative functors """
    @classmethod
    @abstractmethod
    def pure(cls, v:a) -> Functor[a]:
        """ pure :: a -> f a """

    @abstractmethod
    def applied_over(self, rhs:Functor[a]) -> Functor[b]:
        """ (<*>) :: f (a -> b) -> f a -> f b """

    def __matmul__(self, rhs:Functor[a]) -> Functor[b]:
        """ We use `x @ y` as Haskell's `x <*> y` """
        return self.applied_over(rhs)
