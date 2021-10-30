#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   config.py    
@Contact :   wangcc@csc.com.cn
@License :   (C)Copyright 2017-2018, CSC

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/10/14 17:03   wangcc     1.0         None
'''

from datetime import datetime
from pathlib import Path
default_start_date = 20070101
default_end_date = int(datetime.now().strftime('%Y%m%d'))
cal_config = {
    "Tday": {
        "si": 20070104,
        "ei": 20210930,
        "col_name": "trade_dt"
             },
    "Aday": {
        "si": 20070101,
        "ei": 20210930,
        "col_name": "ann_date"
             },
    "report_period": {
        "si": 20001231,
        "ei": 20211232,
        "col_name": "report_period"
             }
}

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

data_path = r"T:\data\new_api_data"
(Path(data_path) / r"features").mkdir(exist_ok=True)
(Path(data_path) / r"datasets").mkdir(exist_ok=True)
(Path(data_path) / r"calendars").mkdir(exist_ok=True)
(Path(data_path) / r"instruments").mkdir(exist_ok=True)
