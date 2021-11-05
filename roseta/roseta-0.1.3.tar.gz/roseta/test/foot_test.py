import unittest

from roseta import trans_foot


class TestFoot(unittest.TestCase):
    def setUp(self) -> None:
        self.foot_data = {
            "二尺": [(66.67, "cm"), (0.6667, "m")],
            "两尺": [(66.67, "cm"), (0.6667, "m")],
            "2尺": [(66.67, "cm"), (0.6667, "m")],
            "2.1尺": [(70, "cm"), (0.7, "m")],
            "2点1尺": [(70, "cm"), (0.7, "m")],
            "一尺八": [(60, "cm"), (0.6, "m")],
            "1尺一五": [(38.33, "cm"), (0.3833, "m")],
            "二尺五": [(83.33, "cm"), (0.8333, "m")],
            "2尺3": [(76.67, "cm"), (0.7667, "m")],
            "2尺四": [(80, "cm"), (0.8, "m")],
            "2尺2寸": [(73.33, "cm"), (0.7333, "m")],
            "2尺多": [(73.33, "cm"), (0.7333, "m")],
            "两尺一寸": [(70, "cm"), (0.7, "m")],
            "两尺几": [(83.33, "cm"), (0.8333, "m")],
        }

    def test_trans_foot(self) -> None:
        for key, value in self.foot_data.items():
            self.assertEqual(trans_foot(key),  value[0])  # default unit: cm
            self.assertEqual(trans_foot(key, unit="cm"), value[0])
            self.assertEqual(trans_foot(key, unit="m"),  value[1])


if __name__ == '__main__':
    unittest.main()
