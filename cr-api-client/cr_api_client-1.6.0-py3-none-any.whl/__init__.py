#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

from loguru import logger


# Initialize loguru
config = {
    "handlers": [
        {
            "sink": sys.stdout,
            "format": "<green>{time:HH:mm:ss}</green>|<level>{level: ^7}</level>| {message}",
        },
    ],
    "extra": {"user": "someone"},
}
logger.configure(**config)
