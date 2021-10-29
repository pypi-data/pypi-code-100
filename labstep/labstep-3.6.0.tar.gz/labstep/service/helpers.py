#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Barney Walker <barney@labstep.com>

from datetime import datetime
from time import gmtime, strftime
from labstep.constants.version import VERSION


def url_join(*args):
    """
    Join a set of args with a slash (/) between them. Instead of
    checking for the presence of a slash, the slashes from both sides
    of each arg will be .strip() and then args .join() together.

    Returns
    -------
        returns "/".join(arg.strip("/") for arg in args)

    """
    return "/".join(arg.strip("/") for arg in args)


def handleError(response, *args, **kwargs):
    """
    Returns
    -------
        The error code and error message if the
        status code of the request is not 200.
    """
    if response.status_code != 200:
        print(
            """Get the latest version of the SDK by running:
        pip install labstep --upgrade"""
        )
        raise Exception(
            "Request Error {code}:{message}".format(
                code=response.status_code, message=response.content
            )
        )
    return


def getTime():
    """
    Returns
    -------
    timestamp
        The datetime at .now() in json serializable format.
    """
    timezone = strftime("%z", gmtime())
    tz_hour = timezone[:3]
    tz_minute = timezone[3:]
    timestamp = datetime.now().strftime(
        "%Y-%m-%d" + "T" + "%H:%M:%S" + "{}:{}".format(tz_hour, tz_minute)
    )
    return timestamp


def handleDate(date):
    """
    Returns
    -------
        The datetime for in json serializable format.
    """
    if date is None:
        return None

    for fmt in ('%Y-%m-%d', '%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S'):
        try:
            return datetime.strptime(date, fmt).strftime('%Y-%m-%dT%H:%M:%S+00:00')
        except ValueError:
            pass
    raise ValueError(
        'Please Specify date in format: YY-MM-DD or YY-MM-DD HH:MM:SS')



def handleString(string):
    """
    Casts to string or returns None
    """
    return str(string) if string else None


def handleKeyword(string):
    """
    Returns
    -------
    string
        The string in lowercase, and any whitespace replaced with '_'.
    """
    if string is None:
        return None
    else:
        return string.lower().replace(" ", "_")


def update(entity, newData):
    """
    Returns
    -------
    the updated entity
    """
    entity.__data__ = newData
    for key in newData:
        setattr(entity, key, newData[key])
    return entity


def getHeaders(user=None):
    if user is None:
        return {
            "User-Agent": f"Python SDK {VERSION}"
        }
    else:
        return {
            "apikey": user.api_key,
            "User-Agent": f"Python SDK {VERSION}"
        }
