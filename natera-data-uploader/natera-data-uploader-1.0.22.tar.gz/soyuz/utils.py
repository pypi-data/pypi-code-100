#!/usr/bin/env python

import logging
import logging.config
import sys


def read_in_chunks(file_object, chunk_size=65536):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


class _ExcludeErrorsFilter(logging.Filter):
    def filter(self, record):
        """Filters out log messages with log level ERROR (numeric value: 40) or higher."""
        return record.levelno < 40


class Logging(object):
    config = {
        'version': 1,
        'filters': {
            'exclude_errors': {
                '()': _ExcludeErrorsFilter
            }
        },
        'formatters': {
            'include_process': {
                'format': '(%(process)d) %(asctime)s %(name)s (line %(lineno)s) | %(asctime)s %(levelname)-8s %(message)s'
            }
        },
        'handlers': {
            'console_stderr': {
                # Sends log messages with log level ERROR or higher to stderr
                'class': 'logging.StreamHandler',
                'level': 'ERROR',
                'formatter': 'include_process',
                'stream': sys.stderr
            },
            'console_stdout': {
                # Sends log messages with log level lower than ERROR to stdout
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'include_process',
                'filters': ['exclude_errors'],
                'stream': sys.stdout
            },
            'file': {
                # Sends all log messages to a file
                'class': 'logging.FileHandler',
                'level': 'DEBUG',
                'formatter': 'include_process',
                'filename': 'uploader.log',
                'encoding': 'utf8'
            }
        },
        'root': {
            # In general, this should be kept at 'NOTSET'.
            # Otherwise it would interfere with the log levels set for each handler.
            'level': 'NOTSET',
            'handlers': ['console_stderr', 'console_stdout', 'file']
        },
    }

    def get_log_file(self):
        return self.config["handlers"]["file"]["filename"]

    def set_log_file(self, log_file_path):
        self.config["handlers"]["file"]["filename"] = log_file_path

    def initialize(self):
        logging.config.dictConfig(self.config)


class UploaderException(BaseException):
    pass
