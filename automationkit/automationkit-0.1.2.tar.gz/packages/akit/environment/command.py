"""
.. module:: command
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that is utilized by the shell command to activate the environment. We
               utilize a special activation module for command activations so we can turn off
               logging to the console and to files unless logging parameters are passed.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2020, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

import os
from logging.handlers import RotatingFileHandler

# For console activation we don't want to log to the console and we want
# to point the logs to a different output folder
os.environ["AKIT_CONSOLE_LOG_LEVEL"] = "QUIET"
os.environ["AKIT_JOBTYPE"] = "console"

import akit.environment.activate # pylint: disable=unused-import,wrong-import-position

from akit.xlogging.foundations import logging_initialize, LoggingDefaults # pylint: disable=wrong-import-position

LoggingDefaults.DefaultFileLoggingHandler = RotatingFileHandler
logging_initialize()
