"""
Guilded API Wrapper
~~~~~~~~~~~~~~~~~~~~
An Asynchronous, Pythonic API Wrapper For The Guilded API
:copyright: (c) 2021-present VincentRPS
:license: Apache-2.0, see LICENSE for more details.
"""

__title__ = 'OneGuild'
__author__ = 'VincentRPS'
__license__ = 'Apache-2.0'
__copyright__ = 'Copyright 2021-present VincentRPS'
__version__ = '0.1'

__path__ = __import__('pkgutil').extend_path(__path__, __name__)

import logging
from typing import NamedTuple, Literal

from .message import *


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info: VersionInfo = VersionInfo(major=0, minor=0, micro=1, releaselevel='final', serial=0)

logging.getLogger(__name__).addHandler(logging.NullHandler())
