# -*- coding: utf-8 -*-
# @Time    : 2021/11/5 9:42
# @Author  : Blue52
# @FileName: cytimeutil
# @Software: PyCharm


import time
from datetime import timedelta
import datetime


# 时间字符串按照本身格式转为时间戳
def strToTimeStamp(timeStr, timeFmt):
    timeArray = time.strptime(timeStr, timeFmt)
    time_stamp = int(time.mktime(timeArray))
    return time_stamp


# 时间戳转为一定格式的时间字符串
def timeStampToStr(timeStamp, timeFmt):
    timeArray = time.localtime(timeStamp)
    timeStr = time.strftime(timeFmt, timeArray)
    return timeStr


# 计算两个时间字符串之间的差值，可以按照秒(s)、分(m)、小时(h)返回，默认返回秒
def timeMinusStr(start_time_str, end_time_str, time_fmt, timeType):
    start_time = strToTimeStamp(start_time_str, time_fmt)
    end_time = strToTimeStamp(end_time_str, time_fmt)
    return timeMinusStamp(start_time, end_time, timeType)


# 计算两个时间戳之间的差值，可以按照秒(s)、分(m)、小时(h)返回，默认返回秒
def timeMinusStamp(start_time, end_time, timeType):
    secondsDiff = end_time - start_time
    if timeType == 's':
        return secondsDiff
    elif timeType == 'm':
        return round((secondsDiff / 60), 2)
    elif timeType == 'h':
        return round((secondsDiff / 3600), 2)
    else:
        return secondsDiff


# 将时间戳转为世界时间字符串
def timeStrToUTCStr(time_str, timeFmt):
    timeStr = strTimeAddMinHourByFmt(time_str, 0, -8, timeFmt)
    return timeStr


# 时间字符串添加分钟和小时后返回时间字符串
def strTimeAddMinHour(str_p, mins, hours):
    date_p = datetime.datetime.strptime(str_p, '%Y-%m-%d %H:%M:%S')
    date_p = date_p + datetime.timedelta(minutes=mins)
    date_p = date_p + datetime.timedelta(hours=hours)
    date_str = date_p.strftime("%Y-%m-%d %H:%M:%S")
    return date_str


# 时间字符串添加分钟和小时后返回时间字符串
def strTimeAddMinHourByFmt(str_p, mins, hours, fmt):
    date_p = datetime.datetime.strptime(str_p, fmt)
    date_p = date_p + datetime.timedelta(minutes=mins)
    date_p = date_p + datetime.timedelta(hours=hours)
    date_str = date_p.strftime(fmt)
    return date_str


def getDatesByTimes(sDateStr, eDateStr):
    """
    获取两个时间字符串之间，所有的日期
    :param sDateStr:
    :param eDateStr:
    :return:
    """
    list = []
    datestart = datetime.datetime.strptime(sDateStr, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(eDateStr, '%Y-%m-%d')
    list.append(datestart.strftime('%Y%m%d'))
    while datestart < dateend:
        datestart += datetime.timedelta(days=1)
        list.append(datestart.strftime('%Y%m%d'))
    return list


# if __name__ == '__main__':
#     # 计算两个时间字符串，差了多少分钟
#     start_time_str = '2020-07-09 10:30:03'
#     end_time_str = '2020-07-09 11:45:20'
#     time_fmt = "%Y-%m-%d %H:%M:%S"
#     minuteDiff = timeMinusStr(start_time_str, end_time_str, time_fmt, 'm')
#     print(minuteDiff)
