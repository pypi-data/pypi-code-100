import datetime
from python_helper.api.src.domain import Constant as c
from python_helper.api.src.service import ObjectHelper, StringHelper, RandomHelper

DEFAULT_DATETIME_PATTERN = '%Y-%m-%d %H:%M:%S'
DEFAULT_DATE_PATTERN = '%Y-%m-%d'
DEFAULT_TIME_PATTERN = '%H:%M:%S'

DATETIME_FULL_PATTERN = '%Y-%m-%d %H:%M:%S.%f'
TIME_FULL_PATTERN = '%H:%M:%S.%f'

PATTERN_LIST = [
    DEFAULT_DATETIME_PATTERN,
    DEFAULT_DATE_PATTERN,
    DEFAULT_TIME_PATTERN,
    DATETIME_FULL_PATTERN,
    TIME_FULL_PATTERN
]

DATETIME_PATTERN_LIST = [
    DEFAULT_DATETIME_PATTERN,
    DATETIME_FULL_PATTERN
]

DATE_PATTERN_LIST = [
    DEFAULT_DATE_PATTERN
]

TIME_PATTERN_LIST = [
    DEFAULT_TIME_PATTERN,
    TIME_FULL_PATTERN
]

DEFAULT_TIME_BEGIN = '00:00:00'
DEFAULT_TIME_END = '23:59:59'

def toString(givenDatetime, pattern=DEFAULT_DATETIME_PATTERN) :
    return givenDatetime if ObjectHelper.isNone(givenDatetime) or isinstance(givenDatetime, str) else parseToString(givenDatetime, pattern=pattern)

def parseToString(given, pattern=DEFAULT_DATETIME_PATTERN) :
    return str(given)

def parseToPattern(given, pattern=DEFAULT_DATETIME_PATTERN, timedelta=False) :
    given = given.strip()
    if StringHelper.isNotBlank(given) :
        parsed = datetime.datetime.strptime(given, pattern)
        if timedelta and pattern in TIME_PATTERN_LIST :
            return datetime.timedelta(hours=parsed.hour, minutes=parsed.minute, seconds=parsed.second, milliseconds=0, microseconds=0)
        if pattern in DATETIME_PATTERN_LIST :
            return parsed
        elif pattern in DATE_PATTERN_LIST :
            return parsed.date()
        elif pattern in TIME_PATTERN_LIST :
            return parsed.time()

def forcedlyParse(given, pattern=DEFAULT_DATETIME_PATTERN, timedelta=False) :
    parsed = None
    for pattern in [pattern] + PATTERN_LIST :
        try :
            parsed = parseToPattern(given, pattern=pattern, timedelta=timedelta)
        except Exception as exception :
            pass
    return parsed

def parseToDateTime(givenDatetime, pattern=DEFAULT_DATETIME_PATTERN) :
    return givenDatetime if ObjectHelper.isNone(givenDatetime) or not isinstance(givenDatetime, str) else parseToPattern(givenDatetime, pattern=pattern)

def forcedlyGetDateTime(givenDatetime, pattern=DEFAULT_DATETIME_PATTERN) :
    return givenDatetime if ObjectHelper.isNone(givenDatetime) or not isinstance(givenDatetime, str) else forcedlyParse(givenDatetime, pattern=pattern)

def forcedlyGetDate(givenDate, pattern=DEFAULT_DATE_PATTERN) :
    return givenDate if ObjectHelper.isNone(givenDate) or not isinstance(givenDate, str) else forcedlyParse(givenDate, pattern=pattern)

def forcedlyGetTime(givenTime, pattern=DEFAULT_TIME_PATTERN) :
    return givenTime if ObjectHelper.isNone(givenTime) or not isinstance(givenTime, str) else forcedlyParse(givenTime, pattern=pattern)

def forcedlyGetInterval(givenTime, pattern=DEFAULT_DATETIME_PATTERN) :
    return givenTime if ObjectHelper.isNone(givenTime) or not isinstance(givenTime, str) else forcedlyParse(givenTime, pattern=pattern, timedelta=True)

def plusSeconds(givenDateTimeOrTime, seconds=None, deltaInSeconds=None) :
    if ObjectHelper.isNotNone(seconds) :
        deltaInMinutes = datetime.timedelta(seconds=seconds)
    if isinstance(givenDateTimeOrTime, datetime.time) :
        givenDateTimeOrTime = forcedlyParse(f'{str(dateNow())} {givenDateTimeOrTime}')
    return forcedlyGetDateTime(str(givenDateTimeOrTime)) + deltaInMinutes

def minusSeconds(givenDateTimeOrTime, seconds=None, deltaInSeconds=None) :
    if ObjectHelper.isNotNone(seconds) :
        deltaInMinutes = datetime.timedelta(seconds=seconds)
    if isinstance(givenDateTimeOrTime, datetime.time) :
        givenDateTimeOrTime = forcedlyParse(f'{str(dateNow())} {givenDateTimeOrTime}')
    return forcedlyGetDateTime(str(givenDateTimeOrTime)) - deltaInMinutes

def plusMinutes(givenDateTimeOrTime, minutes=None, deltaInMinutes=None) :
    if ObjectHelper.isNotNone(minutes) :
        deltaInMinutes = datetime.timedelta(seconds=minutes*60)
    if isinstance(givenDateTimeOrTime, datetime.time) :
        givenDateTimeOrTime = forcedlyParse(f'{str(dateNow())} {givenDateTimeOrTime}')
    return forcedlyGetDateTime(str(givenDateTimeOrTime)) + deltaInMinutes

def minusMinutes(givenDateTimeOrTime, minutes=None, deltaInMinutes=None) :
    if ObjectHelper.isNotNone(minutes) :
        deltaInMinutes = datetime.timedelta(minutes=minutes)
    if isinstance(givenDateTimeOrTime, datetime.time) :
        givenDateTimeOrTime = forcedlyParse(f'{str(dateNow())} {givenDateTimeOrTime}')
    return forcedlyGetDateTime(str(givenDateTimeOrTime)) - deltaInMinutes

def plusDays(givenDay, days=None, deltaInDays=None) :
    if ObjectHelper.isNotNone(days) :
        deltaInDays = datetime.timedelta(days=days)
    return forcedlyGetDateTime(str(givenDay)) + deltaInDays

def minusDays(givenDay, days=None, deltaInDays=None) :
    if ObjectHelper.isNotNone(minutes) :
        deltaInDays = datetime.timedelta(days=days)
    return forcedlyGetDateTime(str(givenDay)) - deltaInDays

def getDefaultTimeBegin() :
    return forcedlyGetTime(DEFAULT_TIME_BEGIN)

def getDatetimeMonthBegin() :
    return parseToPattern(c.SPACE.join([c.DASH.join(str(dateTimeNow()).split()[0].split(c.DASH)[:-1] + ['01']), DEFAULT_TIME_BEGIN]))

def dateTimeNow() :
    # return datetime.datetime.now()
    return datetime.datetime.utcnow()

def of(date=None, time=None, dateTime=None):
    if ObjectHelper.isNotNone(dateTime):
        if isinstance(dateTime, str):
            date = dateOf(parsedDateTime).split()[0]
            time = timeOf(parsedDateTime).split()[1]
        if isinstance(dateTime, datetime.datetime):
            return dateTime
        else:
            date = dateOf(parsedDateTime)
            time = timeOf(parsedDateTime)
    return datetime.datetime.combine(forcedlyGetDate(date), forcedlyGetTime(time))

def dateOf(dateTime=None) :
    return dateTime.date()

def timeOf(dateTime=None) :
    return dateTime.time()

def dateNow() :
    # datetime.date.today()
    return dateOf(dateTime=dateTimeNow())

def timeNow() :
    return dateTimeNow().time()

def timestampNow():
    return datetime.timestamp(dateTimeNow())

def ofTimestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)

def toTimestamp(date=None, time=None, dateTime=None):
    return datetime.datetime.timestamp(of(date=date, time=time, dateTime=dateTime))

def getTodayDateAndTodayTime() :
    dateTime = dateTimeNow()
    return dateOf(dateTime=dateTime), timeOf(dateTime=dateTime)

def getTodayDateTimeBegin() :
    return parseToDateTime(f'{dateNow()} {DEFAULT_TIME_BEGIN}')

def getTodayDateTimeEnd() :
    return parseToDateTime(f'{dateNow()} {DEFAULT_TIME_END}')

###- deprecated
def getWeekDay(ofDatetime=None, ofDate=None, ofTime=None) :
    if ObjectHelper.isNotNone(ofDatetime) :
        return forcedlyGetDateTime(ofDatetime).weekday()
    elif ObjectHelper.isNotNone(ofDate) and ObjectHelper.isNotNone(ofTime) :
        return of(forcedlyGetDate(ofDate), forcedlyGetTime(ofTime)).weekday()
    elif ObjectHelper.isNotNone(ofDate) :
        return of(forcedlyGetDate(ofDate), forcedlyGetTime(DEFAULT_TIME_END)).weekday()
    return dateTimeNow().weekday()

def getWeekDayOf(dateTime=None, date=None, time=None) :
    if ObjectHelper.isNotNone(dateTime) :
        return forcedlyGetDateTime(dateTime).weekday()
    elif ObjectHelper.isNotNone(date) and ObjectHelper.isNotNone(time) :
        return of(forcedlyGetDate(date), forcedlyGetTime(time)).weekday()
    elif ObjectHelper.isNotNone(date) :
        return of(forcedlyGetDate(date), forcedlyGetTime(DEFAULT_TIME_END)).weekday()
    return dateTimeNow().weekday()

def addNoise(givenDatetime) :
    return givenDatetime + datetime.timedelta(milliseconds=RandomHelper.integer(0,999))
