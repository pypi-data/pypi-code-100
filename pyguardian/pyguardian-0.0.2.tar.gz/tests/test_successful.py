from pyguardian import guard
from pyguardian.errors import InvalidArgumentTypeError
from tests.ctx_managers import not_raises

# Methods to test

@guard(bool, int)
def foo(a, b):
    pass

@guard(bool, (int, float))
def foo_multi(a, b):
    pass

@guard(bool, int)
def bar(a, *args):
    pass

@guard(bool, (int, float))
def bar_multi(a, *args):
    pass

@guard(int, str)
def baz(a, **kwargs):
    pass

@guard(bool, (int, float))
def baz_multi(a, **kwargs):
    pass

@guard(int, str)
def qux(*args, **kwargs):
    pass

@guard((int, float), (bool, str))
def qux_multi(*args, **kwargs):
    pass

# Actual tests

def test_foo():
    with not_raises(InvalidArgumentTypeError):
        foo(True, 1)

def test_foo_multi():
    with not_raises(InvalidArgumentTypeError):
        foo_multi(True, 1.2)

def test_bar():
    with not_raises(InvalidArgumentTypeError):
        bar(True, 1, 2, 3, 4, 5)

def test_bar_multi():
    with not_raises(InvalidArgumentTypeError):
        bar_multi(True, 1, 2, 3.4, 4, 5.6)

def test_baz():
    with not_raises(InvalidArgumentTypeError):
        baz(1, x="Hello", y="World")

def test_baz_multi():
    with not_raises(InvalidArgumentTypeError):
        baz_multi(True, x=1, y=2.3, z=3)

def test_qux():
    with not_raises(InvalidArgumentTypeError):
        qux(1, 2, 3, x="Hello", y="World")

def test_qux_multi():
    with not_raises(InvalidArgumentTypeError):
        qux_multi(1, 2.3, 4, 5.6, x=True, y="Hello")
