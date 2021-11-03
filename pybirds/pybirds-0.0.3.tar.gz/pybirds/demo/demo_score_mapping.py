import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt

from pybirds.data import data_loader
from pybirds.util.model_helper import score_mapping


def demo_megascore():
    df_data = data_loader.DataLoader.get_score_sample_data()

    sm = score_mapping.ScoreMapping(n_bins=25, n_degree=1, score_type='megascore')
    sm.fit(df_data['prob'], df_data['label_fpd30'])

    df_data['cb_score'] = sm.transform(df_data['prob'])

    plt.figure()
    sm.plot_fitted_model()
    plt.show()

    print(sm.eval(df_data['cb_score'], df_data['label_fpd30']))
    print(sm.get_bad_rate(300, 1000, 50))


def demo_subscore():
    df_data = data_loader.DataLoader.get_score_sample_data()

    sm = score_mapping.ScoreMapping(n_bins=25, n_degree=1, score_type='subscore')
    sm.fit(df_data['prob'], df_data['label_fpd30'])

    df_data['cb_score'] = sm.transform(df_data['prob'])

    plt.figure()
    sm.plot_fitted_model()
    plt.show()

    print(sm.eval(df_data['cb_score'], df_data['label_fpd30']))
    print(sm.get_bad_rate(0, 100, 5))


def demo_customize_score():
    df_data = data_loader.DataLoader.get_score_sample_data()

    sm = score_mapping.ScoreMapping(n_bins=25, n_degree=1, score_type='customize')
    sm.fit(df_data['prob'], df_data['label_fpd30'], mapping={0: 0.12, 10: 0.001}, min_score=0, max_score=10)

    df_data['cb_score'] = sm.transform(df_data['prob'])

    plt.figure()
    sm.plot_fitted_model()
    plt.show()

    print(sm.eval(df_data['cb_score'], df_data['label_fpd30']))
    print(sm.get_bad_rate(0, 10, 1))


def main():
    demo_customize_score()


if __name__ == '__main__':
    main()
