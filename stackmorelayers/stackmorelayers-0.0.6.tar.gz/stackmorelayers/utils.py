from functools import partial
from io import BytesIO
from pickle import dumps
from re import search, compile as re_compile, Pattern
from tarfile import TarInfo
from time import time
from typing import Tuple, Iterable, TypeVar, Union, Iterator, Any, Literal

__all__ = (
    'filter_search',
    'string_to_tarfile',
    'object_to_tarfile'
)

_T = TypeVar('_T')


def filter_search(regex: Union[str, Pattern], iterable: Iterable[_T]) -> Iterator[_T]:
    """
    Filter the elements of the input iterable by searching for the given pattern in its values.

    Args:
        regex:     pattern to search
        iterable:  input iterable
    Returns:
        Filter iterator
    """
    return filter(partial(search, re_compile(regex)), iterable)


def string_to_tarfile(filename: str, string: str) -> Tuple[BytesIO, TarInfo]:
    """
    Write string to a tarfile.

    Args:
        filename:  tarfile name
        string:    input string
    Returns:
        (BytesIO handle, TarInfo)
    """
    encoded = string.encode()
    tar_info = TarInfo(filename)
    tar_info.mtime = int(time())
    tar_info.size = len(encoded)
    return BytesIO(encoded), tar_info


def object_to_tarfile(filename: str,
                      obj: Any,
                      *,
                      protocol: Literal[0, 1, 2, 3, 4, 5]) -> Tuple[BytesIO, TarInfo]:
    """
    Write pickleable object to a tarfile.

    Args:
        filename:  tarfile name
        obj:       input object
        protocol:  pickle protocol to use

    Returns:
        (BytesIO handle, TarInfo)
    """
    encoded = dumps(obj, protocol=protocol)
    tar_info = TarInfo(filename)
    tar_info.mtime = int(time())
    tar_info.size = len(encoded)
    return BytesIO(encoded), tar_info
