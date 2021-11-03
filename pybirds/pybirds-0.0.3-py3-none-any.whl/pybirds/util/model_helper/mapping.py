__version__ = 'v1.1.0'
__author__ = ['Liang Junzhe', 'Chen Siqi']

"""
v1.1.0
new features:
1. refactor v1 code to be OOP and simplify the interface
2. update mega-score and sub-score mapping base
3. adjust the minimum risk
4. add transform_online function
5. add plot and compare_calibrate_result functions
"""


import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.base import TransformerMixin


class Calibration(TransformerMixin):
    """
    A score calibration helper.

    Score Types
    -----------
    'megascore':
         mega-score calibration applies to Ascore and Bscore
         score scale 300~1000, 850 -> 0.1%, 500 -> 12.8%

    'subscore':
         sub-score calibration applies to the sub-score of Ascore and Bscore
         score scale 0~100, 95 -> 0.1%, 10 -> 12.8%

    'self-defining':
         self-defining score scale
         must input mapping_base, score_cap, score_floor in fit

    'probability':
         only calibrate probability

    Notes
    -----
    Must check the probability calibration process:
         calling Calibration.calibrate_detail and Calibration.get_calibrate_plot()

    Must check the distribution and risk level of calibration results:
         calling Calibration.compare_calibrate_result(df_score, df_label)

    """

    def __init__(self, **kwargs):
        self.version = 'v1.1.0'

        self.n_bins = kwargs.get('n_bins', 25)
        self.n_degree = kwargs.get('n_degree', 1)
        self.score_type = kwargs.get('score_type', None)

        self.mapping_base = None
        self.score_cap = None
        self.score_floor = None

        self.calibrate_detail = None
        self.calibrate_coef = None
        self.mapping_intercept = None
        self.mapping_slope = None

    def fit(self, df_prob, df_label, **kwargs):
        mapping_base = kwargs.get('mapping_base', None)
        score_cap = kwargs.get('score_cap', None)
        score_floor = kwargs.get('score_floor', None)

        if mapping_base is not None:
            self.score_type = 'self-defining'
            logging.warning('self-defining score type, input mapping_base, score_cap, and score_floor')
            self.mapping_base, self.score_cap, self.score_floor = mapping_base, score_cap, score_floor
            self.mapping_slope, self.mapping_intercept = self.__set_mapping_base(self.mapping_base)

        elif self.score_type == 'probability':
            logging.warning('probability score type, only probability calibration')

        elif self.score_type in ['megascore', 'subscore']:
            self.mapping_base, self.score_cap, self.score_floor = self.__set_default_score_base(self.score_type)
            self.mapping_slope, self.mapping_intercept = self.__set_mapping_base(self.mapping_base)

        else:
            raise Exception('unknown score type, expect megascore, subscore, probability, and self-defining')

        lst_prob = self.__check_type(df_prob)
        lst_label = self.__check_type(df_label)

        df_data = pd.DataFrame({'yprob': lst_prob, 'label': lst_label,
                                'lnodds_prob': [self.prob2lnodds(x) for x in lst_prob]})
        df_data['lnodds_prob_bin'] = pd.qcut(df_data['lnodds_prob'], self.n_bins, duplicates='drop')

        df_cal = df_data.groupby('lnodds_prob_bin').agg(total_user=('label', 'count'),
                                                        bad_rate=('label', 'mean'),
                                                        lnodds_prob_mean_x=('lnodds_prob', 'mean'))
        df_cal['adj_bad_rate'] = df_cal.apply(lambda x: max(x['bad_rate'], 1 / x['total_user'], 0.0001), axis=1)
        df_cal['lnodds_bad_rate_y'] = df_cal['adj_bad_rate'].apply(lambda x: self.prob2lnodds(x))

        lst_col = ['total_user', 'bad_rate', 'adj_bad_rate', 'lnodds_prob_mean_x', 'lnodds_bad_rate_y']
        self.calibrate_detail = df_cal[lst_col]
        self.calibrate_coef = np.polyfit(df_cal['lnodds_prob_mean_x'], df_cal['lnodds_bad_rate_y'], self.n_degree)
        return self

    def transform(self, df_prob):
        lst_prob = self.__check_type(df_prob)
        lst_lnodds_prob = [self.prob2lnodds(x) for x in lst_prob]
        lst_lnodds_cal_prob = [np.poly1d(self.calibrate_coef)(x) for x in lst_lnodds_prob]
        print(lst_lnodds_cal_prob[0:10])
        if self.score_type == 'probability':
            lst_cal_prob = [self.lnodds2prob(x) for x in lst_lnodds_cal_prob]
            return lst_cal_prob

        else:
            lst_score = [self.mapping_intercept + self.mapping_slope * x for x in lst_lnodds_cal_prob]
            #print(lst_score)
            lst_score = [max(x, self.score_floor) for x in lst_score]
            lst_score = [min(x, self.score_cap) for x in lst_score]
            return lst_score

    @classmethod
    def transform_online(cls, pred, calibrate_coef, mapping_intercept, mapping_slope, score_cap, score_floor):
        calibrate_intercept = calibrate_coef[1]
        calibrate_slope = calibrate_coef[0]

        lnodds = calibrate_intercept + calibrate_slope * cls.prob2lnodds(pred)
        score = mapping_intercept + mapping_slope * lnodds
        score = max(score, score_floor)
        score = min(score, score_cap)
        return score

    def compare_calibrate_result(self, df_score, df_label, **kwargs):
        bins = kwargs.get('bins', None)

        if bins is None:
            if self.score_type == 'megascore':
                bins = [0, 300, 400, 500, 550, 600, 650, 700, 750, 800, 850, 1000]
            elif self.score_type == 'subscore':
                bins = [0, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
            else:
                raise Exception('input bins')

        lst_score = self.__check_type(df_score)
        lst_label = self.__check_type(df_label)
        df_data = pd.DataFrame({'score': lst_score, 'label': lst_label})
        df_data['score_bin'] = pd.cut(df_data['score'], bins)

        df_res = df_data.groupby('score_bin').agg(total_user=('label', 'count'), bad_rate=('label', 'mean'))
        df_res = df_res.reset_index()
        df_res['score_max'] = df_res['score_bin'].apply(lambda x: x.right)

        if self.score_type == 'probability':
            df_res['exp_bad_rate'] = df_res['score_max']
        else:
            df_res['exp_bad_rate'] = df_res['score_max'].apply(
                lambda x: self.lnodds2prob((x - self.mapping_intercept) / self.mapping_slope))

        lst_col = ['score_bin', 'score_max', 'total_user', 'bad_rate', 'exp_bad_rate']
        df_res = df_res[lst_col]
        return df_res

    def get_bad_rate(self, score_min, score_max, step):
        if self.score_type == 'probability':
            raise Exception('probability score type, no score mapping process')

        ary_score = np.arange(score_min, score_max, step)
        ary_lnodds = (ary_score - self.mapping_intercept) / self.mapping_slope
        ary_bad_rate = self.lnodds2prob(ary_lnodds)
        return pd.DataFrame({'score': ary_score, 'bad_rate': ary_bad_rate, 'lnodds': ary_lnodds})

    def get_calibrate_plot(self):
        x = self.calibrate_detail['lnodds_prob_mean_x']
        y_actual = self.calibrate_detail['lnodds_bad_rate_y']

        y_pred = np.poly1d(self.calibrate_coef)(x)
        f, ax = plt.subplots(figsize=(8, 6))
        ax.plot(x, y_actual, 'o', x, y_pred, '-', label='1d')
        ax.set_xlabel('lnodds_prob_mean'), ax.set_ylabel('lnodds_bad_rate')
        return ax

    @classmethod
    def __set_default_score_base(cls, score_type):
        if score_type == 'megascore':
            mapping_base = {
                500: 0.128,
                550: 0.0671,
                600: 0.0341,
                650: 0.017,
                700: 0.0084,
                750: 0.0041,
                800: 0.002,
                850: 0.001
            }
            score_cap = 1000
            score_floor = 300

        elif score_type == 'subscore':
            mapping_base = {
                10: 0.128,
                15: 0.0987,
                20: 0.0755,
                25: 0.0574,
                30: 0.0434,
                35: 0.0327,
                40: 0.0246,
                45: 0.0185,
                50: 0.0138,
                55: 0.0104,
                60: 0.0077,
                65: 0.0058,
                70: 0.0043,
                75: 0.0032,
                80: 0.0024,
                85: 0.0018,
                90: 0.0013,
                95: 0.001
            }
            score_cap = 100
            score_floor = 0

        else:
            raise Exception('unknown score type, only megascore and subscore available')

        return mapping_base, score_cap, score_floor

    @classmethod
    def __set_mapping_base(cls, dict_base):
        lst_score = sorted(dict_base.keys())
        lst_bad_rate = sorted(dict_base.values(), reverse=True)
        lst_lnodds_bad_rate = [cls.prob2lnodds(x) for x in lst_bad_rate]

        score_max, score_min = lst_score[-1], lst_score[0]
        lnodds_max, lnodds_min = lst_lnodds_bad_rate[-1], lst_lnodds_bad_rate[0]

        slope = (score_max - score_min) / (lnodds_max - lnodds_min)
        intercept = score_max - slope * lnodds_max
        return slope, intercept

    @classmethod
    def __check_type(cls, data):
        if isinstance(data, (list, pd.Series, np.ndarray)):
            lst_data = list(data)
        elif isinstance(data, pd.DataFrame):
            lst_data = data[data.columns.item()].tolist()
        else:
            raise TypeError('Expected data type: DataFrame, List, Series or Array')
        return lst_data

    @classmethod
    def prob2lnodds(cls, prob):
        if prob == 0:
            lnodds = np.log(np.finfo(float).eps)
        elif prob == 1:
            lnodds = np.log(prob / (1 - prob + np.finfo(float).eps))
        else:
            lnodds = np.log(prob / (1 - prob))
        return lnodds

    @classmethod
    def lnodds2prob(cls, lnodds):
        prob = 1 - 1 / (np.exp(lnodds) + 1)
        return prob


def demo_megascore(df_pred, df_label):
    calibrator = Calibration(n_bins=25, n_degree=1, score_type='megascore')
    calibrator.fit(df_pred, df_label)
    df_pred['megascore'] = calibrator.transform(df_pred)


def demo_subscore(df_pred, df_label):
    calibrator = Calibration(n_bins=25, n_degree=1, score_type='subscore')
    calibrator.fit(df_pred, df_label)
    df_pred['subscore'] = calibrator.transform(df_pred)


def demo_probability(df_pred, df_label):
    calibrator = Calibration(n_bins=25, n_degree=1, score_type='probability')
    calibrator.fit(df_pred, df_label)
    df_pred['probability'] = calibrator.transform(df_pred)


def demo_self_defining(df_pred, df_label, dict_mapping_base, score_cap, score_floor):
    calibrator = Calibration(n_bins=25, n_degree=1)
    calibrator.fit(df_pred, df_label,
                   mapping_base=dict_mapping_base,
                   score_cap=score_cap, score_floor=score_floor)
    df_pred['score'] = calibrator.transform(df_pred)
