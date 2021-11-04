# -*- coding: utf-8 -*-
from datetime import datetime, date, time, tzinfo, timezone, timedelta
from itertools import product

from idebug import *


__all__ = [
    'DatetimeParser',
    'datetime', 'date', 'time', 'tzinfo', 'timezone', 'timedelta'
]


def DatetimeFormatter():
    # 시간 포멧
    _times = [f"%H{s}%M{s}%S" for s in ('', ':')]
    _times += [f"%H{s}%M" for s in ('', ':')]
    time_fmt = [{'time':e} for e in _times]
    # 날짜 포멧
    _dates = [f"%Y{s}%m{s}%d" for s in ('', '.', '/', '-')]
    date_fmt = [{'date':e} for e in _dates]
    # 일시 포멧
    simbols = ('', ' ', 'T')
    _datetimes = [f"{t[0]}{t[1]}{t[2]}" for t in product(_dates, simbols, _times)]
    datetime_fmt = [{'datetime':e} for e in _datetimes]
    return time_fmt + date_fmt + datetime_fmt

Formatter = DatetimeFormatter()


def DatetimeParser(s):
    # 시간대역을 조정하는 역할을 한다
    # MongoDB에 저장되는 datetime은 UTC-timezone 기준이므로, 시간대를 변경해줘야 한다
    # 1970년 1월 1일 이전의 datetime은 astimezone() 함수를 사용할 수 없기 때문이다
    today = datetime.today().astimezone()

    if isinstance(s, str):
        s = s.strip()
        for d in Formatter:
            for type,fmt in d.items():
                try:
                    s = datetime.strptime(s, fmt)
                except Exception as e:
                    pass
                else:
                    # 포멧에는 밀리초를 취급하지 않는다
                    if type == 'time':
                        return today.replace(hour=s.hour, minute=s.minute, second=s.second, microsecond=0)
                    else:
                        return today.replace(year=s.year, month=s.month, day=s.day, hour=s.hour, minute=s.minute, second=s.second, microsecond=0)

        # 포멧팅에 실패할 경우
        if isinstance(s, str):
            if s in ['00000000','0']:
                # 예외처리할 케이스
                return None
            else:
                # 예외처리 이외의 경우, 그 값을 그대로 반환
                return s
    elif isinstance(s, datetime):
        return s.astimezone(tz=today.tzinfo)
    else:
        # logger.debug(f'입력값 타입오류: 반드시 스트링 또는 datetime 만 입력해야한다. s:{s}{type(s)}')
        return s
