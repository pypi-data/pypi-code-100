"Find the root of a bells project"
import logging
import os
import pathlib

def get_root():
    """Finds the root directory of the project"""
    cwd = pathlib.Path(os.getcwd())
    logging.debug("Current directory is %s", cwd)

    for directory in (cwd, *cwd.parents):
        config_dir = directory / ".bells"
        logging.debug("Checking if %s is the root", directory)
        if config_dir.is_dir():
            config_file = config_dir / "config.ini"
            if config_file.is_file():
                logging.debug("Found root: %s", directory)
                return directory.resolve()

    logging.debug("No root found")
    return False
