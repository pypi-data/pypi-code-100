"""This module contains tests for module cacher.py."""

import os
import sys

import pytest

sys.path.append(os.path.dirname(os.getcwd()))
sys.path.append(os.getcwd())

from grebarss_reader.cacher import Cacher


@pytest.fixture
def cacher_instance():
    """
    Initialization object class Cacher
    :return: object class Cacher
    """
    return Cacher('https://people.onliner.by/feed')


@pytest.mark.parametrize('date_data, parsed_date', [
    ['2021-10-23T23:32:33Z', 20211023],
    ['Sat, 23 Oct 2021 19:49:56 +0300', 20211023],
    ['Sun, 24 Oct 2021 14:59:50 GMT', 20211024],
],
                         )
def test_get_convert_date(cacher_instance, date_data, parsed_date):
    """
    Checks available date formats
    :param cacher_instance: object class Cacher
    :param date_data: data with date for convert
    :param parsed_date: expected data
    """
    datetime_obj = cacher_instance._get_convert_date(date_data)
    assert (datetime_obj == parsed_date)


def test_get_convert_date_raises_ValueError(cacher_instance):
    """
    Checks raise ValueError if date formats invalid
    :param cacher_instance: object class Cacher
    """
    invalid_date = 'Sego 2021.10.21'
    with pytest.raises(ValueError):
        cacher_instance._get_convert_date(invalid_date)
