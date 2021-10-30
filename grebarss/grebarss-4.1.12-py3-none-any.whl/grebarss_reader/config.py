"""Storage module with settings for argparse and logging"""

import logging
import sys
from enum import Enum
from pathlib import Path

import argparse


class AppConstant(Enum):
    """Class immutable values"""
    ACTUAL_VERSION = 'Version 4.1.0'


class AppArgParser:
    """Class for initializing arguments for working with CLI"""

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
        self.parser.add_argument('--version', action="version", version=AppConstant.ACTUAL_VERSION.value,
                                 help='Print version info')
        self.parser.add_argument('--json', action='store_true', help='Print result as JSON in stdout')
        self.parser.add_argument('--verbose', action="store_true", help='Outputs verbose status messages')
        self.parser.add_argument('--limit', type=int, default=None, help='Limit news topics if this parameter provided')
        self.parser.add_argument('source', nargs="?", default=None, help='URL RSS')
        self.parser.add_argument('--date', type=int, default=None,
                                 help='Print news published on a specific date from cache')
        self.parser.add_argument('--to-html', type=str, nargs="?", metavar="PATH",
                                 help="Convert news to HTML format and save them by the specified folder path")
        self.parser.add_argument('--to-pdf', type=str, nargs="?", metavar="PATH",
                                 help="Convert news to PDF format and save them by the specified folder path")

    def get_args(self) -> argparse.Namespace:
        """
        Initialization of arguments
        :return: object storing attributes
        """
        return self.parser.parse_args()


class AppLogger:
    """Class for initialization and setup logger and handlers"""

    FORMAT = '%(asctime)s - %(name)s:%(lineno)s - %(levelname)s - %(message)s'

    @staticmethod
    def init_logger(name):
        """Initialization and setup root logger. Setup and start file handler"""
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        current_dir = Path(__file__).parent.resolve()
        file_path = Path(current_dir, 'logs/grebarss_logs.log')

        fh = logging.FileHandler(filename=file_path, mode='w', encoding='utf-8')
        fh.setFormatter(logging.Formatter(AppLogger.FORMAT))
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)

    @staticmethod
    def activate_verbose():
        """Setup and start stream handler for verbose mode"""
        logger = logging.getLogger('app')
        sh = logging.StreamHandler(stream=sys.stdout)
        sh.setFormatter(logging.Formatter(AppLogger.FORMAT))
        sh.setLevel(logging.INFO)
        logger.addHandler(sh)
