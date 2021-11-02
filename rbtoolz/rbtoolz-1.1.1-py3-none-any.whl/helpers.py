#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Helper functions primarily for data analysis
"""


__author__ = 'Ross Bonallo'
__license__ = 'MIT Licence'
__version__ = '1.1.0'


import pandas as pd
import numpy as np
import pytz
from datetime import datetime, timedelta
from rbtoolz.plotting import auto_plot


def seag(_df, period='Y', agg='sum', realign_month=None):
    if isinstance(_df, pd.Series):
        df = pd.DataFrame(_df).copy()
    else:
        df = _df.copy()

    year_now = datetime.today().year
    max_year = df.index.max().year
    # E.g Sum/Win chart we would like to reset on 1st April. Realign Month = 4.
    realign_day = None
    if realign_month:
        realign_day = datetime(year_now, realign_month, 1)
        day_diff = (datetime(year_now,1,1,) - datetime(year_now-1, realign_month, 1)).days
        df.index = df.index + timedelta(days=day_diff)

    if agg == 'mean':
        agg_func = np.mean
    else:
        agg_func = np.sum

    if period == 'M':
        _df = pd.pivot_table(df, index=df.index.day, columns=df.index.month,
                aggfunc=agg_func, fill_value=np.nan)

    elif period == 'W':
        _df = pd.pivot_table(df, index=df.index.dayofweek, columns=df.index.year,
                aggfunc=agg_func, fill_value=np.nan)

    elif period == 'WA':
        _df = pd.pivot_table(df, index=df.index.week, columns=df.index.year,
                aggfunc=agg_func, fill_value=np.nan)

    elif period == 'Y':
        _df = pd.pivot_table(df, index=df.index.dayofyear, columns=df.index.year,
                aggfunc=agg_func, fill_value=np.nan)

    else:
        raise(Exception('Period {} not available'.format(period)))

    _df = _df.droplevel(0, axis=1)

    cols = _df.columns.values[:-1]

    for c in cols:
        _df[c] = _df[c].fillna(method='ffill')

    if realign_month:
        dt_index = [realign_day + timedelta(days=i) for i in range(len(_df.index))]
        _df.index = dt_index

        last_column = _df.columns[-1]

        if last_column > max_year:
            year_diff = last_column - max_year
            _df.columns = [y-year_diff for y in _df.columns]

    return _df


def savgolay(df, period=5, order=2):
    from scipy.signal import savgol_filter
    return df.apply(lambda s: savgol_filter(s, period, order))


def annualize(rate,period):
    return ((1. + rate)**period)-1.


def deannualize(rate,period):
    return ((rate + 1.)**(1./period))-1.


flatten = lambda t: [item for sublist in t for item in sublist]


def drop_duplicates(df):
    return df.loc[~df.index.duplicated()]


def to_date(dt=datetime.today()):
    try:
        return datetime(dt.year, dt.month, dt.day)
    except:
        return dt


def get_today_trace(_min, _max, applicable_at=None):
    dt = applicable_at if applicable_at else to_date(datetime.today())
    df = pd.DataFrame([_min,_max], [dt,dt])
    df.columns=['Today']
    today_trace = auto_plot(df, colors_override=['red'],as_traces=True)
    return today_trace


def bump_months(dt=datetime.today(), bumps=0, day=1, keep_days=False):
    month_bump = dt.month + bumps
    if month_bump > 12:
        month_bump, year_bump = (month_bump-12, dt.year + 1)
    elif month_bump <= 0:
        month_bump, year_bump = (month_bump+12, dt.year - 1)
    else:
        month_bump, year_bump = (month_bump, dt.year)
    if keep_days:
        day = dt.day
    return datetime(year_bump, month_bump ,day)


def filter_outliers(df):
    from scipy import stats
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)
    df = df.copy().dropna()
    return df[(np.abs(stats.zscore(df)) < 3).all(axis=1)]


def fst(l):
    return [x[0] for x in l]


def snd(l):
    return [x[1] for x in l]


def thrd(l):
    return [x[2] for x in l]


def monthly_resample(_df, daily=False, from_back=False):
    df = _df.resample('1M').mean()
    if not from_back:
        df.index = df.index.map(bump_months)
    if daily:
        if from_back:
            return df.resample('1D').fillna(method='bfill')
        else:
            return df.resample('1D').fillna(method='ffill')
    else:
        return df


def weekly_resample(_df, daily=False):
    df = _df.resample('1W').sum().divide(7.)
    if daily:
        return df.resample('1D').fillna(method='bfill')
    else:
        return df


def to_utc(naive_dt):
    local = pytz.timezone("CET")
    local_dt = local.localize(naive_dt, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    return utc_dt


def to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=None)
    return local_dt


