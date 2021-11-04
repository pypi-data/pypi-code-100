#!/usr/bin/env/python
"""Log simply v2."""
import logging
import logging.config
from pathlib import Path
import yaml  # type: ignore


def log_config(config: Path = Path("logging.yaml")):
    """Read Logging Config YAML file."""
    with open(config, "r") as stream:
        try:
            logging_config = yaml.safe_load(stream)
        except yaml.YAMLError:
            # no config so take defaults
            pass
    logging.config.dictConfig(logging_config)
