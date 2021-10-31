from abc import ABC
from mammut.curriculum.report.utils import Component
from mammut.curriculum.core.mammut_session_context import MammutSessionContext


class CurriculumBaseMessage(ABC):
    """Generic message to report in the curriculum core components.
    """

    def __init__(
        self, component: Component, message: str, report_level,
    ):
        """
        Args:
            component: Which curriculum component reports the message.
            message: message text.
            mammut_session_context: context with the curriculum session data.
            report_level: message report level.
        """
        self.component: component = component
        self.level = report_level
        self.message = message
        self.package_id = None
        self.session_id = None
        self.mammut_id = None

    def set_context(self, mammut_session_context: MammutSessionContext):
        self.package_id = mammut_session_context.package_id
        self.session_id = mammut_session_context.session_id
        self.mammut_id = mammut_session_context.mammut_id

    def __str__(self):
        f_str = f"Session:{self.session_id} - Mammut:{self.mammut_id} - Package: {self.package_id} - {self.message}"
        return f_str


class CurriculumBaseMessageWithCourse(CurriculumBaseMessage):
    """Generic message to report in the curriculum components where
    course ID is relevant.
    """

    def __init__(
        self, component: Component, course_id, message: str, report_level,
    ):
        super(CurriculumBaseMessageWithCourse, self).__init__(
            component, message, report_level
        )
        self.course_id = course_id

    def __str__(self):
        f_str = f"Session:{self.session_id} - Mammut:{self.mammut_id} - Package:{self.package_id} - Course:{self.course_id} - {self.message}"
        return f_str


class CurriculumBaseMessageWithLesson(CurriculumBaseMessageWithCourse):
    """Generic message to report in the curriculum components where
    lesson ID is relevant.
    """

    def __init__(
        self,
        component: Component,
        course_id,
        lesson_id,
        message: str,
        report_level,
    ):
        super(CurriculumBaseMessageWithLesson, self).__init__(
            component, course_id, message, report_level
        )
        self.lesson_id = lesson_id

    def __str__(self):
        f_str = f"Session:{self.session_id} - Mammut:{self.mammut_id} - Package:{self.package_id} - Course:{self.course_id} - Lesson:{self.lesson_id} - {self.message}"
        return f_str
