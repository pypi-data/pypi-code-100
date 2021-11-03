# vim: encoding=utf-8 ts=4 et sts=4 sw=4 tw=79 fileformat=unix nu wm=2
import pytest
from a28 import utils


def test_string_validation_short():
    assert utils.valid_string('ab', min_length=3) is False


def test_string_validation_long():
    assert utils.valid_string('abcdefghijklmnop', max_length=10) is False


def test_string_validation_invalid():
    assert utils.valid_string('!@£$%^&*(())__+') is False


def test_string_validation_valid():
    assert utils.valid_string('avalidword') is True


def test_confirm_nope(monkeypatch):
    # monkeypatch the "input" function, so that it returns "Mark".
    # This simulates the user entering "Mark" in the terminal:
    monkeypatch.setattr('builtins.input', lambda _: "nope")
    result = utils.confirm('test message')
    assert result is False


def test_confirm_y(monkeypatch):
    # monkeypatch the "input" function, so that it returns "Mark".
    # This simulates the user entering "Mark" in the terminal:
    monkeypatch.setattr('builtins.input', lambda _: "y")
    result = utils.confirm('test message')
    assert result is True


def test_confirm_yes(monkeypatch):
    # monkeypatch the "input" function, so that it returns "Mark".
    # This simulates the user entering "Mark" in the terminal:
    monkeypatch.setattr('builtins.input', lambda _: "yes")
    result = utils.confirm('test message')
    assert result is True


def test_confirm_ok(monkeypatch):
    # monkeypatch the "input" function, so that it returns "Mark".
    # This simulates the user entering "Mark" in the terminal:
    monkeypatch.setattr('builtins.input', lambda _: "ok")
    result = utils.confirm('test message')
    assert result is True


def test_confirm_sure(monkeypatch):
    # monkeypatch the "input" function, so that it returns "Mark".
    # This simulates the user entering "Mark" in the terminal:
    monkeypatch.setattr('builtins.input', lambda _: "sure")
    result = utils.confirm('test message')
    assert result is True


def test_confirm_alrighty(monkeypatch):
    # monkeypatch the "input" function, so that it returns "Mark".
    # This simulates the user entering "Mark" in the terminal:
    monkeypatch.setattr('builtins.input', lambda _: "alrighty")
    result = utils.confirm('test message')
    assert result is True


def test_confirm_ofcourse(monkeypatch):
    # monkeypatch the "input" function, so that it returns "Mark".
    # This simulates the user entering "Mark" in the terminal:
    monkeypatch.setattr('builtins.input', lambda _: "of course")
    result = utils.confirm('test message')
    assert result is True


def test_confirm_yup(monkeypatch):
    # monkeypatch the "input" function, so that it returns "Mark".
    # This simulates the user entering "Mark" in the terminal:
    monkeypatch.setattr('builtins.input', lambda _: "yup")
    result = utils.confirm('test message')
    assert result is True
