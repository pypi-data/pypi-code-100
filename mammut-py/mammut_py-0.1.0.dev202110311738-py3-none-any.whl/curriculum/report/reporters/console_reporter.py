from mammut.curriculum.report.reporters.base_reporter import BaseReporter
from mammut.curriculum.report.messages.message import CurriculumBaseMessage
import logging


class ConsoleReporter(BaseReporter):
    """Custom reporter for standard output message handling.

    TODO: constructor parameters must be replaced by configuration values.
    """

    def __init__(self, logger_name, threshold=logging.INFO):
        super(ConsoleReporter, self).__init__(threshold)
        self._set_custom_logger(logger_name, threshold)

    def send_message(self, message: CurriculumBaseMessage, **kwargs):
        self._logger.log(message.level, str(message))

    def _set_custom_logger(self, name: str, level):
        logger = logging.getLogger(name)
        logger.setLevel(level)
        ch = logging.StreamHandler()
        ch.setLevel(level)
        formatter = logging.Formatter("[%(levelname)s] %(message)s")
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.propagate = False
        self._logger = logger
