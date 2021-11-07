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
from functools import reduce
from typing import Generic, TypeVar


__all__ = ["Monoid"]


m = TypeVar("m")

class Monoid(Generic[m], metaclass=ABCMeta):
    """ Abstract base class for monoids """
    @staticmethod
    @abstractmethod
    def mempty() -> Monoid[m]:
        """ mempty :: m """

    @abstractmethod
    def mappend(self, rhs:Monoid[m]) -> Monoid[m]:
        """ mappend :: m -> m -> m """

    @classmethod
    def mconcat(cls, *ms:Monoid[m]) -> Monoid[m]:
        """ mconcat :: [m] -> m """
        folder = lambda x, y: x.mappend(y)
        return reduce(folder, ms, cls.mempty())
