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

from finkl.maybe import Maybe, Just, Nothing
from finkl.util import compose


_inc = lambda x: x + 1
_dbl = lambda x: x * 2


class TestEq(unittest.TestCase):
    def test_equality(self):
        self.assertEqual(Just(123), Just(123))
        self.assertEqual(Nothing, Nothing)
        self.assertNotEqual(Just(1), Just(2))
        self.assertNotEqual(Just(123), Nothing)
        self.assertNotEqual(Nothing, Just(123))


class TestFunctor(unittest.TestCase):
    def test_fmap(self):
        self.assertEqual(Just(123).fmap(_inc), Just(124))
        self.assertEqual(Nothing.fmap(_inc), Nothing)


class TestApplicative(unittest.TestCase):
    def test_pure(self):
        self.assertEqual(Maybe(123), Just(123))

    def test_applied_over(self):
        self.assertEqual(Just(_dbl) @ Just(123), Just(246))
        self.assertEqual(Just(_dbl) @ Nothing, Nothing)
        self.assertEqual(Nothing @ Just(123), Nothing)


class TestMonad(unittest.TestCase):
    def test_return(self):
        self.assertEqual(Maybe.retn(123), Just(123))

    def test_bind(self):
        self.assertEqual(Nothing >= compose(Just, _inc), Nothing)
        self.assertEqual(Nothing.bind(compose(Just, _inc)), Nothing)

        self.assertEqual(Just(123) >= compose(Just, _inc), Just(124))
        self.assertEqual(Just(123).bind(compose(Just, _inc)), Just(124))

        self.assertEqual((Just(123) >= compose(Just, _inc)) >= compose(Just, _dbl), Just(248))
        self.assertEqual(Just(123).bind(compose(Just, _inc)).bind(compose(Just, _dbl)), Just(248))

    def test_sequence(self):
        self.assertEqual(Just(123) >> Nothing, Nothing)
        self.assertEqual(Just(123).then(Nothing), Nothing)

    def test_complex(self):
        self.assertEqual((Just(123) >= compose(Just, _inc)) >> Just(1) >= compose(Just, _dbl), Just(2))

    def test_laws(self):
        # NOTE Obviously here we're just testing arbitrary values,
        # rather than over the entire type space.

        # Left Identity
        self.assertEqual(Maybe.retn(123) >= compose(Just, _inc), compose(Just, _inc)(123))

        # Right Identity
        self.assertEqual(Just(123) >= Maybe.retn, Just(123))

        # Associativity
        self.assertEqual((Just(123) >= compose(Just, _inc)) >= compose(Just, _dbl),
                         Just(123) >= (lambda x: Just(_inc(x)) >= compose(Just, _dbl)))

    def test_do_notation(self):
        self.assertEqual(Just("Hello") >= (lambda x: Just("World") >= (lambda y: Maybe(f"{x} {y}!"))), Just("Hello World!"))
        self.assertEqual(Just("Hello").bind(lambda x: Just("World").bind(lambda y: Maybe(f"{x} {y}!"))), Just("Hello World!"))


if __name__ == "__main__":
    unittest.main()
