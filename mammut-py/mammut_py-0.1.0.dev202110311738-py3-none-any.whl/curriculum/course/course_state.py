from abc import ABC
from typing import List
from mammut.curriculum.core.utils import LanguageLevel
from mammut.curriculum.core.mammut_session_context import MammutSessionContext
import dataclasses


@dataclasses.dataclass
class CourseState(ABC):
    """Data class for courses.

    It contains all the relevant state for the course, without extra processing logic.

    A course is approved if the total sum of weights for the approved
    problems surpasses or equals the approval_criteria.

    If a course can't be approved, it will be reprocessed in the next
    academic period. If for some reason a course can't never be approved,
    the retries_count for the course will avoid an infinite loop of an academic period.

    Args:
        course_id(int): 'id' value in datasource retrieved data.
        academic_period(int): 'academic_period' value in datasource retrieved data.
        prerequisites(List[int]): 'prerequisites' value in datasource retrieved data.
        language_level: 'language_level' value in datasource retrieved data.
        course_name(str): 'course_name' value in datasource retrieved data.
        approval_criteria(float): approval normalized criteria for this course.
        retry(int): 'retry' string value to indicate how many times a course can be processed before
            stopping the curriculum.
        retries_count(int)
        regional_settings(str): 'regional_settings' value in datasource retrieved data.
        last_score(float): last registered score for this course.
        perfect_score(float): the perfect score of the course if all problems are passed.
        mammut_session_context: The curriculum session context where this course instance exists.
    """

    course_id: int
    academic_period: int
    prerequisites: List[int]
    language_level: LanguageLevel
    course_name: str
    _approval_criteria: float
    _retry_value: int
    _retries_count: int
    regional_settings: str
    _last_score: float
    _perfect_score: float
    mammut_session_context: MammutSessionContext

    def __hash__(self):
        return self.course_id

    def __eq__(self, other):
        return (
            isinstance(other, CourseState)
            and self.course_id == other.course_id
        )
