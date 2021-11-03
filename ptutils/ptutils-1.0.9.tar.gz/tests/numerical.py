#!/bin/false
# -*- coding: utf-8 -*-

"""
This module provides unit tests for `ptutils.numerical`.
"""

from ptutils.numerical import __NAN__
from math import isnan


def test_nan():
    assert isnan(__NAN__)
