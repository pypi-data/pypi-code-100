"""
utilities shared by bdrc_utils
"""
import argparse
import os
import sys
from pathlib import Path
from typing import AnyStr


def reallypath(what_path: AnyStr) -> Path:
    """
    Resolves everything about the path
    :param what_path: Pathlike object
    :return: fully resolved path
    """
    from os import path

    # jimk #499: detect non-file paths and don't expand
    if what_path is None:
        return None
    # Regex more elegant, but need fastway to say UNCs must be at beginning
    if what_path.find('://') > 0 or what_path.startswith('//') or what_path.startswith('\\'):
        return what_path

    return path.realpath(path.expandvars(path.expanduser(what_path)))


def get_work_facts(a_path: str) -> (int, int):
    """
    Returns the sum of all file sizes and file count in a path
    64 bit python platforms (2 and 3)report sys.maxsize as
    9,223,372,036,854,775,807  or 9 exaBytes.
    """
    size: int = 0
    _count: int = 0
    from os.path import join, getsize
    for root, dirs, files in os.walk(a_path):
        size += sum(getsize(join(root, name)) for name in files)
        _count += len(files)
    return size, _count


def get_work_image_facts(a_path: str, image_folder_name: str = 'images') -> (int, int, int, int):
    """
    Returns a tuple of the:
    - non image total size
    - non image file count
    - images total file size
    - images total file count
    """
    _size: int = 0
    _count: int = 0
    _page_size: int = 0
    _page_count: int = 0
    from os.path import join, getsize
    for root, dirs, files in os.walk(a_path):
        if root.find(image_folder_name) > 0:
            _page_size += sum(getsize(join(root, name)) for name in files)
            _page_count += len(files)
        else:
            _size += sum(getsize(join(root, name)) for name in files)
            _count += len(files)
    return _size, _count, _page_size, _page_count

