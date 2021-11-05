from contextlib import contextmanager
import pytest

@contextmanager
def not_raises(e):
    try:
        yield
    except e:
        raise pytest.fail(f"DID RAISE EXCEPTION: {e}")

