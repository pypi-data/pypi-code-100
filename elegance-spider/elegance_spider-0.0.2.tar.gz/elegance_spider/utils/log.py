import sys
import logging

from elegance_spider.conf import settings


class Logger(object):
    def __init__(self):
        self._logger = logging.getLogger()
        self.formatter = logging.Formatter(
            fmt=settings.DEFAULT_LOG_FMT, datefmt=settings.DEFAULT_LOG_DATEFMT)
        self._logger.addHandler(self._get_file_handler(
            settings.DEFAULT_LOG_FILENAME))
        self._logger.addHandler(self._get_console_handler())
        self._logger.setLevel(settings.DEFAULT_LOG_LEVEL)

    def _get_file_handler(self, filename):
        filehandler = logging.FileHandler(filename=filename, encoding='utf-8')
        filehandler.setFormatter(self.formatter)
        return filehandler

    def _get_console_handler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.formatter = self.formatter
        return console_handler

    @property
    def logger(self):
        return self._logger


logger = Logger().logger
