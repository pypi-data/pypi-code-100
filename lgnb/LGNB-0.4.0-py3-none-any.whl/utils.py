#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   utils.py    
@Contact :   wangcc@csc.com.cn
@License :   (C)Copyright 2017-2018, CSC

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/10/14 18:50   wangcc     1.0         None
'''


import numpy as np
import numba as nb
import pandas as pd
from tqdm import tqdm
from .reader_utils import Cal
from .config import default_start_date, default_end_date

calendar = Cal._get_calendar("Tday")
susday_config = {
    444001000: True,  # 上午停牌
    444002000: True,  # 下午停牌
    444003000: False,  # 今起停牌
    444004000: True,  # 盘中停牌
    444005000: True,  # 停牌半天
    444007000: True,  # 停牌1小时
    444008000: False,  # 暂停交易
    444016000: True,  # 停牌一天
}

suspension_config = {
    444001000: True,  # 上午停牌
    444002000: True,  # 下午停牌
    444003000: True,  # 今起停牌
    444004000: True,  # 盘中停牌
    444005000: True,  # 停牌半天
    444007000: True,  # 停牌1小时
    444008000: True,  # 暂停交易
    444016000: True,  # 停牌一天
}


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


def dict_configure(df):
    groups = df.groupby(df.index)
    config = {}
    for code, df in tqdm(groups):
        config[code] = stinfo_by_code(df, code)
    return config


def stinfo_by_code(df, code):
    df = df.sort_values(df.columns[0])
    array = df.loc[code].values.flatten()
    if np.isnan(array[-1]):
        array[-1] = default_end_date
    array = np.minimum(array, default_end_date)  # ipo 可能有未来的某一天上市信息
    mask = np.isnan(array)
    array = array[(~mask) & (~np.roll(mask, 1))]
    return array


@nb.jit(nopython=True, cache=True)
def match_amt(value, idx, ref_stt_idx, ref_end_idx):
    value = np.append([np.nan], value)
    fidx = np.append([ref_stt_idx], idx)
    bidx = np.roll(fidx, -1)
    bidx[-1] = ref_end_idx + 1
    amt = bidx - fidx
    return value, amt


def create_ndns_table(index, cols, fill_value=False):
    table = pd.DataFrame(fill_value, index=index, columns=cols)
    return table


def to_ndns_reports(df, value_label, start_date, end_date, key1='report_period', key2='ann_date'):
    df['si'] = df[key2].apply(lambda x: bisect_left(calendar, x))
    dfs = {}
    ref_stt_idx = bisect_left(calendar, int(start_date))
    ref_end_idx = bisect_right(calendar, int(end_date)) - 1
    index = Cal.calendar(start_date, end_date)
    for inst, df_i in tqdm(df.groupby(df['code'])):
        df_i = df_i.sort_values([key2, key1]).drop_duplicates(key2, keep='last')
        value, amt = match_amt(df_i[value_label].values, df_i.si.values, ref_stt_idx, ref_end_idx)
        dfs[inst] = np.repeat(value, amt)
    return pd.DataFrame(dfs, index=index)


def to_ndns_io_date(df, time_keys, timeindex, stcoklist):
    """ st:"entry_date","remove_date"
        ipo:"listdate","delistdate"
        suspend"""
    tdict = dict_configure(df[time_keys])
    table_dict = {}
    for inst in tqdm(tdict.keys()):
        tlist = tdict.get(inst)
        if tlist is not None:
            sei = tlist.reshape((-1, 2))
            index = np.concatenate([Cal.calendar(si, ei) for si, ei in sei])
            table_dict[inst] = pd.Series(1, index=np.unique(index))
    return pd.concat(table_dict, axis=1).reindex(index=timeindex, columns=stcoklist)


def to_ndns_indu(indu, time_keys, timeindex, stcoklist, level):
    "entry_date	remove_date"
    indu = indu.reset_index().set_index('stockcode')[time_keys + [level]]
    ori_table = create_ndns_table(timeindex, stcoklist, np.nan)
    indu['remove_date'].fillna(int(default_end_date), inplace=True)
    transform_dict = dict(zip(indu.L1.unique(), range(indu.L1.unique().shape[0])))
    indu.L1 = indu.L1.map(transform_dict)
    for inst, si, ei, value in tqdm(indu.to_records()):
        ori_table.loc[si:ei, (inst,)] = value
        # print(inst)
    return ori_table.reindex(columns=stcoklist)


def process_sus(sus):
    sus['is_sus'] = sus.suspend_type.map(suspension_config)
    sus = sus.loc[sus.is_sus]
    sus['replace'] = sus.suspend_type.map(susday_config) & np.isnan(sus.resump_date)
    sus.loc[sus['replace'], 'resump_date'] = sus.loc[sus['replace'], 'suspend_date']
    return sus


def nanargsort(mat):
    new_mat = np.full_like(mat, np.nan)
    for i in np.arange(new_mat.shape[0]):
        arr_i = mat[i, :]
        mask = np.isnan(arr_i)
        new_mat[i, ~mask] = np.argsort(np.argsort(-arr_i[~mask])) < 2500  # 求最大
    return new_mat


