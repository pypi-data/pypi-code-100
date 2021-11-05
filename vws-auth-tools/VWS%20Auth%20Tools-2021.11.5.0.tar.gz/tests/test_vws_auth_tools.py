"""
Tests for authorization tools.
"""

import datetime
from zoneinfo import ZoneInfo

from freezegun import freeze_time

import vws_auth_tools


def test_rfc_1123_date() -> None:
    """
    The date is returned in the format described at
    https://library.vuforia.com/articles/Training/Using-the-VWS-API:

    ```
    Date: This is the current date per RFC 2616, section 3.3.1, rfc1123-date
    format, for example, Sun, 22 Apr 2012 08:49:37 GMT,

    NOTE: The date and time always refer to GMT.
    ```
    """
    not_gmt_timezone = ZoneInfo('America/New_York')
    frozen_time = datetime.datetime(
        year=2015,
        month=2,
        day=5,
        hour=9,
        minute=55,
        second=12,
        microsecond=11,
        tzinfo=not_gmt_timezone,
    )
    with freeze_time(frozen_time):
        result = vws_auth_tools.rfc_1123_date()

    assert result == 'Thu, 05 Feb 2015 14:55:12 GMT'


def test_authorization_header() -> None:
    """
    The authorization header is constructed as described in the Vuforia
    documentation. This example has been run on known-working code and so any
    refactor should continue to pass this test.
    """
    access_key = 'my_access_key'
    secret_key = 'my_secret_key'
    method = 'HTTPMETHOD'
    content = b'some_bytes'
    content_type = 'some/content/type'
    date = 'some_date_string'
    request_path = '/foo'

    result = vws_auth_tools.authorization_header(
        access_key=access_key,
        secret_key=secret_key,
        method=method,
        content=content,
        content_type=content_type,
        date=date,
        request_path=request_path,
    )

    assert result == 'VWS my_access_key:8Uy6SKuO5sSBY2X8/znlPFmDF/k='
