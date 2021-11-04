# -*- ecoding: utf-8 -*-
# @ModuleName: phi_tool.py
# @Function: 一些工具方法
# @Author: ctx_phi
# @Craete Time: 2021/11/4 10:37

import pandas as pd
from datetime import datetime


def datelist(self, beginDate, endDate):
    '''
    根据st和et生成日期列表
    '''
    # beginDate, endDate是形如‘20160601’的字符串或datetime格式
    date_l=[datetime.strftime(x,'%Y-%m-%d %H:%M:%S') for x in list(pd.date_range(start=beginDate, end=endDate))]
    return date_l


if __name__ =='__main__':
    None