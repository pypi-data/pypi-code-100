from mammut.curriculum.report.messages.message import CurriculumBaseMessage
from mammut.curriculum.report.messages.curriculum_messages import *
from typing import List
import ray
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


@ray.remote
class RayReportersRegistry:
    """The RayReporterRegistry actor is used in remote workers as the actor
    handle to centralize all the remote produced messages.

    The main curriculum then can request messages in a single place
    and report them where the user "is".
    """

    def __init__(self):
        self._cached_messages: List[CurriculumBaseMessage] = []
        self._last_index_retrieved: int = 0

    def get_messages(self):
        """Returns the new messages arrived since the last
        call to this method.
        """
        messages = self._cached_messages[
            self._last_index_retrieved : len(self._cached_messages)
        ]
        self._last_index_retrieved = len(self._cached_messages)
        log.debug(f"Retrieve {len(messages)} new messages")
        return messages

    def save_message(self, message: CurriculumBaseMessage):
        """Adds a new message to the report registry.
        """
        self._cached_messages.append(message)

    def save_ktt_plain_message(self, message: str, level: str):
        """Receives a plain string message and the plain
        report string level.
        Internally, the string message will be reported as some
        curriculum message type.
        Note: This method is used for allowing mammut-ktt to publish
        messages in the report registry without dealing with serialization
        code of more complex classes like messages.
        Args:
            message: the plain string message
            level: the report level plain string.
        Returns
            Returns an int, without especial meaning. Just to handshake the
            Java call in the mammut-ktt client code.
        """
        log_level = logging.getLevelName(level)
        if log_level == logging.DEBUG:
            report_message = CurriculumGeneralDebugMessage(message)
        elif log_level == logging.INFO:
            report_message = CurriculumGeneralInfoMessage(message)
        elif log_level == logging.ERROR:
            report_message = CurriculumGeneralErrorMessage(message)
        elif log_level == logging.WARNING:
            report_message = CurriculumGeneralWarningMessage(message)
        else:
            report_message = CurriculumGeneralInfoMessage(message)
        self._cached_messages.append(report_message)
        log.debug("received KtT plain message")
        return 0

    def get_all_messages(self):
        """Returns all the messages arrived since this process
        started.
        """
        return self._cached_messages
