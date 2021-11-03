import unittest

from proces import preprocess


class SamplingTest(unittest.TestCase):
    def setUp(self) -> None:
        self.text_list = []
        self.result_list = []

    def test_sampling(self) -> None:
        self.assertEqual(preprocess(self.text_list), self.result_list)


if __name__ == '__main__':
    unittest.main()
