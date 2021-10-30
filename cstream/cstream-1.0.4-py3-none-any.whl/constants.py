"""
src/cstream/constants.py
"""
# Standard Library
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

# Local
from .cstream import CStream, NullStream

CStream.config(level=WARNING)

stdout = CStream(end="\n", level=None)
stderr = CStream(end="\n", fg="RED", level=ERROR)
stdwar = CStream(end="\n", fg="YELLOW", level=WARNING)
stdlog = CStream(end="\n", level=DEBUG)
devnull = NullStream()

__all__ = [
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
    "stdout",
    "stderr",
    "stdwar",
    "stdlog",
    "devnull",
]
