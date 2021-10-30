from .cstream import CStream, NullStream
from .constants import (
    stderr,
    stdlog,
    stdwar,
    stdout,
    devnull,
    DEBUG,
    INFO,
    WARNING,
    ERROR,
    CRITICAL,
)

CStream.init()

__all__ = [
    "CStream",
    "NullStream",
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