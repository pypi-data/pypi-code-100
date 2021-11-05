import os
import sys
import inspect
import rich.pretty
from loguru import logger
from importlib.metadata import metadata

# -- Get the Metadata.
__version__ = metadata("pyhelios")["Version"]
__author__ = metadata("pyhelios")["Author"]
__maintainer__ = metadata("pyhelios")["Maintainer"]
__license__ = metadata("pyhelios")["License"]
__description__ = metadata("pyhelios")["Summary"]

# -- Configure the rich package.
rich.pretty.install()

# -- Configure le loguru package.
config = {
    "handlers": [
        {
            "sink": sys.stderr,
            "filter": lambda record: record["level"].name == "ERROR",
            "format": "<g>[{time:HH:mm:ss}]</g> <lvl>[{level}]</lvl> <lvl>{message}</lvl> <cyan>{name}</cyan>:<magenta>{line}</magenta>",
        },
        {
            "sink": sys.stdout,
            "filter": lambda record: record["level"].name == "INFO",
            "format": "<g>[{time:HH:mm:ss}]</g> <lvl>[{level}]</lvl> {message}",
        },
    ]
}
logger.configure(**config)
logger.level("ERROR", color="<red>")
logger.level("INFO", color="<green>")
