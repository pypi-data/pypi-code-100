"""
Utility Functions
=================


"""
import logging
import os
from argparse import Namespace

import yaml

logger = logging.getLogger(__name__)


def validate_folder(folder: str) -> None:
    """Validate target folder exists, if not exist, an empty folder will be created.

    :param folder: folder path
    """
    if os.path.isfile(folder):
        raise FileExistsError("Target folder path exists by file")
    os.makedirs(os.path.abspath(folder), exist_ok=True)


def _get_logging_level(level: str):
    try:
        return getattr(logging, level.upper())
    except AttributeError:
        print("Logging level (%s) not match, use default level (info)" % level)
        return logging.INFO

def set_log(level: str = 'info') -> None:
    """Set Logger level

    :param level: info|warn|error|critical etc.
    """
    level = _get_logging_level(level)
    logging.basicConfig(level=level,
                        format='%(name)-25s:%(funcName)20s:%(lineno)d:%(levelname)-8s: %(message)s')


def set_adv_log(screen_level:str = 'info', log_file:str=None, file_log_level:str="info", skip = (), skip_level='warning', **kwargs) -> None:
    screen_level = _get_logging_level(screen_level)
    if log_file is None:
        set_log(screen_level)
        return

    file_log_level = _get_logging_level(file_log_level)
    logging.basicConfig(level=file_log_level,
                        format='%(asctime)s:%(name)-25s:%(funcName)20s:%(lineno)d:%(levelname)-8s: %(message)s',
                        filename=log_file, **kwargs)

    screen_handler = logging.StreamHandler()
    screen_handler.setLevel(screen_level)
    formatter = logging.Formatter('%(name)-25s:%(funcName)20s:%(lineno)d:%(levelname)-8s: %(message)s')
    screen_handler.setFormatter(formatter)
    logging.getLogger().addHandler(screen_handler)

    skip_level = _get_logging_level(skip_level)
    for skip_logger in skip:
        logging.getLogger(skip_logger).setLevel(skip_level)


def load_yaml_namespace(filename: str) -> Namespace:
    """Load YAML config into a Namespace object

    :param filename: YAML file
    :return: Namespace object that attributes are accessible directly
    """
    config = yaml.safe_load(open(filename))
    return Namespace(**config)
