from pyguardian import guard
from pyguardian.errors import UnknownKeywordArgumentWarning
import pytest

# Methods to test

@guard(n=int)
def foo():
    pass

@guard(n=int)
def bar(*args):
    pass

@guard(n=int)
def baz(**kwargs):
    pass

@guard(int, n=int, b=int)
def baz(a, b):
    pass

# Actual tests

def test_foo():
    with pytest.warns(UnknownKeywordArgumentWarning):
        foo()
        
def test_bar():
    with pytest.warns(UnknownKeywordArgumentWarning):
        bar()
        
def test_baz():
    with pytest.warns(UnknownKeywordArgumentWarning):
        baz(1, 2)
