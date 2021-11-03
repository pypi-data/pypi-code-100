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

import unittest

from finkl.monad import Writer
from finkl.monoid import List, Sum


class _Logger(Writer[int, str]):
    monoid = List

class _Counter(Writer[str, int]):
    monoid = Sum


class TestWriter_Logger(unittest.TestCase):
    def test_return(self):
        logger = _Logger.retn(123)
        self.assertEqual(logger.value, 123)
        self.assertEqual(logger.writer, List([]))

    def test_bind(self):
        _inc = lambda x: _Logger(x + 1, List([f"Incremented {x}"]))
        _dbl = lambda x: _Logger(x * 2, List([f"Doubled {x}"]))

        result = _Logger.retn(0) \
                        .bind(_inc) \
                        .bind(_inc) \
                        .bind(_dbl)

        self.assertEqual(result.value, 4)
        self.assertEqual(result.writer, List([
            "Incremented 0",
            "Incremented 1",
            "Doubled 2"
        ]))

class TestWriter_Counter(unittest.TestCase):
    def test_return(self):
        counter = _Counter.retn("Hello, World!")
        self.assertEqual(counter.value, "Hello, World!")
        self.assertEqual(counter.writer, Sum(0))

    def test_bind(self):
        def _say(what):
            return lambda x: _Counter(f"{x}{what}", Sum(1))

        result = _Counter.retn("Hello") \
                         .bind(_say(", ")) \
                         .bind(_say("World")) \
                         .bind(_say("!"))

        self.assertEqual(result.value, "Hello, World!")
        self.assertEqual(result.writer, Sum(3))


if __name__ == "__main__":
    unittest.main()
