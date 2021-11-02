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

from typing import Callable, TypeVar


__all__ = ["identity", "compose"]


a = TypeVar("a")
b = TypeVar("b")
c = TypeVar("c")


def identity(x:a) -> a:
    """ id :: a -> a """
    return x


def compose(f:Callable[[b], c], g:Callable[[a], b]) -> Callable[[a], c]:
    """ (.) :: (b -> c) -> (a -> b) -> (a -> c) """
    return lambda x: f(g(x))
