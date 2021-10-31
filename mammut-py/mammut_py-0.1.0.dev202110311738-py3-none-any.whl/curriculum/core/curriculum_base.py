from mammut.common.storage.storage_manager import StorageManager
from mammut.assessment.assessor import Assessor
from mammut.curriculum.course.course import Course
from mammut.curriculum.report.package_progress_report import PackageProgress
import mammut.curriculum.course.utils as course_utils
from mammut.curriculum.core.flowchart import Flowchart
from mammut.curriculum.lesson import lesson_base
from mammut.curriculum.lesson.lesson_type import LessonType
from mammut.common.package import Package
from typing import List, Optional
import pandas as pd
import mammut.curriculum.report as report
from mammut.curriculum.core.mammut_session_context import MammutSessionContext


class CurriculumBase(object):
    """Encapsulates all the Curriculum learning required tools:
        - Courses, Lessons, Assessments.
        - Package, Dictionary, LinguisticStandard.

    The courses in a Curriculum forms a flowchart, which is
    a directed acyclic graph. The flowchart implies that courses are
    meant to be progressive, which allows to organize them into academic
    periods.
    """

    _storage_manager = StorageManager()

    DEFAULT_START_CELL = "A1"
    DEFAULT_START_COLUMN = "A"
    DEFAULT_START_ROW = "1"
    DEFAULT_END_CELL = "J"

    def __init__(
        self,
        package_id: str,
        standard_spreadsheet_id: str,
        curriculum_base_sheet_title: str = "curriculum",
        lessons_base_sheet_title: str = "lessons",
        assessments_sheet_title: str = "assessments",
        standard_base_sheet_title: str = "base",
        standard_dict_sources_sheet_title: str = "dict-sources",
        standard_pos_sheet_title: str = "pos-tags",
        standard_features_sheet_title: str = "features",
        standard_dimensions_sheet_title: str = "dimensions",
        dictionary_sheet_title: str = "dictionary",
        standard_functionals_sheet_title: str = "functionals",
        standard_non_functionals_sheet_title: str = "non-functionals",
        standard_primes_sheet_title: str = "primes",
        standard_synonym_sheet_title: str = "synonym",
        synonym_sheet_title: str = "synonym",
        progress_sheet_title: str = "progress",
        package_id_is_spreadsheet: bool = False,
        show_progress: bool = True,
        create_progress_sheet: bool = False,
        mammut_session_context: Optional[MammutSessionContext] = None,
        enable_ktt_interpretation: bool = False,
    ):
        self.errors = []
        self.valid = True
        self.curriculum_base_sheet_title: str = curriculum_base_sheet_title
        self.lessons_base_sheet_title: str = lessons_base_sheet_title
        self.assessment_sheet_title: str = assessments_sheet_title
        self.progress_sheet_title: str = progress_sheet_title
        self._create_progress_sheet: bool = create_progress_sheet
        self.package: Package = Package(
            package_id,
            standard_spreadsheet_id,
            package_id_is_spreadsheet,
            show_progress,
            standard_base_sheet_title,
            standard_dict_sources_sheet_title,
            standard_pos_sheet_title,
            standard_features_sheet_title,
            standard_dimensions_sheet_title,
            dictionary_sheet_title,
            standard_functionals_sheet_title,
            standard_non_functionals_sheet_title,
            standard_primes_sheet_title,
            standard_synonym_sheet_title,
            synonym_sheet_title,
        )
        self.package_spreadsheet_id = self.package.spreadsheet_id
        self.courses: List[Course] = []
        self.flowchart: Optional[Flowchart] = None
        self.assessor: Optional[Assessor] = None
        self.base_curriculum_dataframe = None
        self.base_lessons_dataframe = None
        self.progress: Optional[PackageProgress] = None
        self._enable_ktt_interpretation: bool = enable_ktt_interpretation

        # TODO: The session context is created here if doesn't exists,
        #   because right now, the Curriculum is the entrypoint class.
        #   In the future, there'll be another layer to instantiate Curriculum processes.
        #   Sessions should be created there.
        if mammut_session_context:
            self._mammut_session_context = mammut_session_context
        else:
            self._mammut_session_context = MammutSessionContext(
                self.package.main_id,
            )
            report.set_mammut_session_context(self._mammut_session_context)

        super(CurriculumBase, self).__init__()

    def _load_curriculum_spreadsheets(self):
        """Loads information from curriculum sheets.

        Downloads the dataframes for:
            - curriculum spreadsheet
            - lessons spreadsheet
        """
        base_curriculum_dataframe: pd.DataFrame = self._storage_manager.get_spreadsheet_as_dataframe(
            self.package_spreadsheet_id,
            self.curriculum_base_sheet_title,
            self.DEFAULT_START_COLUMN,
            self.DEFAULT_START_ROW,
            self.DEFAULT_END_CELL,
        )
        if base_curriculum_dataframe is None:
            self.valid = False
            message = f"{self.curriculum_base_sheet_title} sheet not found"
            self.errors += message
            report.send_message(report.CurriculumGeneralErrorMessage(message))

        base_lessons_dataframe = self._storage_manager.get_spreadsheet_as_dataframe(
            self.package_spreadsheet_id,
            self.lessons_base_sheet_title,
            lesson_base.Lesson.DEFAULT_START_COLUMN,
            lesson_base.Lesson.DEFAULT_START_ROW,
            lesson_base.Lesson.DEFAULT_END_CELL,
        )
        if base_lessons_dataframe is None:
            self.valid = False
            message = f"{self.lessons_base_sheet_title} sheet not found"
            self.errors += message
            report.send_message(report.CurriculumGeneralErrorMessage(message))

        """
            Validates the lessons type column values for specified courses
        """
        if not all(
            base_lessons_dataframe[lesson_base.Lesson.MODEL_COLUMN].isin(
                LessonType.names()
            )
        ):
            self.valid = False
            message = "Invalid Model(s) specified for Lessons"
            self.errors += message
            report.send_message(report.CurriculumGeneralErrorMessage(message))

        if self.valid:
            self.base_curriculum_dataframe = base_curriculum_dataframe
            self.base_lessons_dataframe = base_lessons_dataframe

            report.send_message(
                report.CurriculumGeneralDebugMessage(
                    "Load Courses from Package."
                )
            )

            for index, row_course in base_curriculum_dataframe.iterrows():
                if not row_course[course_utils.HIDDEN_COLUMN]:
                    course = self._get_course_instance(
                        row_course, base_lessons_dataframe
                    )
                    self.courses.append(course)

    def load(self):
        """Loads the Curriculum and all the Package information.
        """
        report.send_message(
            report.CurriculumGeneralInfoMessage(
                "Load Curriculum Package information",
            )
        )

        self.package.load_main_classes()

        report.send_message(
            report.CurriculumGeneralInfoMessage(
                "Main classes Package, LinguisticStandard, Dictionary loaded"
            )
        )

        """
        Assessor must load before the courses, since the courses
        instances contains a reference to the assessor.
        """
        self.assessor = Assessor(
            self.package_spreadsheet_id, self.assessment_sheet_title
        )

        self.assessor.load()

        report.send_message(
            report.CurriculumGeneralInfoMessage("Curriculum Assessor loaded")
        )

        self.progress = PackageProgress(
            self,
            self._storage_manager,
            self.progress_sheet_title,
            create_sheet=self._create_progress_sheet,
        )

        self._load_curriculum_spreadsheets()
        self.flowchart = Flowchart(self)
        if not self.flowchart.valid or not self.valid:
            self.valid = False
            self.errors += self.flowchart.errors

        if self._enable_ktt_interpretation:
            self.flowchart.add_ktt_interpretation_course(self)

        report.send_message(
            report.CurriculumGeneralInfoMessage(
                "Curriculum courses flowchart loaded"
            )
        )

    def _get_course_instance(
        self, row: pd.Series, lessons_df: pd.DataFrame
    ) -> Course:
        """Returns the concrete instantiation of a course.
        It performs concrete instantiation of lessons too
        that are associated to that course.

        Private method used at initialization time.
        """
        course = Course(
            row[course_utils.ID_COLUMN],
            row[course_utils.ACADEMIC_PERIOD_COLUMN],
            row[course_utils.PREREQUISITE_COLUMN],
            row[course_utils.LANGUAGE_LEVEL_COLUMN],
            row[course_utils.COURSE_NAME_COLUMN],
            row[course_utils.APPROVAL_CRITERIA_COLUMN],
            row[course_utils.RETRY_COLUMN],
            row[course_utils.REGIONAL_SETTINGS_COLUMN],
            Course.get_lessons_for_course(
                row[course_utils.ID_COLUMN],
                lessons_df,
                self.package.corpus_map,
                self._mammut_session_context,
            ),
            self.assessor,
            self._mammut_session_context,
        )
        return course
