import sys


def _version() -> str:
    try:
        if sys.version_info >= (3, 8):
            from importlib import metadata
        else:
            import importlib_metadata as metadata
    except ImportError:
        raise Exception(
            "Version number unavailable. importlib-metadata is required for Python 3.7"
        )

    return metadata.version(__name__)


__version__ = _version()
