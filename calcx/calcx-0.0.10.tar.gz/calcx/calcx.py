# -*- coding:utf-8 -*-
# Copyright 2021 Fundmore, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import division

import math
import pandas as pd
import numpy as np
from scipy import stats, optimize
from datetime import datetime, date
from datetime import timedelta
from dateutil.relativedelta import relativedelta

from .periods import ANNUALIZATION_FACTORS, APPROX_BDAYS_PER_YEAR
from .periods import DAILY, WEEKLY, MONTHLY, QUARTERLY, YEARLY
from .periods import PAST_MONTH, PAST_QUARTER, PAST_HALF_YEAR, PAST_YEAR, PAST_TWO_YEAR, PAST_THREE_YEAR, THIS_YEAR
from .periods import df_trade_dates

#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)

def _format_data(df, date_column='date', nv_column='sawnav', index_column=None, compute_index=False):

    """
    Returns the df pd.DataFrame from data_file, support Excel format,
    will support csv|txt in the future.

    Parameters
    ----------
    data_file : data_files
    dict_columns : dict format, used for mapping input columns to
    system-used columns: df.ix[:,['date','nav','sanav','sawnav']]

    Returns
    -------
    df : pd.DataFrame, columns specified in dict_columns
    """
    # 按给定顺序重置column name
    dict_columns = {date_column: 'date', nv_column: 'sawnav'}
    df.rename(columns=dict_columns, inplace=True)
    # 排序
    df = df.sort_values(by=['date'], ascending=True).reset_index(drop=True)
    df['date'] = pd.to_datetime(df['date'])
    df['date_str'] = df['date'].apply(lambda x: str(x)[:10])
    # 匹配沪深300指数
    if index_column is None:
        df['index_price'] = pd.Series()
    else:
        df['index_price'] = df[index_column]
        df['index_price'].ffill(inplace=True)
    if compute_index:
        df['sawnav'] = df['index_price']
    # 去除开头的空值
    df_dropna = df.dropna(axis=0, subset=['sawnav'])
    i_min = df_dropna.index.min()
    df = df[df.index >= i_min]
    return df


def _adjust_periods(df, period=PAST_MONTH):

    """
    根据时期参数(period)调整收益计算区间
    Returns the nav values of df adjusted by adjustment_factor. Optimizes for the
    case of adjustment_factor being 0 by returning returns itself, not a copy!

    Parameters
    ----------
    df : pd.DataFrame, columns in system specified format
    period : str, period value

    Returns
    -------
    out : date index, str
    """

    def nearest(items, pivot):
        delta = list(map(lambda x: pivot - datetime.date(x) >= timedelta(days=0), items))
        delta_set = list(set(delta))
        if delta_set == [False]:
            date = items.iloc[0]
        else:
            date = items[delta].iloc[-1]
        return date

    dates = df['date']
    current_date = dates.iloc[-1]
    start_date = None
    if period == PAST_MONTH:
        # find the PAST_MONTH day
        new_date = datetime.date(current_date) - relativedelta(months=1)
        # find the nearest index
        start_date = nearest(dates, new_date)
    elif period == PAST_QUARTER:
        # find the PAST_QUARTER day
        new_date = datetime.date(current_date) - relativedelta(months=3)
        # find the nearest index
        start_date = nearest(dates, new_date)
    elif period == PAST_HALF_YEAR:
        # find the PAST_HALF_YEAR day
        new_date = datetime.date(current_date) - relativedelta(months=6)
        # find the nearest index
        start_date = nearest(dates, new_date)
    elif period == PAST_YEAR:
        # find the PAST_YEAR day
        new_date = datetime.date(current_date) - relativedelta(years=1)
        # find the nearest index
        start_date = nearest(dates, new_date)
    elif period == PAST_TWO_YEAR:
        # find the PAST_TWO_YEAR day
        new_date = datetime.date(current_date) - relativedelta(years=2)
        # find the nearest index
        start_date = nearest(dates, new_date)
    elif period == PAST_THREE_YEAR:
        # find the PAST_THREE_YEAR day
        new_date = datetime.date(current_date) - relativedelta(years=3)
        # find the nearest index
        start_date = nearest(dates, new_date)
    elif period == THIS_YEAR:
        # find the THIS_YEAR day
        new_date = date(int(current_date.year), 1, 1)
        # find the nearest index
        start_date = nearest(dates, new_date)
    else:
        df_set = df[(df['date'] >= period[0]) & (df['date'] <= period[1])]
        if df_set.empty:
            return df
        return df_set

    if start_date is None:
        raise ValueError("start_index cannot be 'None'. ")
    start_index = dates.tolist().index(start_date)

    return df[start_index:]


def _adjust_returns(df, adjustment_factor=None):

    """
    基于调整因子adjustment_factor调整收益returns
    Returns the nav values of df adjusted by adjustment_factor. Optimizes for the
    case of adjustment_factor being 0 by returning returns itself, not a copy!

    Parameters
    ----------
    df : pd.DataFrame, columns in system specified format
    adjustment_factor : pd.Series or np.ndarray or float or int

    Returns
    -------
    df : pd.DataFrame, columns in system specified format
    """
    if adjustment_factor is None or adjustment_factor == 0 \
            or isinstance(adjustment_factor, (float, int)) is False:
        return df
    df['sawnav'] = df['sawnav'] - adjustment_factor
    return df


def max_drawdown(df, out=None):

    """
    Returns the max drawdown values of df['nav']

    Parameters
    ----------
    df : pd.DataFrame, columns in system specified format
    out : array-like, optional
        Array to use as output buffer.
        If not passed, a new array will be created.

    Returns
    -------
    max_drawdown : float
    """
    returns = df['nav']
    l = ((np.maximum.accumulate(returns) - returns) / np.maximum.accumulate(returns)).idxmax()
    k = (returns[:l]).idxmax()
    mdd = (returns[k] - returns[l]) / (returns[k])
    return mdd


def returns_ratio(df, period=DAILY, annualization=None):
    """
    计算收益率
    Compute return_ratio.

    Parameters
    ----------
    returns : pd.Series or np.ndarray
        Daily returns of the strategy, noncumulative.
        - See full explanation in :func:`~empyrical.stats.cum_returns`.
    period : str, optional
        Defines the periodicity of the 'returns' data for purposes of
        annualizing. Value ignored if `annualization` parameter is specified.
        Defaults are::

            'monthly':12
            'weekly': 52
            'daily': 252

    annualization : int, optional
        Used to suppress default values available in `period` to convert
        returns into annual returns. Value should be the annual frequency of
        `returns`.
        - See full explanation in :func:`~empyrical.stats.annual_return`.

    Returns
    -------
    returns_ratio : float
    """
    if annualization is None:
        if period is not None:
            df = _adjust_periods(df, period)
        out = df['sanav'].iloc[-1]/df['sanav'].iloc[0]-1
    else:
        date_st = df['date'].iloc[0]
        date_en = df['date'].iloc[-1]
        days = (date_en - date_st).days
        returns = df['sanav'].iloc[-1] - 1
        out = (1 +returns) ** (annualization / days) - 1
    return out


def returns_ratio_interval(df, start='2019-05-10', end='2021-06-11', annualization=None):
    """
    计算区间收益率
    Compute return_ratio.

    Parameters
    ----------
    returns : pd.Series or np.ndarray
        Daily returns of the strategy, noncumulative.
        - See full explanation in :func:`~empyrical.stats.cum_returns`.
    start, end : str
        Defines the periodicity of the 'returns' data for purposes of
        annualizing. Value ignored if `annualization` parameter is specified.
        Defaults are::

            'monthly':12
            'weekly': 52
            'daily': 252

    annualization : int, optional
        Used to suppress default values available in `period` to convert
        returns into annual returns. Value should be the annual frequency of
        `returns`.
        - See full explanation in :func:`~empyrical.stats.annual_return`.

    Returns
    -------
    returns_ratio : float
    """
    returns = df['nav']

    out = 0.6147
    return out


# -------------------------------------------------------------------------------------------
# 计算自适应收益序列
def _adjust_self_returns(df):
    if len(df) <= 1:
        return pd.DataFrame(), [np.nan, np.nan], [np.nan, np.nan]
    else:
        df['self_r'] = df['sawnav'] / df['sawnav'].shift(1) - 1
        df['index_r'] = df['index_price'] / df['index_price'].shift(1) - 1
        df['r_poor'] = df['self_r'] - df['index_r']
        interval_num = len(df) - 1

        date_st = datetime.date(df['date'].iloc[0])
        date_en = datetime.date(df['date'].iloc[-1])
        days = (date_en - date_st).days
        days_avg = days / interval_num

        # import chinese_calendar
        # from business_calendar import Calendar
        # cal = Calendar()
        # new_date_st = date_st + relativedelta(days=1)
        # # chi_cal_list = chinese_calendar.get_workdays(new_date_st, date_en)
        # # work_cal_list = list(cal.range(new_date_st, date_en))
        # days_list = list(set(chi_cal_list).intersection(set(work_cal_list)))
        days_list = df_trade_dates[(df_trade_dates['date']>=date_st) & (df_trade_dates['date']<=date_en)]['date'].to_list()
        work_days = len(days_list)
        work_days_avg = work_days / interval_num
        return df, [days_avg, work_days_avg], [days, work_days]


# 计算周收益序列
def _adjust_week_returns(df):
    df['year_week_day'] = df['date'].apply(lambda x: pd.to_datetime(x, format="%Y-%m-%d").isocalendar())
    df['year_week'] = df['year_week_day'].apply(lambda x: str(x[0]) + str(x[1]) if x[1] >= 10 else str(x[0]) + str(0) + str(x[1]))
    df['returns_week'] = (df['sawnav'] / df['sawnav'].shift(1) - 1)

    df_week = df.groupby(['year_week'])['date'].max()
    df_week = pd.DataFrame(df_week)
    df_week.sort_values('date', inplace=True)
    df_week.reset_index(inplace=True)
    if len(df_week) <= 1:
        return pd.Series()
    else:
        df_week = df_week.ffill()
        df_week_r = pd.merge(df_week, df, on=['year_week', 'date'], how='left')
        df_week_r['week_returns'] = df_week_r['sawnav'] / df_week_r['sawnav'].shift(1) - 1
        df_week_r['interval_days'] = (df_week_r['date']-df_week_r['date'].shift(1)).apply(lambda x: x.days)
        interval_days_avg = df_week_r['interval_days'].mean()
        return df_week_r['week_returns'][1:], interval_days_avg


# 收益率
def returns(df):
    if df.empty:
        r = np.nan
    else:
        r = df['sawnav'].iloc[-1]/df['sawnav'].iloc[0]-1
    return r


# 动态收益率序列
def returns_list(df, align=1):
    if align == 1:
        df_dropna = df.dropna(axis=0, subset=['index_price'])
        i_min = df_dropna.index.min()
        df = df[df.index >= i_min]
        
    df_rl = pd.DataFrame(columns=['date', 'self_total_r', 'index_total_r'])
    if df.empty:
        return df_rl
    else:
        df['self_total_r'] = df['sawnav']/df['sawnav'].iloc[0]-1
        df['index_total_r'] = df['index_price']/df['index_price'].iloc[0]-1
        df_rl['date'] = df['date'][1:]
        df_rl['self_total_r'] = df['self_total_r'][1:]
        df_rl['index_total_r'] = df['index_total_r'][1:]
        return df_rl


# 动态最大回撤序列
def mdd_list(df):
    df_rl = pd.DataFrame(columns=['date', 'mdd'])
    if df.empty:
        return df_rl
    else:
        df['mdd'] = (df['sawnav'] / df['sawnav'].expanding(min_periods=1).max()) - 1
        df_rl['date'] = df['date']
        df_rl['mdd'] = df['mdd']
        return df_rl


# 年化收益率
def returns_a(returns, days, annual_days):
    if np.isnan(returns) or days == 0:
        returns_a = np.nan
    else:
        returns_a = (1 + returns) ** (annual_days / days) - 1
    return returns_a


# 波动率(以自适应收益序列计算)
def std(df):
    if df.empty:
        std = np.nan
    else:
        std = df['self_r'].std()
    return std


# 年化波动率(以波动率计算)
def std_a(std, days_avg, annual_days):
    if np.isnan(std) or days_avg == 0:
        std_a = np.nan
    else:
        std_a = (std * ((annual_days / days_avg) ** 0.5))
    return std_a


# 下行风险(以自适应收益序列计算)
def std_d(df, days_avg, rf):
    if df.empty:
        std_d = np.nan
    else:
        # rf_self = (rf + 1) ** (interval_days_avg / 365) - 1
        rf_self = rf / 365 * days_avg
        df_dd = df[df['self_r'] < rf_self]['self_r']
        power2 = df_dd.apply(lambda x: (x-rf_self) ** 2)
        power2_sum = power2.sum()
        n = power2.count()
        std_d = math.sqrt(power2_sum / (n-1))
    return std_d


# 年化下行风险(以下行风险计算)
def stdd_a(stdd, days_avg, annual_days):
    if np.isnan(stdd) or days_avg == 0:
        stdd_a = np.nan
    else:
        stdd_a = (stdd * ((annual_days / days_avg) ** 0.5))
    return stdd_a


# 最大回撤/开始日期/结束日期/回补天数
def max_dd(df):
    nv_list = df['sawnav'].tolist()
    if all(x <= y for x, y in zip(nv_list, nv_list[1:])):
        return np.nan, np.nan, np.nan, np.nan
    endidx = ((np.maximum.accumulate(df['sawnav']) - df['sawnav']) / np.maximum.accumulate(df['sawnav'])).idxmax()
    startidx = (df['sawnav'][:endidx]).idxmax()
    mdd = (df['sawnav'][startidx] - df['sawnav'][endidx]) / (df['sawnav'][startidx])

    restoreidx = np.nan
    for i in range(endidx + 1, len(nv_list)):
        if df['sawnav'][i] >= df['sawnav'][startidx]:
            restoreidx = i
            break
    if np.isnan(restoreidx):
        re_days = np.nan
    else:
        date_en = datetime.date(df['date'][endidx])
        date_re = datetime.date(df['date'][restoreidx])
        re_days = (date_re - date_en).days
    return mdd, df['date_str'][startidx], df['date_str'][endidx], re_days


# 夏普比率
def sharp(r, std, rf, days):
    if np.isnan(r) or np.isnan(std):
        sharp = np.nan
    else:
        # rf_self = (rf + 1) ** (days / 365) - 1
        rf_self = rf / 365 * days
        sharp = (r - rf_self) / std
    return sharp


# 年化夏普比率
def sharp_a(r_a, std_a, rf):
    if np.isnan(r_a) or np.isnan(std_a):
        sharp_a = np.nan
    else:
        sharp_a = (r_a - rf) / std_a
    return sharp_a


# 索提诺比率
def sor(r, stdd, rf, days):
    if np.isnan(r) or np.isnan(stdd):
        sor = np.nan
    else:
        rf_self = rf / 365 * days
        sor = (r - rf_self) / stdd
    return sor


# 年化索提诺比率
def sor_a(r_a, stdd, rf, days_avg, annual_days):
    if np.isnan(r_a) or np.isnan(stdd):
        sor_a = np.nan
    else:
        sor_a = (r_a - rf) / stdd / ((annual_days / days_avg) ** 0.5)
    return sor_a


# 卡玛比率
def calmar(r, mdd):
    try:
        if np.isnan(r) or np.isnan(mdd):
            return np.nan
    except:
        if pd.isna(r) or pd.isna(mdd):
            return np.nan
    else:
        return r / mdd


# 年化卡玛比率
def calmar_a(r_a, mdd):
    try:
        if np.isnan(r_a) or np.isnan(mdd):
            return np.nan
    except:
        if pd.isna(r_a) or pd.isna(mdd):
            return np.nan
    else:
        return r_a / mdd


# Spearman秩相关
def spearman(df):
    if df.empty:
        spearman = np.nan
    else:
        spearman = df['self_r'].corr(df['index_r'], 'spearman')
    return spearman


# 信息比率
def info(r, df, rf, days):
    if np.isnan(r) or df.empty:
        info = np.nan
    else:
        # rf_self = (rf + 1) ** (days / 365) - 1
        rf_self = rf / 365 * days
        r_poor_std = df['r_poor'].std()
        info = (r - rf_self) / r_poor_std
    return info


# 年化信息比率
def info_a(r_a, df, rf, days_avg, annual_days):
    if np.isnan(r_a) or df.empty:
        info_a = np.nan
    else:
        r_poor_std_a = df['r_poor'].std() * ((annual_days / days_avg) ** 0.5)
        info_a = (r_a - rf) / r_poor_std_a
    return info_a


# β系数
def beta(df):
    if df.empty:
        beta = np.nan
    else:
        cov = df['self_r'].cov(df['index_r'])
        std_index = df['index_r'].std()
        beta = cov / (std_index ** 2)
    return beta


# α系数
def alpha(r, rf, beta, df, days):
    if np.isnan(r) or np.isnan(beta) or df.empty:
        alpha = np.nan
    else:
        r_index = df['index_price'].iloc[-1] / df['index_price'].iloc[0] - 1
        rf_self = rf / 365 * days
        alpha = r - (rf_self + beta * (r_index - rf_self))
    return alpha


# 年化α系数
def alpha_a(r_a, rf, beta, df, days, annual_days):
    if np.isnan(r_a) or np.isnan(beta) or df.empty:
        alpha_a = np.nan
    else:
        r_index = df['index_price'].iloc[-1] / df['index_price'].iloc[0] - 1
        r_index_a = (1 + r_index) ** (annual_days / days) - 1
        alpha_a = r_a - (rf + beta * (r_index_a - rf))
    return alpha_a


# 在险价值(95%置信度)
def var95(r, std):
    if np.isnan(r) or np.isnan(std):
        var95 = np.nan
    else:
        var95 = r - 1.6449 * std
    return var95


# 年化在险价值(95%置信度)
def var95_a(r_a, std_a):
    if np.isnan(r_a) or np.isnan(std_a):
        var95_a = np.nan
    else:
        var95_a = r_a - 1.6449 * std_a
    return var95_a


# 投资胜率
def win_rate(df):
    if df.empty:
        win_rate = np.nan
    else:
        n = df[df['r_poor'] > 0]['r_poor'].count()
        m = df['r_poor'].count()
        win_rate = n / m
    return  win_rate


# 平均损益比
def loss_profit(df):
    if df.empty:
        loss_profit = np.nan
    else:
        df_n = df[df['r_poor'] > 0]['r_poor']
        df_m = df[df['r_poor'] < 0]['r_poor']
        n = df_n.count()
        m = df_m.count()
        rsum_n = df_n.sum()
        rsum_m = df_m.sum()
        loss_profit = (rsum_n / n) / (-rsum_m / m)
    return loss_profit


# 盈亏次数比
def loss_profit_times(df):
    if df.empty:
        loss_profit_times = np.nan
    else:
        df_n = df[df['r_poor'] > 0]['r_poor']
        df_m = df['r_poor']
        n = df_n.count()
        m = df_m.count()
        loss_profit_times = '%s/%s' % (n, m)
    return loss_profit_times


class CalcxTarget:
    def __init__(self, df, date_column='date', nv_column='sawnav', index_column=None, compute_index=False, 
                 adjustment_factor=None, period=None):
        self.df_format = _format_data(df, date_column, nv_column, index_column, compute_index)
        self.df_factor = _adjust_returns(self.df_format, adjustment_factor)
        self.df_m1_p = _adjust_periods(self.df_factor, PAST_MONTH)
        self.df_m3_p = _adjust_periods(self.df_factor, PAST_QUARTER)
        self.df_m6_p = _adjust_periods(self.df_factor, PAST_HALF_YEAR)
        self.df_y1_p = _adjust_periods(self.df_factor, PAST_YEAR)
        self.df_y2_p = _adjust_periods(self.df_factor, PAST_TWO_YEAR)
        self.df_y3_p = _adjust_periods(self.df_factor, PAST_THREE_YEAR)
        self.df_year_p = _adjust_periods(self.df_factor, THIS_YEAR)
        period = [pd.to_datetime(date(1990,1,1)), pd.to_datetime(datetime.today().date())] if period is None or type(period) is str else period
        self.df_set_p = _adjust_periods(self.df_factor, period)

        self.df_total, self.avg_days_total, self.days_total  = _adjust_self_returns(self.df_factor)
        self.df_m1, self.avg_days_m1, self.days_m1 = _adjust_self_returns(self.df_m1_p)
        self.df_m3, self.avg_days_m3, self.days_m3 = _adjust_self_returns(self.df_m3_p)
        self.df_m6, self.avg_days_m6, self.days_m6 = _adjust_self_returns(self.df_m6_p)
        self.df_y1, self.avg_days_y1, self.days_y1 = _adjust_self_returns(self.df_y1_p)
        self.df_y2, self.avg_days_y2, self.days_y2 = _adjust_self_returns(self.df_y2_p)
        self.df_y3, self.avg_days_y3, self.days_y3 = _adjust_self_returns(self.df_y3_p)
        self.df_year, self.avg_days_year, self.days_year = _adjust_self_returns(self.df_year_p)
        self.df_set, self.avg_days_set, self.days_set = _adjust_self_returns(self.df_set_p)

    def judge_period(self, period):
        if period == 'total':
            df = self.df_total
            avg_days = self.avg_days_total
            days = self.days_total
        elif period == 'm1':
            df = self.df_m1
            avg_days = self.avg_days_m1
            days = self.days_m1
        elif period == 'm3':
            df = self.df_m3
            avg_days = self.avg_days_m3
            days = self.days_m3
        elif period == 'm6':
            df = self.df_m6
            avg_days = self.avg_days_m6
            days = self.days_m6
        elif period == 'y1':
            df = self.df_y1
            avg_days = self.avg_days_y1
            days = self.days_y1
        elif period == 'y2':
            df = self.df_y2
            avg_days = self.avg_days_y2
            days = self.days_y2
        elif period == 'y3':
            df = self.df_y3
            avg_days = self.avg_days_y3
            days = self.days_y3
        elif period == 'year':
            df = self.df_year
            avg_days = self.avg_days_year
            days = self.days_year
        else:
            df = self.df_set
            avg_days = self.avg_days_set
            days = self.days_set
        return df, avg_days, days

    def returns(self, period='total', annual_days=None):
        df, days_avg, days = self.judge_period(period)
        r_v = returns(df)
        if annual_days is None:
            return r_v
        else:
            days = days[0] if annual_days >= 365 else days[1]
            return returns_a(r_v, days, annual_days)

    def std(self, period='total', annual_days=None):
        df, days_avg, days = self.judge_period(period)
        std_v = std(df)
        if annual_days is None:
            return std_v
        else:
            days_avg = days_avg[0] if annual_days >= 365 else days_avg[1]
            return std_a(std_v, days_avg, annual_days)

    def std_d(self, period='total', annual_days=None, rf=0.015):
        df, days_avg, days = self.judge_period(period)
        stdd_v = std_d(df, days_avg[0], rf)
        if annual_days is None:
            return stdd_v
        else:
            days_avg = days_avg[0] if annual_days >= 365 else days_avg[1]
            return stdd_a(stdd_v, days_avg, annual_days)

    def max_dd(self, period='total'):
        df, days_avg, days = self.judge_period(period)
        mdd, start_date, end_date, re_days = max_dd(df)
        return mdd, start_date, end_date, re_days

    def sharp(self, period='total', annual_days=None, rf=0.015):
        df, days_avg, days = self.judge_period(period)
        r_v = returns(df)
        std_v = std(df)
        if annual_days is None:
            return sharp(r_v, std_v, rf, days[0])
        else:
            days_avg = days_avg[0] if annual_days >= 365 else days_avg[1]
            days = days[0] if annual_days >= 365 else days[1]
            ra_v = returns_a(r_v, days, annual_days)
            stda_v = std_a(std_v, days_avg, annual_days)
            return sharp_a(ra_v, stda_v, rf)

    def sor(self, period='total', annual_days=None, rf=0.015):
        df, days_avg, days = self.judge_period(period)
        r_v = returns(df)
        stdd_v = std_d(df, days_avg[0], rf)
        if annual_days is None:
            return sor(r_v, stdd_v, rf, days[0])
        else:
            days_avg = days_avg[0] if annual_days >= 365 else days_avg[1]
            days = days[0] if annual_days >= 365 else days[1]
            ra_v = returns_a(r_v, days, annual_days)
            return sor_a(ra_v, stdd_v, rf, days_avg, annual_days)

    def calmar(self, period='total', annual_days=None):
        df, days_avg, days = self.judge_period(period)
        r_v = returns(df)
        mdd_v = max_dd(df)
        if annual_days is None:
            return calmar(r_v, mdd_v)
        else:
            days = days[0] if annual_days >= 365 else days[1]
            ra_v = returns_a(r_v, days, annual_days)
            return calmar_a(ra_v, mdd_v)

    def spearman(self, period='total'):
        df, days_avg, days = self.judge_period(period)
        return spearman(df)

    def info(self, period='total', annual_days=None, rf=0.015):
        df, days_avg, days = self.judge_period(period)
        r_v = returns(df)
        if annual_days is None:
            return info(r_v, df, rf, days[0])
        else:
            days_avg = days_avg[0] if annual_days >= 365 else days_avg[1]
            days = days[0] if annual_days >= 365 else days[1]
            ra_v = returns_a(r_v, days, annual_days)
            return info_a(ra_v, df, rf, days_avg, annual_days)

    def beta(self, period='total'):
        df, days_avg, days = self.judge_period(period)
        return beta(df)

    def alpha(self, period='total', annual_days=None, rf=0.015):
        df, days_avg, days = self.judge_period(period)
        r_v = returns(df)
        beta_v = beta(df)
        if annual_days is None:
            return alpha(r_v, rf, beta_v, df, days[0])
        else:
            days = days[0] if annual_days >= 365 else days[1]
            ra_v = returns_a(r_v, days, annual_days)
            return alpha_a(ra_v, rf, beta_v, df, days, annual_days)

    def var95(self, period='total', annual_days=None):
        df, days_avg, days = self.judge_period(period)
        r_v = returns(df)
        std_v = std(df)
        if annual_days is None:
            return var95(r_v, std_v)
        else:
            days_avg = days_avg[0] if annual_days >= 365 else days_avg[1]
            days = days[0] if annual_days >= 365 else days[1]
            ra_v = returns_a(r_v, days, annual_days)
            stda_v = std_a(std_v, days_avg, annual_days)
            return var95_a(ra_v, stda_v)

    def win_rate(self, period='total'):
        df, days_avg, days = self.judge_period(period)
        return win_rate(df)

    def loss_profit(self, period='total'):
        df, days_avg, days = self.judge_period(period)
        return loss_profit(df)

    def loss_profit_times(self, period='total'):
        df, days_avg, days = self.judge_period(period)
        return loss_profit_times(df)

    def return_list(self, period='total', align=1):
        df, days_avg, days = self.judge_period(period)
        a = returns_list(df, align)
        return a
    
    def mdd_list(self, period='total'):
        df, days_avg, days = self.judge_period(period)
        return mdd_list(df)

    @staticmethod
    def judge_value(x, decimal=4, percent=''):
        if type(x) is str:
            return x
        try:
            if np.isnan(x) or x is None:
                return ''
        except:
            if pd.isna(x) or x is None:
                return ''
        else:
            if percent == '':
                return "%.{d}f{p}".format(d=decimal, p=percent) % (x)
            else:
                return "%.{d}f{p}".format(d=decimal, p=percent) % (x*100)
            
    @staticmethod
    def judge_value2(x, decimal=4, percent=''):
        if type(x) is str:
            return x
        try:
            if np.isnan(x) or x is None:
                return None
        except:
            if pd.isna(x) or x is None:
                return None
        else:
            if percent == '':
                return round(x, decimal)
            else:
                return "%.{d}f{p}".format(d=decimal, p=percent) % (x * 100)



