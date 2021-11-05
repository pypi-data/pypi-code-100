import sys

if sys.version_info >= (3, 8):
    from importlib import metadata as importlib_metadata
else:
    import importlib_metadata


def get_by_key(key: str):
    return importlib_metadata.entry_points().get(key, ())
