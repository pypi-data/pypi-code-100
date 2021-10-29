__version__ = "1.1.0"


import importlib
import importlib.util
import os
import sys

import pyftype
from pyftype.utils import get_bytes

__kinds = []
__package_dir = os.path.join(os.path.dirname(__file__), "modules")
for root, _, files in os.walk(__package_dir):
    for f in files:
        if "__" in f:
            continue
        if f.endswith(".pyc"):
            continue
        name = os.path.basename(f[:-3])
        location = os.path.join(root, f)
        spec = importlib.util.spec_from_file_location(name, location)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)

        for item in dir(module):
            if "_" in item:
                continue
            if item == "Type":
                continue
            t = getattr(module, item)
            if isinstance(t, type):
                __kinds.append(t())


def _match(obj, matchers=__kinds):
    """
    类型匹配

    Args:
        obj: path to file, bytes or bytearray.

    Returns:
        Type instance if type matches. Otherwise None.

    Raises:
        TypeError: if obj is not a supported type.
    """
    buf = get_bytes(obj)

    for matcher in matchers:
        if matcher.match(buf):
            return matcher

    return None


def guess(obj):
    """
    判断文件类型

    Args:
        obj: path to file, bytes or bytearray.

    Returns:
        The matched type instance. Otherwise None.

    Raises:
        TypeError: if obj is not a supported type.
    """
    return _match(obj) if obj else None


def guess_mime(obj):
    """
    Infers the file type of the given input
    and returns its MIME type.

    Args:
        obj: path to file, bytes or bytearray.

    Returns:
        The matched MIME type as string. Otherwise None.

    Raises:
        TypeError: if obj is not a supported type.
    """
    kind = guess(obj)
    return kind.mime if kind else kind


def guess_extension(obj):
    """
    Infers the file type of the given input
    and returns its RFC file extension.

    Args:
        obj: path to file, bytes or bytearray.

    Returns:
        The matched file extension as string. Otherwise None.

    Raises:
        TypeError: if obj is not a supported type.
    """
    kind = guess(obj)
    return kind.extension if kind else kind
