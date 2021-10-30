import unittest
import pandas as pd
from pathlib import Path
from src.preprocessing.preprocessor import Preprocessor


class TestPreprocessor(unittest.TestCase):
    def setUp(self):
        self.preprocessor = Preprocessor()
        data_path = Path('data/hotel-reviews')
        self.df = pd.read_csv(data_path / 'bew_lang.csv',
                              sep=';',
                              nrows=1000,
                              warn_bad_lines=False,
                              error_bad_lines=False)

    def test_preprocessor(self):
        df_cleaned = self.preprocessor.transform(self.df)
        self.assertNotEqual(len(self.df), len(df_cleaned))


if __name__ == '__main__':
    unittest.main()
