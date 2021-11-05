import unittest

from roseta import trans_city


class TestCity(unittest.TestCase):
    def setUp(self) -> None:
        self.city_data = {
            # pattern1
            "杭州": [("杭州市", "市"), ("浙江省杭州市", "省")],
            "杭州市": [("杭州市", "市"), ("浙江省杭州市", "省")]
        }

    def test_trans_city(self) -> None:
        for key, value in self.city_data.items():
            self.assertEqual(trans_city(key), value[0])  # default unit: 市
            self.assertEqual(trans_city(key, unit="市"), value[0])
            self.assertEqual(trans_city(key, unit="省"), value[1])


if __name__ == '__main__':
    unittest.main()
