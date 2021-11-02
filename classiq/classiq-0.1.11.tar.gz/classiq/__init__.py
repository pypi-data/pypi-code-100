"""Classiq SDK."""

import sys

from classiq.async_utils import enable_jupyter_notebook, is_notebook as _is_notebook
from classiq.authentication.authentication import (  # noqa: F401
    register_device as authenticate,
)
from classiq.client import configure  # noqa: F401
from classiq.exceptions import ClassiqVersionError


def _version() -> str:
    try:
        if sys.version_info >= (3, 8):
            from importlib import metadata
        else:
            import importlib_metadata as metadata
    except ImportError:
        raise ClassiqVersionError(
            "Version number unavailable. importlib-metadata is required for Python 3.7"
        )

    return metadata.version(__name__)


__version__ = _version()

if _is_notebook():
    enable_jupyter_notebook()
