import logging


def set_package_logger_handler():
    logger = logging.getLogger('switchcraft')
    logger.addHandler(logging.NullHandler())
    logger.propagate = False
