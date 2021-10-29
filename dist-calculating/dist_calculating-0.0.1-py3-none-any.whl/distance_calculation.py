from math import cos, sin, radians, sqrt, asin, pi

"""
License: MIT License
Author: reisgoldmanX

"""

km_r = 6371  # Radius of earth in km
miles_r = 3956  # Radius of earth in miles


def fixing_angles(values: list, lat_or_lon=None) -> list:
    """
    There are 360 meridians- 180 to the east and 180 to the west of the Prime Meridian.
    The Earth is divided by the Equator into two equal halves known as the Northern Hemisphere (with 90 parallels) and
    the Southern Hemisphere (with 90 parallels).
    """
    lat = []
    lon = []

    if lat_or_lon is True:
        for latitude in values:
            if latitude > 90:
                latitude = 90
                lat.append(latitude)

            elif latitude < -90:
                latitude = -90
                lat.append(latitude)
            else:
                lat.append(latitude)
        return lat

    elif lat_or_lon is False:
        for longitude in values:
            if longitude > 180:
                longitude = 180
                lon.append(longitude)
            elif longitude < -180:
                longitude = -180
                lon.append(longitude)
            else:
                lon.append(longitude)
        return lon


def local_time_calculation(longitude1: int, longitude2: int) -> int:
    """Returns minutes in int

    1) The meridian difference between the two determined points is revealed.
      * If the meridians are located in the same hemisphere, they should be subtracted,
        if they are located in different hemispheres, they should be added.

    2) The resulting meridian difference is multiplied by 4 minutes.

    Additional information:
        - Because the Earth rotates from west to east, local time is always ahead in the east and behind in the west.
        - Local times of regions on the same meridian are always the same.
    """

    # Finding out which hemisphere the meridians are in:

    if longitude1 <= 0 and longitude2 <= 0:  # West hemisphere
        local_time_difference_minutes_west = abs((longitude1 - longitude2)) * 4
        return local_time_difference_minutes_west

    elif longitude1 >= 0 and longitude2 >= 0:  # East hemisphere
        local_time_difference_minutes_east = abs((longitude1 - longitude2)) * 4
        return local_time_difference_minutes_east

    elif longitude1 <= 0 or longitude2 <= 0:  # East & West hemisphere
        longitude1, longitude2 = abs(longitude1), abs(longitude2)
        local_time_difference_minutes_ew = (longitude1 + longitude2) * 4
        return local_time_difference_minutes_ew


def find_anti_meridian(longitude: int) -> int:
    """ Anti-meridian Calculation
    To find the anti-meridian of a meridian, it is necessary to subtract it from 180.
    """
    longitude = fixing_angles([longitude], lat_or_lon=False)[0]

    anti_meridian = 180 - longitude
    return anti_meridian


def distance_between_meridians(latitude: int) -> float:
    """ Calculating the distance between meridians
    To understand how many kilometers are between two meridians at our current point;
    First, we must calculate the length of the parallel at that point, using the angle of the parallel at that point.
    Then we have to divide by 360 since there are 360 meridians in the world.
    """
    latitude = fixing_angles([latitude], lat_or_lon=True)[0]
    distant = cos(latitude * (pi / 180))
    return distant * 111


def distance_calculation(latitude: float, longitude: float,
                         target_latitude: float, target_longitude: float, miles=False) -> float:
    """
    Calculate the distance between two points on Earth with Haversine formula.
    """
    latitude, target_latitude = fixing_angles([latitude, target_latitude], lat_or_lon=True)
    longitude, target_longitude = fixing_angles([longitude, target_longitude], lat_or_lon=False)

    latitude = radians(latitude)
    longitude = radians(longitude)
    target_latitude = radians(target_latitude)
    target_longitude = radians(target_longitude)

    lat = latitude - target_latitude
    lon = longitude - target_longitude

    haversine_1 = sin(lat / 2) ** 2 + cos(latitude) * cos(target_latitude) * sin(lon / 2) ** 2
    haversine_2 = 2 * asin(sqrt(haversine_1))
    if miles is False:
        return haversine_2 * km_r
    elif miles is True:
        return haversine_2 * miles_r
