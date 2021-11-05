"""
Unittests for spacing_functions module
"""

import unittest
import numpy as np

from binarycpython.utils.spacing_functions import const
from binarycpython.utils.functions import Capturing


class test_spacing_functions(unittest.TestCase):
    """
    Unit test for spacing functions
    """

    def test_const(self):
        with Capturing() as output:
            self._test_const()

    def _test_const(self):
        """
        Unittest for function const
        """

        const_return = const(1, 10, 10)
        self.assertTrue(
            (const_return == np.linspace(1, 10, 10 + 1)).all(),
            msg="Output didn't contain SINGLE_STAR_LIFETIME",
        )


if __name__ == "__main__":
    unittest.main()
