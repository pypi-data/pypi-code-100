from mammut.curriculum.report.errors.base_error import BaseError
from mammut.curriculum.report.utils import Phase
from json import JSONDecodeError


class JSONLessonParsingError(BaseError):
    def __init__(
        self,
        exception: JSONDecodeError,
        phase: Phase,
        course: str,
        lesson: str,
        column: str,
    ):
        BaseError.__init__(self, "Error parsing JSON string for Lesson", phase)
        self.course: str = course
        self.lesson: str = lesson
        self.column: str = column
        self.exception = exception

    def __str__(self):
        s = (
            f"{self.message}, "
            f"Phase: {self.phase}, "
            f"Course: {self.course}, "
            f"Lesson: {self.lesson}, "
            f"Column value: {self.column}"
        )
        return s


class JSONProblemParsingError(BaseError):
    def __init__(
        self,
        exception: JSONDecodeError,
        phase: Phase,
        course_id: str,
        assessment_id: str,
        problem_id: str,
        column_value: str,
    ):
        BaseError.__init__(
            self, f"Error parsing JSON string for Problem", phase
        )
        self.phase = phase
        self.course = course_id
        self.assessment = assessment_id
        self.problem = problem_id
        self.column = column_value
        self.exception = exception

    def __str__(self):
        s = (
            f"{self.message}, "
            f"Phase: {self.phase}, "
            f"Course: {self.course}, "
            f"Assessment: {self.assessment}, "
            f"Problem:{self.problem}, "
            f"Column: {self.column}"
        )
        return s


class ModelRequiredParameterMissingKey(BaseError):
    def __init__(self, missing_key: str, course_id, lesson_id):
        BaseError.__init__(
            self, f'"Missing key {missing_key} in lesson {lesson_id} from course {course_id}"', Phase.LECTURE_LESSON
        )

        self.course_id = course_id
        self.lesson_id = lesson_id

    def __str__(self):
        return self.message
