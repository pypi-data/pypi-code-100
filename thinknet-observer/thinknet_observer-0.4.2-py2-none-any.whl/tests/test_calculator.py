import unittest
import math
from thinknet_observer import Calculator


class CalculatorTestCase(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_natural_number(self):
        """Test natural number 5 multiplied by 2"""

        # 5 multiplied by 2 return 10
        result = self.calculator.multiply(5, 2)
        self.assertEqual(result, 10)

    def test_integer_number1(self):
        """Test integer number -7 multiplied by 2"""

        # -7 multiplied by 2 return -14
        result = self.calculator.multiply(-7, 2)
        self.assertEqual(result, -14)

    def test_integer_number2(self):
        """Test integer number -7 multiplied by 2"""

        # -7 multiplied by 2 return -14
        result = self.calculator.add(-7, 2)
        self.assertEqual(result, -5)

    def test_zero(self):
        """Test 0 multiplied by 2"""

        # 0 multiplied by 2 return 0
        result = self.calculator.multiply(2, 0)
        self.assertEqual(result, 0)

    def test_rational_number(self):
        """Test rational number 6/17 multiplied by 2"""

        # 6/17 multiplied by 2 return (6/17) * 2
        result = self.calculator.multiply(6 / 17, 2)
        self.assertEqual(result, (6 / 17) * 2)

    def test_real_number(self):
        """Test real number PI multiplied by 2"""

        # PI multiplied by 2 return 2PI
        result = self.calculator.multiply(math.pi, 2)
        self.assertEqual(result, math.pi * 2)


if __name__ == "__main__":
    unittest.main()
