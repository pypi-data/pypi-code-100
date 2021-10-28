"""
Module for manipulating dates
"""

import datetime
from calendar import monthrange
from datetime import date, datetime, timedelta
from typing import Union

def round_time(dt:datetime = None, roundTo:timedelta = timedelta(minutes=1), roundType:str = 'nearest') -> datetime:
    """Round a time to a nearest common format

    Parameters
    ----------
    dt : datetime.datetime object
        Datetime one wish to round
    roundTo : datetime.timedelta object (optional)
        What to round to. Defaults to datetime.timedelta(minutes=1).
    roundType : str
        How to round. 'nearest', 'roundup', 'rounddown'

    Returns
    -------
    dt_rounded : datetime.datetime object
        Rounded datetime
    """
    roundTo = roundTo.total_seconds()
    if dt == None : dt = datetime.datetime.now()
    seconds = (dt - dt.min).seconds
    if roundType=='nearest':
        rounding = (seconds+roundTo/2) // roundTo * roundTo
    elif roundType=='roundup':
        rounding = (seconds+roundTo) // roundTo * roundTo
    elif roundType=='rounddown':
        rounding = seconds // roundTo * roundTo

    return dt + timedelta(0, rounding - seconds, -dt.microsecond)


def per_delta(start:datetime, end:datetime, delta:timedelta):
    """Generate a list of datetimes within an interval

    Parameters
    ----------
    start : datetime.datetime object
        Starting date
    end : datetime.datetime object
        End date
    delta : datetime.timedelta object
        Increment in time, e.g. 1 hour would be datetime.timedelta(hours=1)
    """
    curr = start
    while curr < end:
        yield curr
        curr += delta


# def current_run_datetime(frequency:int=3, delay:int=2) -> datetime:
#     """Get the time of the current valid analysis

#     Parameters
#     ----------
#     frequency : integer (optional)
#         Frequency of analysis in hours. Defaults to 3 hours.
#     delay : integer (optional)
#         Delay in hours between now and when analysis becomes available. Defaults to 2 hours.

#     Returns
#     -------
#     nowrounded : datetime.datetime object
#         Time for the latest current valid analysis
#     """
#     now = datetime.utcnow()
#     nowrounded = now.replace(hour=((now.hour - delay) - (now.hour - delay) % frequency) % 24)
#     if (now - timedelta(hours=frequency)).strftime('%d') != nowrounded.strftime('%d'):
#         nowrounded = nowrounded - timedelta(hours=24)
#     return nowrounded

def current_run_datetime(frequency:int=180, delay:int=120, roundto:str='hour', now:Union[datetime, None]=None) -> datetime:
    """Get the time of the current valid analysis

    Parameters
    ----------
    frequency : integer (optional)
        Frequency of analysis in minutes. Defaults to 180 minutes (3 hours).
    delay : integer (optional)
        Delay in minutes between now and when analysis becomes available. Defaults to 120 minutes (2 hours)
    roundto : string (optional)
        What to round to: Available is "hour", "minute". Defaults to "hour"
    now : datetime object (optional)
        Current time to get run for. Defaults to now.

    Returns
    -------
    nowrounded : datetime.datetime object
        Time for the latest current valid analysis
    """

    if now is None: now=datetime.utcnow()

    if roundto=='hour':
        delay = delay//60
        frequency = frequency//60

        delayed_now_hour = now.hour - delay

        if delayed_now_hour<0: now += timedelta(days=delayed_now_hour//24)
        nowrounded = now.replace(hour=((delayed_now_hour) - (delayed_now_hour) % frequency) % 24)

    elif roundto=='minute' or roundto=='10minute':
        if int(now.minute) < delay:
            delay+=60 
        nowrounded = now.replace(minute=((now.minute - delay) - (now.minute - delay) % frequency) % 60)
        nowrounded = nowrounded.replace(hour=(nowrounded.hour - (nowrounded.minute)//50) % 24)

    if (now - timedelta(minutes=frequency)).hour != nowrounded.hour:
        nowrounded-=timedelta(hours=1)

    if (now - timedelta(minutes=frequency)).strftime('%d') != nowrounded.strftime('%d'):
        nowrounded-=timedelta(hours=24)



    if roundto=='hour':
        nowrounded = round_time(nowrounded, roundTo=timedelta(hours=1), roundType='rounddown')
    elif roundto=='minute':
        nowrounded = round_time(nowrounded, roundTo=timedelta(minutes=1), roundType='rounddown')
    elif roundto=='10minute':
        nowrounded = round_time(nowrounded, roundTo=timedelta(minutes=10), roundType='rounddown')

    return nowrounded


def month_delta(d1:datetime, d2:datetime) -> int:
    """Find the difference between dates in months

    Parameters
    ----------
    d1 : datetime.datetime object
        Date 1
    d2 : datetime.datime object
        Date 2

    Returns
    -------
    delta : integer
        Difference between dates in months
    """
    delta = 0
    while True:
        mdays = monthrange(d1.year, d1.month)[1]
        d1 += timedelta(days=mdays)
        if d1 <= d2:
            delta += 1
        else:
            break
    return delta


def add_month(date=None):
    """Add one month to date

    Parameters
    ----------
    date : datetime.datetime object
        Date to add one month to.

    Returns
    -------
    candidate: datetime.datetime object
        Candidate date with one month added
    """
    # number of days this month
    month_days = monthrange(date.year, date.month)[1]
    candidate = date + timedelta(days=month_days)
    # but maybe we are a month too far
    if candidate.day != date.day:
        # go to last day of next month,
        # by getting one day before begin of candidate month
        return candidate.replace(day=1) - timedelta(days=1)
    else:
        return candidate


def subtract_one_month(date=None):
    """Subtract one month from date

    Parameters
    ----------
    date : datetime.datetime object
        Date to subtract one month from.

    Returns
    -------
    dt3: datetime.datetime object
        Date after subtracting one month
    """
    dt1 = date.replace(day=1)
    dt2 = dt1 - timedelta(days=1)
    dt3 = dt2.replace(day=1)
    return dt3


def count_days(date1=None, date2=None, includeEnd=False):
    """Count the days between two dates

    Parameters
    ----------
    date1 : datetime.datetime object
        Date 1
    date2 : datetime.datetime object
        Date 2
    includeEnd : boolean
        Whether to include the last day itself. Defaults to False.

    Returns
    -------
    days : integer
        Days between two dates.
    """
    if includeEnd:
        return int((date2-date1).total_seconds()/(60*60*24) + 1)
    else:
        return int((date2-date1).total_seconds()/(60*60*24))
