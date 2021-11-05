from enum import Enum
try:
    from shapely.geometry import shape
except ModuleNotFoundError:
    raise ModuleNotFoundError('Expect package named shapely, try to install shapely')
from pyproj import CRS, Proj


class AreaUnit(Enum):
    """
    面积单位
    """
    KILOMETERS2 = 'km2'
    METERS2 = 'm2'


# 面积换算因数
_CONVERSIONS_FROM_M2 = {
    AreaUnit.KILOMETERS2: 1e+6,
    AreaUnit.METERS2: 1.0
}


def area(*points, unit: AreaUnit = AreaUnit.METERS2, crs: CRS = CRS.from_epsg(3857)) -> float:
    """
    计算地球上多边形的面积
    :param points: 多个点集合，形式为 (latitude, longitude)
    :param unit: 面积单位，默认为平方米
    :param crs: CRS 实例，默认为墨卡托投影
    :return: 面积
    """
    p = Proj(crs.to_proj4())

    return shape({
        'type': 'Polygon',
        'coordinates': [list(map(lambda x: p(*x[:: -1]), points))]
    }).area * _CONVERSIONS_FROM_M2[unit]
