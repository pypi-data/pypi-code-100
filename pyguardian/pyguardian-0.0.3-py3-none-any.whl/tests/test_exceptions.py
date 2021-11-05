from pyguardian import guard
from pyguardian.errors import InvalidArgumentTypeError
import pytest

# Methods to test

@guard(bool, int)
def foo_bad(a, b):
	pass

@guard(bool, (int, float))
def foo_multi_bad(a, b):
	pass

@guard(bool, int)
def bar_bad(a, *args):
	pass

@guard(bool, (int, float))
def bar_multi_bad(a, *args):
	pass

@guard(int, str)
def baz_bad(a, **kwargs):
	pass

@guard(bool, (int, float))
def baz_multi_bad(a, **kwargs):
	pass

@guard(int, str)
def qux_bad(*args, **kwargs):
	pass

@guard((int, float), (bool, str))
def qux_multi_bad(*args, **kwargs):
	pass

# Actual tests

def test_foo_bad():
	with pytest.raises(InvalidArgumentTypeError):
		foo_bad("not int", 1)

def test_foo_multi_bad():
	with pytest.raises(InvalidArgumentTypeError):
		foo_multi_bad(True, "not int or float")

def test_bar_bad():
	with pytest.raises(InvalidArgumentTypeError):
		bar_bad(True, 1, 2, 3, "not int", 5)

def test_bar_multi_bad():
	with pytest.raises(InvalidArgumentTypeError):
		bar_multi_bad(True, 1, 2, 3.4, "not int or float", 5.6)

def test_baz_bad():
	with pytest.raises(InvalidArgumentTypeError):
		baz_bad(1, x=False, y="World")

def test_baz_multi_bad():
	with pytest.raises(InvalidArgumentTypeError):
		baz_multi_bad(True, x="not int or float", y=2.3, z=3)

def test_qux_bad():
	with pytest.raises(InvalidArgumentTypeError):
		qux_bad(1, 2, 3, x="Hello", y=False)

def test_qux_multi_bad():
	with pytest.raises(InvalidArgumentTypeError):
		qux_multi_bad(1, 2.3, "not int or float", 5.6, x=True, y="Hello")
