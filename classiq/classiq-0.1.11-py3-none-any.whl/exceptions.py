import logging

CLASSIQ_LOGGER = None


def logger():
    global CLASSIQ_LOGGER
    if CLASSIQ_LOGGER is None:
        CLASSIQ_LOGGER = _initialize_logger()

    return CLASSIQ_LOGGER


def _initialize_logger():
    # Initialize a logger for classiq-usage
    logger = logging.getLogger("ClassiqLogger")
    # Set the format. Default logging format does not contain time information.
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
    # Add a console handler
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    # Show only warnings & errors
    consoleHandler.setLevel(logging.WARNING)
    # Register the console handler
    logger.addHandler(consoleHandler)

    return logger


class ClassiqError(Exception):
    def __init__(self, message):
        super().__init__(message)
        logger().error(f"{message}\n")


class ClassiqExecutionError(ClassiqError):
    pass


class ClassiqGenerationError(ClassiqError):
    pass


class ClassiqAnalyzerError(ClassiqError):
    pass


class ClassiqAPIError(ClassiqError):
    pass


class ClassiqVersionError(ClassiqError):
    pass


class ClassiqValueError(ClassiqError, ValueError):
    pass


class ClassiqAuthenticationError(ClassiqError):
    pass


class ClassiqExpiredTokenError(ClassiqAuthenticationError):
    pass
