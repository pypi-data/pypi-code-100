"""Main module for working with APP"""

import os
import sys
from pathlib import Path

import logging

sys.path.append(os.path.dirname(os.getcwd()))

from grebarss_reader.config import AppLogger
from grebarss_reader.grebarss_parser import RssParser

AppLogger.init_logger('app')
logger = logging.getLogger("app.rss_reader")


def main():
    """Starts APP"""
    rss_parser = RssParser()
    try:
        rss_parser.start()
    except Exception as exc_obj:
        logger.exception(f"Rss reader crashed from {exc_obj}")
        print(f"Rss reader crashed from {type(exc_obj).__name__}. For more information see log file.")


if __name__ == "__main__":
    logger.info('RSS reader started working.')
    main()
    logger.info('RSS reader finished working.')
