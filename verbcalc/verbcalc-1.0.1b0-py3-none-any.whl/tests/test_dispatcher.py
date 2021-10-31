"""
Tests dispatcher module.
"""
import unittest

from verbcalc.core.dispatcher import Dispatcher, InvalidExpressionException


class TestDispatcher(unittest.TestCase):
    """
    Tests how dispatcher works.
    """

    def test_naive_single(self):
        self.assertEqual(4, Dispatcher().dispatch(['2', '+', '2']))

    def test_naive_multiple(self):
        self.assertEqual(4, Dispatcher().dispatch(
            ['2', '+', '2', '-', '2', '+', '2']))

    def test_multiple(self):
        self.assertEqual(130, Dispatcher().dispatch(
            ['2', '+', '2', '*', '8', '**', '2']))

    def test_functions(self):
        self.assertEqual(5, Dispatcher().dispatch(['abs', '-5']))

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            Dispatcher().dispatch(['2', '/', '0'])

    def test_incorrect_amount_of_operators(self):
        with self.assertRaises(InvalidExpressionException):
            Dispatcher().dispatch(['2', '4', '3', '-', '-'])


if __name__ == '__main__':
    unittest.main()
