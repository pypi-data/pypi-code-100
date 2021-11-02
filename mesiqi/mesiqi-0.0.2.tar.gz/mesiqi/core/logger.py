import json
import logging
import os
import re
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path, PurePath

from pythonjsonlogger import jsonlogger

NAME = "mesiqi"
LOG_LEVEL = logging._nameToLevel["INFO"]
DTFORMAT = "%Y-%m-%d %H:%M:%S%z"

TARGET_DIR = "mesiqi/target"
Path(Path(TARGET_DIR)).mkdir(parents=True, exist_ok=True)
LOG_FILE = TARGET_DIR + "/mesiqi.log"

# get package version
with open(Path(__file__).parent / "../__init__.py", encoding="utf-8") as f:
    result = re.search(r'__version__ = ["\']([^"\']+)', f.read())

    if not result:
        raise ValueError("Can't find the version in __init__.py")

    VERSION = result.group(1)


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(
        logging.Formatter(
            f"[%(asctime)s] %(levelname)s - %(name)s {VERSION} | %(message)s"
        )
    )
    return console_handler


def get_file_handler():
    supported_keys = [
        "levelname",
        "levelno",
        "asctime",
        "created",
        "filename",
        "funcName",
        "lineno",
        "module",
        "msecs",
        "message",
        "name",
        #'pathname',
        "process",
        "processName",
        "relativeCreated",
        #'thread',
        #'threadName',
    ]

    log_format = lambda x: ["%({0:s})s".format(i) for i in x]
    custom_format = " ".join(log_format(supported_keys))
    file_handler = logging.FileHandler(LOG_FILE, mode="a+")
    formatter = jsonlogger.JsonFormatter(
        custom_format, static_fields={"name": NAME, "version": VERSION}
    )
    file_handler.setFormatter(formatter)
    return file_handler


def get_logger(name: str = __name__):

    logging.basicConfig(
        datefmt=DTFORMAT,
        level=LOG_LEVEL,
        handlers=[get_console_handler(), get_file_handler()],
    )
    logger = logging.getLogger(name)

    return logger
