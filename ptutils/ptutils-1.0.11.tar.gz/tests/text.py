#!/bin/false
# -*- coding: utf-8 -*-

"""
This module provides unit tests for `ptutils.text`.
"""
import pytest
from ptutils.text import strip_quotes, strip_brackets, strip_line_ending


STRIP_QUOTES_TEST_CASES = [
    (b"'''hello'''", b"'''hello'''"),
    ("'hello'", "hello"),
    ('"hello"', "hello"),
    ('4', "4"),
    ('"4', '"4'),
    ("'4", "'4"),
]


@pytest.mark.parametrize(
    argnames  = ["obj", "expected"],
    argvalues = STRIP_QUOTES_TEST_CASES,
    ids       = [f"{repr(x[0])}->{repr(x[1])}" for x in STRIP_QUOTES_TEST_CASES]
)
def test_strip_quotes(obj, expected):
    assert strip_quotes(obj) == expected


SQUARE_BRACKETS = [['[', ']']]
CURLY_BRACKETS  = [['{', '}']]
PAREN_BRACKETS  = [['(', ')']]
DEFAULT_BRACKETS = SQUARE_BRACKETS + CURLY_BRACKETS + PAREN_BRACKETS

STRIP_BRACKETS_TEST_CASES = [
    (b"[[hello]]", DEFAULT_BRACKETS, b"[[hello]]"),
    ("",             DEFAULT_BRACKETS,                  ""),
    ("[]",           DEFAULT_BRACKETS,                  ""),
    ("[",            DEFAULT_BRACKETS,                  "["),
    ("[[[hello]]]",  DEFAULT_BRACKETS,                  "hello"),
    ("{([hello])}",  DEFAULT_BRACKETS,                  "hello"),
    ("({[hello]})",  DEFAULT_BRACKETS,                  "hello"),
    ("([{hello}])",  DEFAULT_BRACKETS,                  "hello"),
    ("[hello]",      DEFAULT_BRACKETS,                  "hello"),
    ("{hello}",      DEFAULT_BRACKETS,                  "hello"),
    ("(hello)",      DEFAULT_BRACKETS,                  "hello"),
    ("hello",        DEFAULT_BRACKETS,                  "hello"),
    ("{hello}",      SQUARE_BRACKETS,                   "{hello}"),
    ("{hello}",      PAREN_BRACKETS,                    "{hello}"),
    ("{hello}",      SQUARE_BRACKETS + PAREN_BRACKETS,  "{hello}"),
    ("[hello]",      CURLY_BRACKETS,                    "[hello]"),
    ("[hello]",      PAREN_BRACKETS,                    "[hello]"),
    ("[hello]",      CURLY_BRACKETS + PAREN_BRACKETS,   "[hello]"),
    ("{([",          DEFAULT_BRACKETS,                  "{(["),
    ("({[",          DEFAULT_BRACKETS,                  "({["),
    ("([{",          DEFAULT_BRACKETS,                  "([{"),
]


@pytest.mark.parametrize(
    argnames  = ["obj", "brackets", "expected"],
    argvalues = STRIP_BRACKETS_TEST_CASES,
    ids       = [f"{repr(x[0])}->{repr(x[1])}" for x in STRIP_BRACKETS_TEST_CASES]
)
def test_strip_brackets(obj, brackets, expected):
    assert strip_brackets(obj, brackets=brackets) == expected


STRIP_LINE_ENDING_TEST_CASES = [
    ("abc\r\n\r\ndef\r\n", "abc\r\n\r\ndef"),
    ("abc\r\n\r\ndef",     "abc\r\n\r\ndef"),
    ("abc\r\n\r\ndef\r",   "abc\r\n\r\ndef"),
    ("abc\r\n\r\ndef\n",   "abc\r\n\r\ndef"),
    ("abc\r\n\r",          "abc"),
    ("\r\n\r",             ""),
    (b"abc\r\n\r\ndef\r\n", TypeError),
    (b"abc\r\n\r\ndef",     TypeError),
    (b"abc\r\n\r\ndef\r",   TypeError),
    (b"abc\r\n\r\ndef\n",   TypeError),
    (b"abc\r\n\r",          TypeError),
    (b"\r\n\r",             TypeError),
    (None,                  AttributeError)
]


@pytest.mark.parametrize(
    argnames  = ["obj", "expected"],
    argvalues = STRIP_LINE_ENDING_TEST_CASES,
    ids       = [f"{repr(x[0])}->{repr(x[1])}" for x in STRIP_LINE_ENDING_TEST_CASES]
)
def test_strip_line_ending(obj, expected):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected) as _:
            strip_line_ending(obj)
    else:
        assert strip_line_ending(obj) == expected
