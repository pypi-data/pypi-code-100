import pandas as pd

from .. import settings


def get_credit_german_data():
    fp_data = f"{settings.BASE_DIR}/data/credit_german.csv"
    df_data = pd.read_csv(fp_data)

    return df_data
