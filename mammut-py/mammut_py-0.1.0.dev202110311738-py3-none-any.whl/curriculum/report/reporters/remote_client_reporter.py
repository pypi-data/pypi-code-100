from mammut.curriculum.report.reporters.base_reporter import BaseReporter
from mammut.curriculum.report.messages.message import CurriculumBaseMessage
from mammut.curriculum.report.reporters.console_reporter import ConsoleReporter
import logging
from typing import List

log = logging.getLogger(__name__)


class RemoteClientReporter(BaseReporter):
    """Reporter class to support client messages reporting
    in remote classrooms.

    The client can enable module logging to also publish
    messages in the conventional way.

    This remote client reporter holds an actor handle
    for a ray actor where the messages are centralized.

    TODO: constructor parameters should be replaced by
        configuration entries.
    """

    def __init__(
        self, threshold=logging.INFO, enable_module_logging: bool = False,
    ):
        """
        Args:
            threshold: threshold level for this reporter.
            enable_module_logging (bool): enable store of messages in this reporter state.
        """
        super(RemoteClientReporter, self).__init__(threshold)
        self._module_logging_enable: bool = enable_module_logging
        self._reporters: List[BaseReporter] = []
        self._reporters.append(
            ConsoleReporter("client_console_remote_reporter", self.threshold)
        )
        log.debug("Remote client reporter configured")

    def send_message(self, message: CurriculumBaseMessage, **kwargs):
        """Send the message to the remote actor handle.

        Args:
            message: Message to be sent to the remote actor handle.
            **main_report_handle: the handle of the main reporter in the main
                process.
        """
        main_report_handle = kwargs["main_report_handle"]

        if self._module_logging_enable:
            log.log(message.level, str(message))

        main_report_handle.save_message.remote(message)

        for reporter in self._reporters:
            reporter.send_message(message)
