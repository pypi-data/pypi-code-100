# coding=utf-8
from datetime import datetime
from enum import Enum

def get_datetime_from_rfc3339(datetime_str: str):
    d = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    return d

class StringEnum(Enum):
    @classmethod
    def get_values(cls):
        return list(map(lambda e: e[1].value, cls.__members__.items()))

    @classmethod
    def contains_value(cls, value: str):
        return value in cls.get_values()


class RegionalSettingsType(StringEnum):
    ES = 'es'
    ES_VE = 'es-ve'
    EN = 'en'
    EN_US = 'en-us'


class YesNoType(StringEnum):
    Yes = 'Yes'
    No = 'No'

class DaysType(StringEnum):
    Mo = 'Mo'
    Tu = 'Tu'
    We = 'We'
    Th = 'Th'
    Fr = 'Fr'
    Sa = 'Sa'
    Su = 'Su'

DAYS_FOR_SP = {
    DaysType.Mo.value: 'Lunes',
    DaysType.Tu.value: 'Martes',
    DaysType.We.value: 'Miercoles',
    DaysType.Th.value: 'Jueves',
    DaysType.Fr.value: 'Viernes',
    DaysType.Sa.value: 'Sabado',
    DaysType.Su.value: 'Domingo'
}

DAYS_FOR_EN = {
    DaysType.Mo.value: 'Monday',
    DaysType.Tu.value: 'Tuesday',
    DaysType.We.value: 'Wednesday',
    DaysType.Th.value: 'Thursday',
    DaysType.Fr.value: 'Friday',
    DaysType.Sa.value: 'Saturday',
    DaysType.Su.value: 'Sunday'
}

DAYS_PER_LANGUAGE = {
    RegionalSettingsType.ES.value: DAYS_FOR_SP,
    RegionalSettingsType.ES_VE.value: DAYS_FOR_SP,
    RegionalSettingsType.EN.value: DAYS_FOR_EN,
    RegionalSettingsType.EN_US.value: DAYS_FOR_EN,
}

LIST_TRUNCATED_LAST_ITEM_PER_LANGUAGE = {
    RegionalSettingsType.ES.value: 'mas',
    RegionalSettingsType.ES_VE.value: 'mas',
    RegionalSettingsType.EN.value: 'more',
    RegionalSettingsType.EN_US.value: 'more',
}

LIST_LAST_ITEM_SEPARATOR_PER_LANGUAGE = {
    RegionalSettingsType.ES.value: 'y',
    RegionalSettingsType.ES_VE.value: 'y',
    RegionalSettingsType.EN.value: 'and',
    RegionalSettingsType.EN_US.value: 'and',
}
