#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   tools.py    
@Contact :   wangcc@csc.com.cn
@License :   (C)Copyright 2017-2018, CSC

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/10/14 16:55   wangcc     1.0         None
'''
import pandas as pd


def bisect_right(a, x, lo=0, hi=None):
    """ Return the index where to insert item x in list a, assuming a is sorted. """

    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if x < a[mid]:
            hi = mid
        else:
            lo = mid + 1
    return lo


def bisect_left(a, x, lo=0, hi=None):
    """ Return the index where to insert item x in list a, assuming a is sorted. """

    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo


def to_intdate(dt: (str, pd.Timestamp)):
    if isinstance(dt, str):
        return int(dt.replace('-', ''))
    if isinstance(dt, pd.Timestamp):
        return int(dt.strftime("%Y%m%d"))
    else:
        return dt
