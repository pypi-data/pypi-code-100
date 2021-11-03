import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt

from pybirds.data import data_loader
from pybirds.util.model_helper import score_bin


def main():
    df_data = data_loader.DataLoader.get_score_sample_data()
    print(df_data.head().to_string())

    score_bin.ScoreBin.fit_transform_subscore(df_data, df_data, 'label_fpd30', 'prob', 'subscore')

    res = score_bin.ScoreBin.bin_megascore(df_data, 'score')
    print(res)

    res = score_bin.ScoreBin.bin_subscore(df_data, 'subscore', bin_name='subscore_bin')
    print(res)


if __name__ == '__main__':
    main()
