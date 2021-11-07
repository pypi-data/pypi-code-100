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

from finkl.monad import List


class TestList(unittest.TestCase):
    def test_equality(self):
        self.assertNotEqual(List(1, 2, 3), List())
        self.assertEqual(List(1, 2, 3), List(1, 2, 3))

    def test_fmap(self):
        self.assertEqual(List(1, 2, 3).fmap(lambda x: x + 1), List(2, 3, 4))

    def test_return(self):
        self.assertEqual(List.retn(123), List(123))

    def test_bind(self):
        _inc = lambda x: List(x + 1)
        _dbl = lambda x: List(x * 2)

        result = List(1, 2, 3).bind(_inc).bind(_inc).bind(_dbl)
        self.assertEqual(result, List(6, 8, 10))

    def test_laws(self):
        # NOTE Obviously here we're just testing arbitrary values,
        # rather than over the entire type space.
        _inc = lambda x: List(x + 1)
        _dbl = lambda x: List(x * 2)

        # Left Identity
        self.assertEqual(List.retn(123) >= _inc, _inc(123))

        # Right Identity
        self.assertEqual(List(123) >= List.retn, List(123))

        ## Associativity
        self.assertEqual((List(123) >= _inc) >= _dbl,
                         List(123) >= (lambda x: _inc(x) >= _dbl))

    def test_mconcat(self):
        self.assertEqual(List.mconcat(), List())
        self.assertEqual(List.mconcat(*[List(x) for x in [1, 2, 3]]), List(1, 2, 3))


if __name__ == "__main__":
    unittest.main()
