

import re
import pandas as pd
from pandas.io.json import json_normalize


def set_difference(li1, li2):
    """차집합 리스트. li1 - li2"""
    return [e for e in li1 if e not in li2]

def list_cols_normalize(df, litype_cols):
    """두개 이상의 컬럼이 리스트형 값을 가진 경우 이를 전부 풀어서 다시 프레임으로 반환
    """
    cols = list(df.columns)
    for col in litype_cols:
        cols.remove(col)
    df1 = df.loc[:, cols]

    for col in litype_cols:
        df2 = df.loc[:,[col,'_id']]
        df2 = json_normalize( df2.dropna().to_dict('records'), col, ['_id'] ).rename(columns={0:col})
        df1 = df1.join(df2.set_index('_id'), on='_id')

    return df1

def reg_matched(li, pat):
    """http://www.cademuir.eu/blog/2011/10/20/python-searching-for-a-string-within-a-list-list-comprehension/
    """
    r = re.compile(".*("+pat+").*")
    return [m.group(0) for e in li for m in [r.search(e)] if m]
