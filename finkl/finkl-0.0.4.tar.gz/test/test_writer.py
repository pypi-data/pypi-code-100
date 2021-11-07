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

import unittest
from typing import Generic, TypeVar

from finkl.abc import Eq, Monoid
from finkl.monad import List, Writer
from finkl.monoid import Sum


a = TypeVar("a")
m = TypeVar("m", bound=Monoid)

class _EqWriter(Generic[a, m], Writer[a, m], Eq):
    def __eq__(self, rhs:_EqWriter[a, m]) -> bool:
        return self.run_writer() == rhs.run_writer()

class _Logger(_EqWriter[int, List[str]]):
    writer = List

class _Counter(_EqWriter[str, Sum]):
    writer = Sum


class TestWriter_Logger(unittest.TestCase):
    def test_return(self):
        logger = _Logger.retn(123)
        self.assertEqual(logger, _Logger(123, List()))

    def test_bind(self):
        _inc = lambda x: _Logger(x + 1, List(f"Incremented {x}"))
        _dbl = lambda x: _Logger(x * 2, List(f"Doubled {x}"))

        result = _Logger(0).bind(_inc) \
                           .bind(_inc) \
                           .bind(_dbl)

        self.assertEqual(result, _Logger(4, List(
            "Incremented 0",
            "Incremented 1",
            "Doubled 2"
        )))

    def test_laws(self):
        # NOTE Obviously here we're just testing arbitrary values,
        # rather than over the entire type space.
        _inc = lambda x: _Logger(x + 1, List("foo"))
        _dbl = lambda x: _Logger(x * 2, List("bar"))

        # Left Identity
        self.assertEqual(_Logger.retn(123) >= _inc, _inc(123))

        # Right Identity
        self.assertEqual(_Logger(123) >= _Logger.retn, _Logger(123))

        ## Associativity
        self.assertEqual((_Logger(123) >= _inc) >= _dbl,
                         _Logger(123) >= (lambda x: _inc(x) >= _dbl))


class TestWriter_Counter(unittest.TestCase):
    def test_return(self):
        counter = _Counter.retn("Hello, World!")
        self.assertEqual(counter, _Counter("Hello, World!", Sum(0)))

    def test_bind(self):
        def _say(what):
            return lambda x: _Counter(f"{x}{what}", Sum(1))

        result = _Counter("Hello").bind(_say(", ")) \
                                  .bind(_say("World")) \
                                  .bind(_say("!"))

        self.assertEqual(result, _Counter("Hello, World!", Sum(3)))

    def test_laws(self):
        # NOTE Obviously here we're just testing arbitrary values,
        # rather than over the entire type space.
        _emph = lambda x: _Counter(f"{x}!", Sum(1))
        _qstn = lambda x: _Counter(f"{x}?", Sum(1))

        # Left Identity
        self.assertEqual(_Counter.retn("foo") >= _emph, _emph("foo"))

        # Right Identity
        self.assertEqual(_Counter("foo") >= _Counter.retn, _Counter("foo"))

        ## Associativity
        self.assertEqual((_Counter("foo") >= _emph) >= _qstn,
                         _Counter("foo") >= (lambda x: _emph(x) >= _qstn))


if __name__ == "__main__":
    unittest.main()
