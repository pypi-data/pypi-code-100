import pandas as pd
from pathlib import Path

from .. import settings


class DataLoader:
    @classmethod
    def get_credit_german_data(cls):
        fp_data = Path(f'{settings.BASE_DIR}', 'data', 'credit_german.csv')
        df_data = pd.read_csv(fp_data)

        return df_data

    @classmethod
    def get_score_sample_data(cls):
        fp_data = Path(f'{settings.BASE_DIR}', 'data', 'score_sample.csv')
        df_data = pd.read_csv(fp_data)

        return df_data
