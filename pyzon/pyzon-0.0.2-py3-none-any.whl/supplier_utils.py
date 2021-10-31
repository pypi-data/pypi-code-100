# -*- coding: utf-8 -*-
# @Time    : 2/4/21 3:32 PM
# @Author  : nzooherd
# @File    : supplier_utils.py
# @Software: PyCharm
from datetime import datetime


def lazy_supplier(func, timeout):
    value, update_time = None, None

    def lazy_func():
        nonlocal value, update_time
        now = datetime.now()
        if value and update_time and (update_time + timeout) > datetime.timestamp(now):
            return value
        else:
            value = func()
            update_time = datetime.timestamp(now)
        return value

    return lazy_func