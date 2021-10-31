"""
Tests calculating.
"""
import unittest

import verbcalc


class TestCalculate(unittest.TestCase):
    def test_calculations(self):
        self.assertEqual(verbcalc.calculate('2 plus 2'), 4)
        self.assertEqual(verbcalc.calculate('2 minus 2'), 0)
        self.assertEqual(verbcalc.calculate('2 times 2'), 4)
        self.assertEqual(verbcalc.calculate('2 divided by 2'), 1)
        self.assertEqual(verbcalc.calculate('2 to the power of 2'), 4)
        self.assertEqual(verbcalc.calculate('Absolute value of -2'), 2)


if __name__ == '__main__':
    unittest.main()
