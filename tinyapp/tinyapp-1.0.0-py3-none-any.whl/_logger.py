#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging.handlers
import os.path


default_name = "tinyapp"


def init_app_logger(logfile, level, backup_count=180):
    logfile = os.path.abspath(logfile)
    logdir = os.path.dirname(logfile)
    os.makedirs(logdir, exist_ok=True)

    logger = logging.getLogger(default_name)
    logger.setLevel(level)

    formatter = logging.Formatter("[%(asctime)s][%(levelname)s] %(filename)s:%(lineno)s => %(message)s")

    handler = logging.handlers.TimedRotatingFileHandler(
        filename=logfile,
        when="midnight",
        interval=1,
        backupCount=backup_count,
        encoding="utf8"
    )
    handler.setLevel(level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def init():
    from ._config import get
    level = get("logger", "level", default="info").upper()
    logfile = get("logger", "filename", default="./logs/tinyapp.log")
    backup_count = int(get("logger", "backup", default=180))
    init_app_logger(logfile, level, backup_count)


app_logger = logging.getLogger(default_name)
