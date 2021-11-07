#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python library to communicate with an obs-websocket server.
"""
from pathlib import Path

from single_source import get_version
from .core import ObsWS, open_obs_websocket  # noqa: F401
__version__ = get_version(__name__, Path(__file__).parent.parent)
