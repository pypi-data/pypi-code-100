"""
Module to download, extract and parse data from openweathermap.org
"""
__all__ = ['get_daily_forecast', 'APIError']

import requests
import logging
import json

from typing import List

# NOTE: https currently fails SSL validation even though server is OK and request works in browser
URL_BASE = "http://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&cnt={num_days}&appid={api_key}"
logger = logging.getLogger('openweathermap')


class APIError(Exception):
    pass


def __get_api_key() -> str:
    import os
    res = os.environ.get('OPENWEATHERMAP_API_KEY')
    if not res:
        try:
            with open('.api.txt', 'r') as f:
                res = f.read()
        except IOError:
            pass
    if not res:
        raise APIError("No API key found in environment variable 'OPENWEATHERMAP_API_KEY' or '.api.txt'.")
    return res


def _get_weather(lat: float, lon: float, num_days: int = 7):
    api_key = __get_api_key()
    url = URL_BASE.format(**locals())
    logger.debug(f"{url=}")
    req = requests.get(url)

    if not 200 <= req.status_code < 300:
        raise APIError(f"Failed OpenWeatherMap API request. Status code: {req.status_code} ({req.text})")

    logger.debug(f"{json.dumps(req.json())=}")
    return req.json()


def _clean_weather(day: dict) -> dict:
    import datetime
    copy_fields = ['dt', 'sunrise', 'sunset', 'clouds', 'snow', 'rain', 'pop',
                   'wind_speed', 'wind_deg', 'wind_gust', 'humidity']
    deep_copy_fields = [
        ('temp_day', 'temp.day'),
        ('temp_morn', 'temp.morn'),
        ('temp_eve', 'temp.eve'),
    ]
    timestamp_fields = ['dt', 'sunrise', 'sunset']
    clean = {k: day.get(k, None) for k in copy_fields}
    for k, path in deep_copy_fields:
        a, b = path.split('.')
        clean[k] = day.get(a, {}).get(b, None)
    for k in timestamp_fields:
        clean[k] = datetime.datetime.fromtimestamp(clean[k]).isoformat()
    return clean


def get_daily_forecast(lat: float, lon: float) -> List[dict]:
    """ Return the daily forecasts for the given latitude and longitude.
    Unless the user has a paid account, this will provide data for the current day and 7 future days.
    The returned data is filtered to only include daily forecasts, and cleaned for easier use.

    Users should specify their openweathermap.org API key in the file '.api.txt' or in the environment variable
    openweathermap_api_key
    :param lat: Latitude of the desired forecast location. Float in the range [-90, 90]
    :param lon: Latitude of the desired forecast location. Float in the range (-180, 180]
    :return: List of dictionaries, one for each forecast day."""
    data = _get_weather(lat, lon).get('daily')
    return [_clean_weather(day) for day in data]
