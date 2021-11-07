import unittest
from docedian import utils

class TestUtilsMethods(unittest.TestCase):

    def test_compute_vat_vd(self):
        """
        Test the compute vat vd method
        """

        self.assertEqual(utils.compute_vat_vd('901079560'), '1')
        self.assertEqual(utils.compute_vat_vd('900495672'), '8')
        self.assertEqual(utils.compute_vat_vd('901025526'), '9')
        self.assertEqual(utils.compute_vat_vd('901250040'), '5')
        self.assertEqual(utils.compute_vat_vd('900952931'), '1')
