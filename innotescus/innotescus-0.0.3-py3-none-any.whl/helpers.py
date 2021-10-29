from datetime import datetime
from functools import wraps
from logging import getLogger
from typing import Dict, Union, Callable
from json.decoder import JSONDecodeError

import requests
from .exceptions import YankedVersionError

log = getLogger('innotescus')


def ttl_cache_from_dict_result(f: Callable) -> Callable:
    """ Wrapper for caching the result of a function/method call.
    Cache value TTL expected from result value in key 'expires_at', which
    must be an unix timestamp.
    """
    expiry_time: Union[datetime, None] = None
    cached_response: Union[Dict, None] = None

    @wraps(f)
    def inner(*args, **kwargs):
        nonlocal expiry_time, cached_response

        if cached_response is not None:
            if expiry_time <= datetime.utcnow():  # assume expiry_time is in utc
                log.debug('TTL expired, evicting cached value')
                cached_response, expiry_time = None, None
            else:
                log.debug('Returning cached value')
                return cached_response

        rv = f(*args, **kwargs)

        if type(rv) is dict and 'expires_at' in rv:
            expiry_time = datetime.fromtimestamp(rv['expires_at'])  # DO NOT convert to UTC -- should already be UTC
            cached_response = rv
        else:
            log.debug('Failed to cache result.')

        return rv

    return inner


def check_for_yanked_release():
    """ Ensures the user's version of Innotescus hasn't been removed
    from the pypi repository.  If it has, raise an error.
    """
    from . import __version__  # local import to avoid circular ref
    try:
        release_info =  requests.get('https://pypi.org/pypi/innotescus/json').json()['info']['releases'][__version__]
        yanked = [row for row in release_info if row['yanked']]
        if yanked:
            raise YankedVersionError(yanked[0]['reason'])
    except KeyError:
        log.warning(f'Could not find "innotescus" version {__version__} on pypi')
    except JSONDecodeError:
        log.warning('Could not check for yanked version from pypi')


def check_for_updates():
    """ Checks PYPI for newer major/minor versions of innotescus and emits a warning if
    found.
    """
    from . import __version__  # local import to avoid circular ref
    try:
        latest_version = requests.get('https://pypi.org/pypi/innotescus/json').json()['info']['version']
        current = __version__.split('.')
        latest = latest_version.split('.')
        MAJOR, MINOR, PATCH = 0, 1, 2
        if int(latest[MAJOR]) > int(current[MAJOR]) or int(latest[MINOR]) > int(current[MINOR]):
            log.warning(f'There is a new version of innotescus ({latest_version}).  Please update immediately')
    except JSONDecodeError:
        log.warning('Could not check latest version from pypi')


def deprecated(message: str) -> Callable:
    """ Simple wrapper that outputs a warning message when the wrapped object is called.
    """
    def wrapper(f: Callable) -> Callable:
        @wraps(f)
        def inner(*args, **kwargs):
            log.warning('[DEPRECATED] %s', message)
            f(*args, **kwargs)
        return inner
    return wrapper
