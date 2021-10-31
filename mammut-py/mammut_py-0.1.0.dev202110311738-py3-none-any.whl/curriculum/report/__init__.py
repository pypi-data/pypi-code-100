"""Message reporting package to be used across the curriculum system.

The package will export functions to simply start using the report functionality
right away, by just importing the package. For client classes, is as simple as:

    import mammut.curriculum.report as report
    report.send_message(Message("Hello"))


"""
from .reporters.client_reporter import ClientReporter
from .reporters.remote_client_reporter import RemoteClientReporter
from .reporters.ray_reporter_registry import RayReportersRegistry
from .reporters.console_reporter import ConsoleReporter
from .messages.curriculum_messages import *
from mammut.curriculum.core.mammut_session_context import MammutSessionContext
from mammut.config import settings
from typing import Optional
import logging

log = logging.getLogger(__name__)

__all__ = [
    "send_message",
    "RayReportersRegistry",
]

# Initializes the main client reporter and the remote client reporter.
# TODO: this classes must initialize from configuration values.
#   right now they are taking default hardcoded values in the class definition.

_main_reporter: ClientReporter = ClientReporter(
    threshold=logging.getLevelName(settings.curriculum.report_level)
)
_remote_reporter: RemoteClientReporter = RemoteClientReporter(
    threshold=logging.getLevelName(settings.curriculum.report_level)
)

# enable remote report. If this flag is true, all messages will be sent to a common registry actor handle.
_enable_remote: bool = False
_mammut_session_context: Optional[MammutSessionContext] = None


def send_message(message: CurriculumBaseMessage):
    """Sends a message to all the configured reporters.

    If remote report is enabled, reporter_registry_actor_handle is expected.

    Args:
        message: Message to be sent.
    """
    global _enable_remote
    global _main_reporter
    global _remote_reporter
    global _mammut_session_context

    message.set_context(_mammut_session_context)

    if _enable_remote:
        if (
            not _mammut_session_context
            or not _mammut_session_context.main_report_actor_handle
        ):
            log.error(
                "Trying to report remote message, but no registry actor handle found report context."
            )
            return

        _remote_reporter.send_message(
            message,
            **{
                "main_report_handle": _mammut_session_context.main_report_actor_handle
            },
        )

    else:
        _main_reporter.send_message(message)


def set_mammut_session_context(mammut_session_context: MammutSessionContext):
    """Set the session context for the messages reported in the
    python process.

    The MammutSessionContext contains the remote reporting actor handle
    for remote classrooms produced messages.

    Args:
        mammut_session_context:  mammut session context with the
            remote report actor handle.
    """
    global _mammut_session_context
    _mammut_session_context = mammut_session_context


def enable_remote():
    """Enable remote reporting in the classroom python process.
    """
    global _enable_remote
    _enable_remote = True
