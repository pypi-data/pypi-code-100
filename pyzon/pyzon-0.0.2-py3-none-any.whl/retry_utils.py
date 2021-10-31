# -*- coding: utf-8 -*-
# @Time    : 2/4/21 3:32 PM
# @Author  : nzooherd
# @File    : retry_utils.py
# @Software: PyCharm
import functools
import time
from datetime import timedelta, datetime
from typing import Optional, Callable, Dict


def retry(func: Optional[Callable] = None, duration: timedelta = timedelta(seconds=2), limit: int = 10,
          exception2handler: Optional[Dict[type, callable]] = None) -> Callable:
    if not func:
        return functools.partial(retry, duration=duration, limit=limit)

    @functools.wraps(func)
    def _func(*args, **kwargs):
        duration_seconds = duration.total_seconds()
        count = 1
        while count <= limit:
            try:
                result = func(*args, **kwargs)
                return result
            except:
                count += 1
                time.sleep(duration_seconds)
                continue

    return _func


def frequency_limit(func: Optional[Callable] = None, duration: timedelta = None, limit: int = 0) -> Callable:
    if not func:
        return functools.partial(frequency_limit, duration=duration, limit=limit)

    if not duration:
        raise NotImplementedError

    period_first_call_time, count = None, 0

    @functools.wraps(func)
    def _func(*args, **kwargs):
        nonlocal period_first_call_time, count

        duration_seconds = duration.total_seconds()
        cur_time = int(datetime.timestamp(datetime.now()))

        if period_first_call_time is not None and cur_time < (period_first_call_time + duration_seconds) and count >= limit:
            time.sleep(duration_seconds + period_first_call_time - cur_time + 1)
            count = 0
            period_first_call_time = int(datetime.timestamp(datetime.now()))

        result = func(*args, **kwargs)
        count += 1
        return result

    return _func
