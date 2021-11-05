from enum import Enum
from numpy import arcsin, cos, radians, sin, sqrt


class DistanceUnit(Enum):
    """
    距离单位
    """
    KILOMETERS = 'km'
    METERS = 'm'
    MILES = 'mi'


# 平均地球半径 - https://en.wikipedia.org/wiki/Earth_radius#Mean_radius
AVG_EARTH_RADIUS_M = 6371008


# 距离换算因数
_CONVERSIONS_FROM_M = {
    DistanceUnit.KILOMETERS: 1000.0,
    DistanceUnit.METERS: 1.0,
    DistanceUnit.MILES: 0.000621371192
}


def distance(point1, point2, *, unit: DistanceUnit = DistanceUnit.KILOMETERS) -> float:
    """
    计算大圆距离
    :param point1: 经纬度坐标点，形式为 (latitude, longitude)
    :param point2: 经纬度坐标点，形式为 (latitude, longitude)
    :param unit: 距离单位，默认为米
    :return: 大圆距离
    """
    # 解算经纬度
    lat1, lng1 = point1
    lat2, lng2 = point2

    # 转为弧度制
    lat1 = radians(lat1)
    lng1 = radians(lng1)
    lat2 = radians(lat2)
    lng2 = radians(lng2)

    # 计算
    lat = lat2 - lat1
    lng = lng2 - lng1
    d = sin(lat * 0.5) ** 2 + cos(lat1) * cos(lat2) * sin(lng * 0.5) ** 2

    return 2 * (AVG_EARTH_RADIUS_M * _CONVERSIONS_FROM_M[DistanceUnit(unit)]) * arcsin(sqrt(d))
