#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module provides unit tests for `ptutils.encoding`."""

import pytest
import datetime
from ptutils.encoding import (
    HAVE_YAML,
    encode_json,
    encode_yaml,
    pretty_json,
    pretty_yaml,
    decode_json,
    decode_yaml,
    json_serial
)


def test_json_serial_handles_datetime():
    val = json_serial(datetime.datetime.utcnow())
    assert isinstance(val, str)
    assert bool(val)


def test_json_serial_handles_timedelta():
    val = json_serial(datetime.timedelta(seconds=5))
    assert isinstance(val, (int, float))
    assert val == 5


def test_json_serial_fails_with_unknown_class():
    class C:
        pass
    with pytest.raises(TypeError) as _:
        _ = json_serial(C())


NATIVE_CASES = [
    None,
    "string",
    123456,
    123456.789,
    True,
    False,
    [],
    [None],
    ["a", 2, 3.0, True, False, {}],
    {"a": 1, "5": 123, "p": False}
]


@pytest.mark.parametrize(
    "test_case",
    NATIVE_CASES,
    ids = [f"NATIVE_CASES[{i}]" for i in range(len(NATIVE_CASES))]
)
def test_json_roundtrip(test_case):
    encoded_test_case = encode_json(test_case)
    assert isinstance(encoded_test_case, str)
    assert bool(encoded_test_case)
    decoded_test_case = decode_json(encoded_test_case)
    assert decoded_test_case == test_case


@pytest.mark.parametrize(
    "test_case",
    NATIVE_CASES,
    ids = [f"NATIVE_CASES[{i}]" for i in range(len(NATIVE_CASES))]
)
def test_json_pretty_roundtrip(test_case):
    encoded_test_case = pretty_json(test_case)
    assert isinstance(encoded_test_case, str)
    assert bool(encoded_test_case)
    decoded_test_case = decode_yaml(encoded_test_case)
    assert decoded_test_case == test_case


@pytest.mark.parametrize(
    "test_case",
    NATIVE_CASES,
    ids = [f"NATIVE_CASES[{i}]" for i in range(len(NATIVE_CASES))]
)
def test_yaml_roundtrip(test_case):
    if HAVE_YAML:
        encoded_test_case = encode_yaml(test_case)
        assert isinstance(encoded_test_case, str)
        assert bool(encoded_test_case)
        decoded_test_case = decode_yaml(encoded_test_case)
        assert decoded_test_case == test_case
    else:
        pytest.skip("No YAML support")


@pytest.mark.parametrize(
    "test_case",
    NATIVE_CASES,
    ids = [f"NATIVE_CASES[{i}]" for i in range(len(NATIVE_CASES))]
)
def test_yaml_pretty_roundtrip(test_case):
    if HAVE_YAML:
        encoded_test_case = pretty_yaml(test_case)
        assert isinstance(encoded_test_case, str)
        assert bool(encoded_test_case)
        decoded_test_case = decode_yaml(encoded_test_case)
        assert decoded_test_case == test_case
    else:
        pytest.skip("No YAML support")
