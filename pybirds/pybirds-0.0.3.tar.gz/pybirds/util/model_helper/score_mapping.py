# -*- coding: utf-8 -*-
__version__ = 'v1.0.0'
__author__ = ['Ouyang Ruofei']

"""

fit

transform

"""

import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.base import TransformerMixin


class Config:
    subscore_mapping = {
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

    megascore_mapping = {
        500: 0.128,
        550: 0.0671,
        600: 0.0341,
        650: 0.017,
        700: 0.0084,
        750: 0.0041,
        800: 0.002,
        850: 0.001
    }

    subscore_bins = [0, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
    megascore_bins = [0, 300, 400, 500, 550, 600, 650, 700, 750, 800, 850, 1000]


class ScoreMapping(TransformerMixin):
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
        """

        :param kwargs:
               n_bins
               n_degree
               score_type

               mapping
               max_score
               min_score

               detail
               coef
               slop
               intercept
        """

        self.n_bins = kwargs.get('n_bins', 25)
        self.n_degree = kwargs.get('n_degree', 1)
        self.score_type = kwargs.get('score_type', None)

        self.mapping = None
        self.max_score = None
        self.min_score = None

        self.detail = None
        self.coef = None
        self.slope = None
        self.intercept = None

    def fit(self, df_prob, df_label, **kwargs):
        """

        :param df_prob:
        :param df_label:
        :param kwargs:
        :return:
        """

        self.__config_mapping(**kwargs)

        lst_prob = self.__check_type(df_prob)
        lst_label = self.__check_type(df_label)

        """
        get df_data with following format:
        --------
        yprob label  lnodds_prob       lnodds_prob_bin
        0.1   0      ln(0.1/(1-0.1))   bin1
        0.5   1      ln(0.5/(1-0.5))   bin2
        --------
        
        """
        df_data = pd.DataFrame({'yprob': lst_prob, 'label': lst_label,
                                'lnodds_prob': [self.__prob2lnodds(x) for x in lst_prob]})
        df_data['lnodds_prob_bin'] = pd.qcut(df_data['lnodds_prob'], self.n_bins, duplicates='drop')

        """
        stat df_data as df_cal with following format:
        --------
        lnodds_prob_bin total_user  bad_rate  adj_bad_rate lnodds_prob_mean_x lnodds_bad_rate_y
        bin1            100         0.2       0.2          mean(lnodd)        ln(0.2/(1-0.2))
        bin2            10          0.1       0.1          mean(lnodd)        ln(0.1/(1-0.1))
        --------

        """
        df_cal = df_data.groupby('lnodds_prob_bin').agg(total_user=('label', 'count'),
                                                        bad_rate=('label', 'mean'),
                                                        lnodds_prob_mean_x=('lnodds_prob', 'mean'))
        # adjust bad rate when there is no bad cases: max(bad_rate, 1 / total, 0.0001)
        df_cal['adj_bad_rate'] = df_cal.apply(lambda x: max(x['bad_rate'], 1 / x['total_user'], 0.0001), axis=1)
        # convert adjusted bad rate to lnodd
        df_cal['lnodds_bad_rate_y'] = df_cal['adj_bad_rate'].apply(lambda x: self.__prob2lnodds(x))

        lst_col = ['total_user', 'bad_rate', 'adj_bad_rate', 'lnodds_prob_mean_x', 'lnodds_bad_rate_y']
        self.detail = df_cal[lst_col]

        # do polinomial fit to smooth the lnodd
        self.coef = np.polyfit(df_cal['lnodds_prob_mean_x'], df_cal['lnodds_bad_rate_y'], self.n_degree)

        return self

    def transform(self, df_prob):
        """

        :param df_prob:
        :return:
        """

        lst_prob = self.__check_type(df_prob)
        # convert prob to lnodd
        lst_lnodds_prob = [self.__prob2lnodds(x) for x in lst_prob]
        # smooth the lnodd using fitted model
        lst_lnodds_cal_prob = [np.poly1d(self.coef)(x) for x in lst_lnodds_prob]

        if self.score_type == 'probability':
            # convert back lnodd to prob
            lst_cal_prob = [self.__lnodds2prob(x) for x in lst_lnodds_cal_prob]
            return lst_cal_prob

        else:
            # get score = slope*lnodd+intercept
            lst_score = [self.slope * x + self.intercept for x in lst_lnodds_cal_prob]
            lst_score = [max(x, self.min_score) for x in lst_score]
            lst_score = [min(x, self.max_score) for x in lst_score]
            return lst_score

    @classmethod
    def transform_online(cls, pred, coef, slope, intercept, min_score, max_score):
        """

        :param pred:
        :param coef:
        :param slope:
        :param intercept:
        :param min_score:
        :param max_score:
        :return:
        """

        # get prob to lnodd and smooth with model
        coef_slope, coef_intercept = coef[0], coef[1]
        lnodds = coef_slope * cls.__prob2lnodds(pred) + coef_intercept

        # convert lnodd to score
        score = slope * lnodds + intercept
        score = max(score, min_score)
        score = min(score, max_score)
        return score

    def eval(self, df_score, df_label, **kwargs):
        """

        :param df_score:
        :param df_label:
        :param kwargs:
        :return:
        """

        bins = kwargs.get('bins', None)

        if bins is None:
            if self.score_type == 'megascore':
                bins = Config.megascore_bins
            elif self.score_type == 'subscore':
                bins = Config.subscore_bins
            else:
                bins = np.arange(self.min_score, 1.1*self.max_score, (self.max_score-self.min_score)/10)
                print(bins)

        lst_score = self.__check_type(df_score)
        lst_label = self.__check_type(df_label)

        df_data = pd.DataFrame({'score': lst_score, 'label': lst_label})
        df_data['score_bin'] = pd.cut(df_data['score'], bins)

        df_res = df_data.groupby('score_bin').agg(total_user=('label', 'count'),
                                                  bad_user=('label', 'sum'),
                                                  bad_rate=('label', 'mean'))
        df_res = df_res.reset_index()
        df_res['max_score'] = df_res['score_bin'].apply(lambda x: x.right)

        if self.score_type == 'probability':
            df_res['exp_bad_rate'] = df_res['max_score']
        else:
            df_res['exp_bad_rate'] = df_res['max_score'].apply(
                lambda x: self.__lnodds2prob((x - self.intercept) / self.slope))

        lst_col = ['score_bin', 'max_score', 'total_user', 'bad_user', 'bad_rate', 'exp_bad_rate']
        df_res = df_res[lst_col]
        return df_res

    def get_bad_rate(self, min_score, max_score, step):
        """

        :param min_score:
        :param max_score:
        :param step:
        :return:
        """

        if self.score_type == 'probability':
            raise Exception('probability score type, no score mapping process')

        ary_score = np.arange(min_score, max_score, step)
        ary_lnodds = (ary_score - self.intercept) / self.slope
        ary_bad_rate = self.__lnodds2prob(ary_lnodds)
        return pd.DataFrame({'score': ary_score, 'bad_rate': ary_bad_rate, 'lnodds': ary_lnodds})

    def plot_fitted_model(self):
        """

        :return:
        """

        x = self.detail['lnodds_prob_mean_x']
        y_actual = self.detail['lnodds_bad_rate_y']
        y_pred = np.poly1d(self.coef)(x)

        f, ax = plt.subplots(figsize=(8, 6))
        ax.plot(x, y_actual, 'o', x, y_pred, '-', label='1d')
        ax.set_xlabel('lnodds_prob_mean'), ax.set_ylabel('lnodds_bad_rate')

        return ax

    def __config_mapping(self, **kwargs):
        mapping = kwargs.get('mapping', None)
        max_score = kwargs.get('max_score', None)
        min_score = kwargs.get('min_score', None)

        if self.score_type == 'customize':
            if mapping is None:
                raise ValueError('customize score type, input mapping, max_score, and min_score')

            logging.warning('customize score type, be careful of your mapping')

            self.score_type = 'customize'
            self.mapping, self.min_score, self.max_score = mapping, min_score, max_score
            self.slope, self.intercept = self.__get_slope_and_intercept(self.mapping)

        elif self.score_type == 'probability':
            logging.warning('probability score type, only do probability calibration')

        elif self.score_type in ['megascore', 'subscore']:
            self.mapping, self.min_score, self.max_score = self.__set_default_mapping(self.score_type)
            self.slope, self.intercept = self.__get_slope_and_intercept(self.mapping)

        else:
            raise Exception('unknown score type, expect megascore, subscore, probability, and customize')

    @classmethod
    def __set_default_mapping(cls, score_type):
        if score_type == 'megascore':
            mapping = Config.megascore_mapping
            min_score, max_score = 300, 1000

        elif score_type == 'subscore':
            mapping = Config.subscore_mapping
            min_score, max_score = 0, 100

        else:
            raise Exception('unknown score type, only megascore and subscore available')

        return mapping, min_score, max_score

    @classmethod
    def __get_slope_and_intercept(cls, mapping):
        # get mapping for score and bad rate, convert to lnodd
        lst_score = sorted(mapping.keys())
        lst_bad_rate = sorted(mapping.values(), reverse=True)
        lst_lnodds_bad_rate = [cls.__prob2lnodds(x) for x in lst_bad_rate]

        # compute slope and intercept
        min_score, max_score = lst_score[0], lst_score[-1]
        min_lnodds, max_lnodds = lst_lnodds_bad_rate[0], lst_lnodds_bad_rate[-1]
        slope = (max_score - min_score) / (max_lnodds - min_lnodds)
        intercept = max_score - slope * max_lnodds

        return slope, intercept

    @classmethod
    def __prob2lnodds(cls, prob):
        if prob == 0:
            lnodds = np.log(np.finfo(float).eps)
        elif prob == 1:
            lnodds = np.log(prob / (1 - prob + np.finfo(float).eps))
        else:
            lnodds = np.log(prob / (1 - prob))
        return lnodds

    @classmethod
    def __lnodds2prob(cls, lnodds):
        prob = 1 - 1 / (np.exp(lnodds) + 1)
        return prob

    @classmethod
    def __check_type(cls, data):
        if isinstance(data, (list, pd.Series, np.ndarray)):
            lst_data = list(data)
        elif isinstance(data, pd.DataFrame):
            lst_data = data[data.columns.item()].tolist()
        else:
            raise TypeError('Expected data type: DataFrame, List, Series or Array')
        return lst_data
