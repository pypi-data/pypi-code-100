from mammut.curriculum.report.reporters.base_reporter import BaseReporter
from mammut.curriculum.report.reporters.console_reporter import ConsoleReporter
from mammut.curriculum.report.messages.message import CurriculumBaseMessage
from typing import List
import logging

log = logging.getLogger(__name__)


class ClientReporter(BaseReporter):
    """Reporter class to support client reporting calls.

    The client reporter can hold arbitrary custom reporters
    to replicate message report.

    This client can enable module logging to also publish messages
    in the conventional way.

    This reporter can enable caching. When caching is enabled, the messages
    will be saved in an ordered sequence.

    TODO: constructor parameters must be replaced by configuration values.
    """

    def __init__(
        self,
        threshold=logging.INFO,
        enable_module_logging: bool = False,
        enable_caching: bool = False,
    ):
        """
        Args:
            threshold: threshold level for this reporter.
            enable_caching (bool): enable the conventional module logger replication
                of messages
            enable_caching (bool): enable store of messages in this reporter state.
        """
        super(ClientReporter, self).__init__(threshold)
        self._reporters: List[BaseReporter] = []
        self._module_logging_enable: bool = enable_module_logging
        self._cache: List[
            CurriculumBaseMessage
        ] = [] if enable_caching else None
        self._add_reporter(
            ConsoleReporter(
                "client_console_reporter", threshold=self.threshold
            )
        )
        log.debug("Client reported configured")

    def _add_reporter(self, reporter: BaseReporter):
        if reporter not in self._reporters:
            self._reporters.append(reporter)

    def send_message(self, message: CurriculumBaseMessage, **kwargs):
        """Replicates the message report to all custom reporters.

        :Args:
            message: message to be reported.
        """
        if self._module_logging_enable:
            log.log(message.level, str(message))

        if self._cache:
            self._cache.append(message)

        for reporter in self._reporters:
            reporter.send_message(message)
