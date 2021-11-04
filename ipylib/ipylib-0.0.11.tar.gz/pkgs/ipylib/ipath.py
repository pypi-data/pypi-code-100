# -*- coding: utf-8 -*-
import os
from pathlib import PureWindowsPath, PurePosixPath

from idebug import *


__all__ = [
    'clean_path',
]


def clean_path(p):
    # 운영체제 타입에 따라 path 를 수정한다
    if os.name == 'posix':
        return str(PurePosixPath(p))
    elif os.name == 'nt':
        return str(PureWindowsPath(p))
