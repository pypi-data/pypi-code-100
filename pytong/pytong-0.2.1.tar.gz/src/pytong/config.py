#!/usr/bin/env/python
"""
Log v2 within a package.

This takes a logging.yaml configuration file that can either be just
for this package or for all libraries that are compliant.
"""
import logging
import logging.config
from pathlib import Path
import yaml  # type: ignore

log = logging.getLogger(__name__)


def log_config(config: Path = Path("logging.yaml")):
    """Read Logging Config YAML file."""
    log.warning(f"{Path.cwd()=}")
    with open(config, "r") as stream:
        try:
            logging_config = yaml.safe_load(stream)
        except yaml.YAMLError:
            # no config so take defaults
            pass
    logging.config.dictConfig(logging_config)
