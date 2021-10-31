from mammut.curriculum.report.messages.message import (
    CurriculumBaseMessage,
    CurriculumBaseMessageWithLesson,
)
from mammut.curriculum.report.utils import Component
import logging


class CurriculumGeneralInfoMessage(CurriculumBaseMessage):
    """Generic information message for Curriculum processing.
    """

    def __init__(self, message: str):
        super(CurriculumGeneralInfoMessage, self).__init__(
            component=Component.Curriculum,
            report_level=logging.INFO,
            message=message,
        )


class CurriculumGeneralInfoMessageWithLesson(CurriculumBaseMessageWithLesson):
    def __init__(self, message: str, course: int, lesson: int):
        super(CurriculumGeneralInfoMessageWithLesson, self).__init__(
            component=Component.Curriculum,
            course_id=course,
            lesson_id=lesson,
            report_level=logging.INFO,
            message=message,
        )


class CurriculumGeneralDebugMessage(CurriculumBaseMessage):
    """Generic debugging information message for curriculum processing"""

    def __init__(self, message: str):
        super(CurriculumGeneralDebugMessage, self).__init__(
            component=Component.Curriculum,
            report_level=logging.DEBUG,
            message=message,
        )


class CurriculumGeneralErrorMessage(CurriculumBaseMessage):
    """Generic error message for curriculum processing"""

    def __init__(self, message: str):
        super(CurriculumGeneralErrorMessage, self).__init__(
            component=Component.Curriculum,
            report_level=logging.ERROR,
            message=message,
        )


class CurriculumGeneralWarningMessage(CurriculumBaseMessage):
    """Warning general message from curriculum phase.
    """

    def __init__(self, message: str):
        super(CurriculumGeneralWarningMessage, self).__init__(
            component=Component.Curriculum,
            report_level=logging.WARNING,
            message=message,
        )
