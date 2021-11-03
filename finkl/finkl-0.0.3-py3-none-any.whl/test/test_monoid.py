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

from finkl.monoid import List, Sum, Product, Any, All


class TestList(unittest.TestCase):
    def test_mconcat(self):
        self.assertEqual(List.mconcat(), List([]))
        self.assertEqual(List.mconcat(*[List([x]) for x in [1, 2, 3]]), List([1, 2, 3]))


class TestSum(unittest.TestCase):
    def test_mconcat(self):
        self.assertEqual(Sum.mconcat(), Sum(0))
        self.assertEqual(Sum.mconcat(*[Sum(x) for x in [1, 2, 3]]), Sum(6))


class TestProduct(unittest.TestCase):
    def test_mconcat(self):
        self.assertEqual(Product.mconcat(), Product(1))
        self.assertEqual(Product.mconcat(*[Product(x) for x in [1, 2, 3]]), Product(6))


class TestAny(unittest.TestCase):
    def test_mconcat(self):
        self.assertEqual(Any.mconcat(), Any(False))
        self.assertEqual(Any.mconcat(*[Any(x) for x in [False, False, True]]), Any(True))


class TestAll(unittest.TestCase):
    def test_mconcat(self):
        self.assertEqual(All.mconcat(), All(True))
        self.assertEqual(All.mconcat(*[All(x) for x in [True, True, True]]), All(True))


if __name__ == "__main__":
    unittest.main()
