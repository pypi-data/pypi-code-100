from abc import ABC, abstractmethod
from mammut.curriculum.course.course_state import CourseState
from mammut.curriculum.course.course import Course
from mammut.curriculum.core.curriculum_base import CurriculumBase
from mammut.curriculum.core.mammut_session_context import MammutSessionContext
import uuid

from typing import Dict, Set


class Classroom(ABC):
    """
    A classroom is a workspace where courses are processed.
    The classroom contains all the facilities
    required by a course to be processed.

    Contains a curriculum registry that can be used by the
    courses in the workspace.

    By having a curriculum, transitively has access to a
    Package data and a Linguistic Standard.
    """

    def __init__(self, mammut_session_context: MammutSessionContext):
        """
        Args:
            mammut_session_context: The session context for this classroom and the
                curriculums in it.
        """
        self._id = uuid.uuid4()
        self._curriculums: Dict[str, "Curriculum"] = {}
        """
        Last set of processed courses in this Classroom.
        """
        self._last_courses: Set[Course] = set()
        self._mammut_session_context = mammut_session_context

    def id(self):
        return self._id

    def add_curriculum(
        self,
        package_id: str = None,
        standard_spreadsheet_id: str = None,
        curriculum_reference: "Curriculum" = None,
        enable_ktt_interpretation: bool = False,
        package_id_is_spreadsheet: bool = False
    ):
        """
        Adds a new curriculum facility to this classroom.

        If no curriculum_reference is given, the curriculum is instantiated.
        """
        if curriculum_reference is not None:
            self._curriculums[
                curriculum_reference.package.main_id
            ] = curriculum_reference
        else:
            curriculum = CurriculumBase(
                package_id,
                standard_spreadsheet_id,
                package_id_is_spreadsheet=package_id_is_spreadsheet,
                show_progress=False,
                create_progress_sheet=False,
                mammut_session_context=self._mammut_session_context,
                enable_ktt_interpretation=enable_ktt_interpretation
            )
            curriculum.load()
            self._curriculums[package_id] = curriculum

    def get_last_courses_record(self) -> Set[CourseState]:
        """Return the last set of processed courses.

        By requesting last processed courses record, client
        control classes can fetch the latest data state of
        courses processed in this classroom.

        Returns:
            Set of course Records.
        """
        records = set(
            map(lambda course: course.get_course_record(), self._last_courses)
        )
        return records

    @abstractmethod
    def initialize(self):
        """
        initialize resources for a particular classroom type.
        """
        pass

    @abstractmethod
    def take_courses(
        self, courses_ids: Set[int], curriculum_spreadsheet_id: str
    ) -> None:
        """
        Process the desired courses in this classroom.

        This method does not return anything to client control classes,
        is intended to side effect the processing of courses.

        Args:
            courses_ids(Set[int]): list of courses ids to process.
            curriculum_spreadsheet_id: spreadsheet id of the curriculum
                where courses belong.

        Returns:
            A set of course records encapsulating the state of
            processed courses.
        """
        pass

    @abstractmethod
    def stop(self):
        """
        Request gracefully stopping of this classroom execution process.
        """
        pass
