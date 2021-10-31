from mammut.curriculum.lesson import lesson_type
import mammut.curriculum.core.utils as curriculum_utils
from mammut.curriculum.lesson import lesson_base
from mammut.curriculum.lesson.online_lessons import KttInterpretationLesson
from mammut.assessment.assessor import Assessor, Assessment
from typing import List, Optional
import pandas as pd
from mammut.common.corpus.corpus_map import CorpusMap
from mammut.curriculum.course.course_state import CourseState
from mammut.curriculum.core.mammut_session_context import MammutSessionContext
import mammut.curriculum.report as report


class Course(CourseState):
    """This class encapsulates the concept of a course in the curriculum.

    A course is composed essentially by a ordered list of lessons.
    Each Lesson has a set of scheduled assessments, composed of problems.
    Problems encapsulate a weight, which is used to compute the
    course score for approval/disapproval.

    The computation role of the course involves:
    - Prepare a lesson resources: input data, model.
    - Practice a Lesson to train the model.
    - After a Lesson is finished, ask for scheduled assessments
        to that lesson.
    - Apply scheduled assessments for that finished lesson.
    - Repeat for each lesson.
    """

    """
    Registry for lessons type. This internal registry allows to 
    instantiate concrete lessons type using a dictionary key lookup.
    """
    _lessons_registry = {}

    """
    Loads the lessons type internal dictionary used for
    concrete instantiation of lessons.

    The dictionary keys are enumeration names for the problem type, 
    and the values are problems custom classes.
    """
    for enum_type in lesson_type.LessonType.list():
        _lessons_registry[enum_type[0]] = enum_type[1]

    def __init__(
        self,
        course_id: str,
        academic_period: str,
        prerequisites: str,
        language_level: str,
        course_name: str,
        approval_criteria: str,
        retry: str,
        regional_settings: str,
        lessons: List[lesson_base.Lesson],
        assessor: Assessor,
        mammut_session_context: MammutSessionContext,
    ):
        """
        Note: some arguments are received as string values from storage manager retrieved
        dataset.

        Args:
            course_id(str): 'id' value in datasource retrieved data.
            academic_period(str): 'academic_period' value in datasource retrieved data.
            prerequisites(str): 'prerequisites' value in datasource retrieved data.
            language_level(str): 'language_level' value in datasource retrieved data.
            course_name(str): 'course_name' value in datasource retrieved data.
            retry(str): 'retry' string value to indicate how many times a course can be processed before
                stopping the curriculum.
            regional_settings(str): 'regional_settings' value in datasource retrieved data.
            lessons: Lessons for this course
            assessor: assessor reference for course assessment operations
            mammut_session_context: The session context from the classroom.
        """

        # Splits comma separated list of prerequisites for a course.
        prerequisites_list: List[int] = (
            []
            if not prerequisites
            else [
                int(prerequisite.strip())
                for prerequisite in prerequisites.split(",")
            ]
        )

        language_level: curriculum_utils.LanguageLevel = curriculum_utils.LanguageLevel.from_str(
            language_level
        )

        """
        Lessons list for the course.
        """
        self.lessons: List[lesson_base.Lesson] = lessons

        """
        Assessor reference should be assigned by the subclass.
        """
        self.assessor: Assessor = assessor

        perfect_score = self.assessor.get_course_max_score(int(course_id))

        self.course_id = int(course_id)
        self.academic_period = int(academic_period)
        self.prerequisites = prerequisites_list
        self.language_level = language_level
        self.course_name = course_name
        self._approval_criteria = float(approval_criteria)
        self._retry_value = int(retry)
        self._retries_count = 0
        self.regional_settings = regional_settings
        self._last_score = 0.0
        self._perfect_score = perfect_score
        self._mammut_session_context = mammut_session_context

    @property
    def last_attempt(self) -> int:
        """Returns the current number of processed attempts for the course"""
        return self._retries_count

    @property
    def last_score(self) -> float:
        return self._last_score

    def is_allowed(self) -> bool:
        """Returns true if the course is allowed for processing.

        A course might not be allowed for processing if:
            - Number of retries has been reached.

        More conditions can be added in the future.
        """
        retry_allowed = self._retries_count <= self._retry_value
        return retry_allowed

    def start(
        self,
        progress_writer: "Progress",
        mammut_session_context: MammutSessionContext,
    ):
        """Start processing internal lessons in this course.

        Lessons are an ordered list. They are executed one after other.
        Restart _last_score for a new "start" called.

        Args:
            progress_writer: object to write progress in the package document.
            mammut_session_context: session context information for report.
        """
        self._last_score = 0.0
        self._retries_count += 1
        for le in self.lessons:
            """
            Lectures all the prepared knowledge for the lesson.
            """
            report.send_message(
                report.CurriculumGeneralInfoMessageWithLesson(
                    "Lesson lecturing", self.course_id, le.lesson_id
                )
            )
            le.lecture()

            """
            After the lesson has been prepared, it can be practiced.
            """
            report.send_message(
                report.CurriculumGeneralInfoMessageWithLesson(
                    "Lesson practice", self.course_id, le.lesson_id
                ),
            )
            le.practice(mammut_session_context)

            """
            Request scheduled assessment for practiced lesson
            Apply assessment to practiced lesson, and 
            adds the approved points to the _last_score
            """
            scheduled_assessment = self._request_assessments(le.order)
            if scheduled_assessment is not None:
                self._last_score += scheduled_assessment.apply(le)
                progress_writer.add_progress_entry(self, scheduled_assessment)

    def approved(self) -> bool:
        """Returns true if the Course has been approved.

        The course is approved if all the applied assessments
        were approved.
        """
        return (
            self._last_score / self._perfect_score
        ) >= self._approval_criteria

    def _request_assessments(
        self, finished_lesson_order: int
    ) -> Optional[Assessment]:
        """Returns a list of scheduled assessments for the finished lesson.
        """
        return self.assessor.get_scheduled_assessment(
            self.course_id, finished_lesson_order
        )

    @staticmethod
    def get_lessons_for_course(
        course_id: str,
        lessons_df: pd.DataFrame,
        corpus_map: CorpusMap,
        mammut_session_context: MammutSessionContext,
    ) -> List[lesson_base.Lesson]:
        lessons: List[lesson_base.Lesson] = []
        for index, row_lesson in lessons_df.loc[
            lessons_df[lesson_base.Lesson.COURSE_COLUMN] == course_id
        ].iterrows():
            """
            Creates the Lesson based on the returned class
            reference 
            """
            lesson = Course._lessons_registry[
                row_lesson[lesson_base.Lesson.MODEL_COLUMN]
            ](
                row_lesson[lesson_base.Lesson.ID_COLUMN],
                row_lesson[lesson_base.Lesson.COURSE_COLUMN],
                row_lesson[lesson_base.Lesson.ORDER_COLUMN],
                row_lesson[lesson_base.Lesson.CORPUS_ID_COLUMN],
                corpus_map,
                row_lesson[lesson_base.Lesson.NAME_COLUMN],
                row_lesson[lesson_base.Lesson.LANGUAGE_COMPETENCE_COLUMN],
                row_lesson[lesson_base.Lesson.PARAMETERS_COLUMN],
                mammut_session_context,
            )
            lessons.append(lesson)

        lessons.sort(key=lambda x: x.order)
        return lessons

    def __hash__(self):
        return self.course_id

    def __eq__(self, other):
        return (
            isinstance(other, CourseState)
            and self.course_id == other.course_id
        )

    def get_course_record(self) -> CourseState:
        return CourseState(
            self.course_id,
            self.academic_period,
            self.prerequisites,
            self.language_level,
            self.course_name,
            self._approval_criteria,
            self._retry_value,
            self._retries_count,
            self.regional_settings,
            self._last_score,
            self._perfect_score,
            self._mammut_session_context,
        )

    def fetch_course_state(self, record: CourseState):
        """Updates the course state to the received course state.

        It will keep the greater retries count.
        """
        if not self.course_id == record.course_id:
            raise ValueError(
                "Can't updated a course state with different course_id"
            )

        if record._retries_count > self._retries_count:
            self._retries_count = record._retries_count
        self._last_score = record._last_score


class KttPackageInterpretationCourse(Course):
    """This course is the responsible for handling the Package interpretation
    process.

    The package compilation process is a pre-requisite to all courses,
    so if enabled, it's executed in the academic period "0".

    KtT transducer will perform the interpretation and store the data in the
    long term working memory.

    Todo: Evaluation and assessment process for this course
        isn't defined yet.

    Todo: synchronization between classroom and remote java process
        isn't implemented yet. Some wait should be useful.

    Todo: Language level isn't defined yet for this course. Using
        `SemanticPragmatic` as some value.

    Todo: Remember to implement the mammut-id retrieval when mammut
        entity provider generalization are implemented.
        (https://github.com/mammut-io/mammut-py/issues/150)
    """

    def __init__(
        self, mammut_session_context: MammutSessionContext, assessor: Assessor
    ):
        super(KttPackageInterpretationCourse, self).__init__(
            course_id="0",
            academic_period="0",
            prerequisites="",
            language_level="SemanticPragmatic",
            course_name="KtT package interpretation",
            approval_criteria="1.0",
            retry="1",
            regional_settings="en",
            lessons=[],
            assessor=assessor,
            mammut_session_context=mammut_session_context,
        )

        self._perfect_score = 1.0

        ktt_interpretation_lesson = KttInterpretationLesson(
            lesson_id=KttInterpretationLesson.RESERVED_LESSON_ID,
            course=f'{self.course_id}',
            order="1",
            corpus_id="0",
            name=self.course_name,
            language_competence="WordIdentification",
            parameters="{}",
            mammut_session_context=mammut_session_context,
        )

        self.lessons.append(ktt_interpretation_lesson)

    def start(
        self,
        progress_writer: "Progress",
        mammut_session_context: MammutSessionContext,
    ):
        super(KttPackageInterpretationCourse, self).start(
            progress_writer, mammut_session_context
        )
        # This course is approved after package compilation has been performed.
        self._last_score = self._perfect_score
