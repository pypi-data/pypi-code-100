import os
import sys
import inspect
import rich.pretty
from loguru import logger

import pyhelios
import pyhelios.toml

pyhelios_path = os.path.dirname(inspect.getfile(pyhelios))
pyproject = os.path.join(pyhelios_path, "..", "pyproject.toml")
metadata = pyhelios.toml.read(pyproject)

__version__ = metadata["tool"]["poetry"]["version"]
__authors__ = metadata["tool"]["poetry"]["authors"]
__maintainers__ = metadata["tool"]["poetry"]["maintainers"]
__license__ = metadata["tool"]["poetry"]["license"]
__description__ = metadata["tool"]["poetry"]["description"]

rich.pretty.install()

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
