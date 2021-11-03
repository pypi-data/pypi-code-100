#!/bin/false
# -*- coding: utf-8 -*-

"""
This module provides unit tests for `ptutils.punning`.
"""
import pytest
import math
from ptutils.encoding import HAVE_YAML
from ptutils.punning import to_string, boolify, listify, as_numeric, as_encoded, as_literal, canonize
from ptutils.undefined import UNDEFINED


class C:
    pass


c = C()


TO_STRING_TEST_CASES = [
    (b"hello", "hello"),
    ("hello", "hello"),
    (5, "5"),
    (None, "None"),
    (False, "False"),
    (True, "True"),
    ([True, 1], "[True, 1]"),
    (list(), "[]"),
    ({"a": True, "b": 1}, "{'a': True, 'b': 1}"),
    (dict(), "{}"),
    (c, str(c))
]


@pytest.mark.parametrize(
    argnames  = ["obj", "expected"],
    argvalues = TO_STRING_TEST_CASES,
    ids       = [f"{repr(x[0])}->{repr(x[1])}" for x in TO_STRING_TEST_CASES]
)
def test_to_string(obj, expected):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected) as _:
            to_string(obj)
    else:
        assert to_string(obj) == expected


BOOLIFY_TEST_CASES = [
    # normal cases
    (False, False),
    (True, True),
    (None, False),
    (UNDEFINED, False),
    ("yes", True),
    ("on", True),
    ("enabled", True),
    ("true", True),
    ("YES", True),
    ("ON", True),
    ("EnAbLeD", True),
    ("trUE", True),
    ("1", True),
    ("no", False),
    ("disabled", False),
    ("off", False),
    ("false", False),
    ("0", False),
    # error cases
    (b"hello", TypeError),
    ("hello", TypeError),
    (5, TypeError),
    ([True, 1], TypeError),
    (list(), TypeError),
    ({"a": True, "b": 1}, TypeError),
    (dict(), TypeError),
]


@pytest.mark.parametrize(
    argnames  = ["obj", "expected"],
    argvalues = BOOLIFY_TEST_CASES,
    ids       = [f"{repr(x[0])}->{repr(x[1])}" for x in BOOLIFY_TEST_CASES]
)
def test_boolify(obj, expected):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected) as _:
            boolify(obj)
    else:
        assert boolify(obj) == expected


LISTIFY_TEST_CASES = [
    (None,               False, [None]),
    ("a",                False, ["a"]),
    (1,                  False, [1]),
    (1.5,                False, [1.5]),
    (False,              False, [False]),
    (c,                  False, [c]),
    ({'a': 1, 'b': 'B'}, False, [{'a': 1, 'b': 'B'}]),
    ([1, 2, 3],          False, [1, 2, 3]),
    (set([1, 2, 3]),     False, set([1, 2, 3])),
    (tuple([1, 2, 3]),   False, tuple([1, 2, 3])),
    (None,               True, [None]),
    ("a",                True, ["a"]),
    (1,                  True, [1]),
    (1.5,                True, [1.5]),
    (False,              True, [False]),
    (c,                  True, [c]),
    ({'a': 1, 'b': 'B'}, True, [{'a': 1, 'b': 'B'}]),
    ([1, 2, 3],          True, [1, 2, 3]),
    (set([1, 2, 3]),     True, [1, 2, 3]),
    (tuple([1, 2, 3]),   True, [1, 2, 3])
]


@pytest.mark.parametrize(
    argnames  = ["obj", "strict", "expected"],
    argvalues = LISTIFY_TEST_CASES,
    ids       = [f"{repr(x[0])}->{repr(x[1])}" for x in LISTIFY_TEST_CASES]
)
def test_listify(obj, strict, expected):
    assert listify(obj, strict=strict) == expected


CANONIZE_TEST_CASES = [
    (None,                    False, None),
    ("a",                     False, "a"),
    (1,                       False, 1),
    (1.5,                     False, 1.5),
    (False,                   False, False),
    (c,                       False, c),
    ({'a': 1, 'b': 'B'},      False, {'a': 1, 'b': 'B'}),
    ([1, 2, 3],               False, [1, 2, 3]),
    (set([1, 2, 3]),          False, {1, 2, 3}),
    (tuple([1, 2, 3]),        False, tuple([1, 2, 3])),
    ("None",                  False, None),
    ("null",                  False, None),
    ("'None'",                False, None),
    ("'null'",                False, None),
    ('"a"',                   False, "a"),
    ("1",                     False, 1),
    ("1.5",                   False, 1.5),
    ("False",                 False, False),
    ('{"a": 1, "b": "B"}',    False, {'a': 1, 'b': 'B'}),
    ("[1, 2, 3]",             False, [1, 2, 3]),
    ("---\n",                 True, None),
    ("---\n- 1\n- 2\n- 3",    True, [1, 2, 3]),
    ("---\na: 1\nb: 2\nc: 3", True, {'a': 1, 'b': 2, 'c': 3}),
    ("this shouldn't parse",  False, "this shouldn't parse"),
    (b'{"a": 1, "b": "B"}',   False, {'a': 1, 'b': 'B'}),
    (b'true',                 False, True),
    (b'fAlsE',                False, False),
    ("---\ninvalid yaml: : :- ::", True, "---\ninvalid yaml: : :- ::"),

]


@pytest.mark.parametrize(
    argnames  = ["obj", "expect_yaml", "expected"],
    argvalues = CANONIZE_TEST_CASES,
    ids       = [f"{repr(x[0])}->{repr(x[1])}" for x in CANONIZE_TEST_CASES]
)
def test_canonize(obj, expect_yaml, expected):
    if expect_yaml and not HAVE_YAML:
        pytest.skip("YAML support unavailable on this platform")

    assert canonize(obj) == expected


AS_NUMERIC_TEST_CASES = [
    (None,                    TypeError),
    ("a",                     ValueError),
    ("+inf",                  float("+inf")),
    ("-inf",                  float("-inf")),
    ("nan",                   float("nan")),
    (1,                       1),
    (1.5,                     1.5),
    ("1",                     1),
    ("1.5",                   1.5),
]


@pytest.mark.parametrize(
    argnames  = ["obj", "expected"],
    argvalues = AS_NUMERIC_TEST_CASES,
    ids       = [f"{repr(x[0])}->{repr(x[1])}" for x in AS_NUMERIC_TEST_CASES]
)
def test_as_numeric(obj, expected):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected) as _:
            as_numeric(obj)
    else:
        v = as_numeric(obj)
        if math.isnan(v):
            assert math.isnan(expected)

        elif math.isinf(v):
            assert math.isinf(expected)

        else:
            assert v == expected
