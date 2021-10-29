import math


def epsg_900913_to_4326(x, y):
    lon = x * 180 / 20037508.34
    lat = (360 / math.pi) * math.atan(math.exp(y * math.pi / 20037508.34)) - 90
    return lon, lat
