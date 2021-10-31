# coding=utf-8

from typing import Optional, List

import mammut.assessment.util
from mammut.common.storage.storage_manager import StorageManager
import pandas as pd
import logging
from mammut.assessment.assessment import Assessment, Problem
from mammut.assessment.problem_type_enum import ProblemType
import mammut.assessment.util as assessment_utils
from typing import Dict

log = logging.getLogger(__name__)


class Assessor:
    """Class to handle assessments and hide complexity
    from clients.

    It contains the in-memory dataframe of assessments.
    And provide a public API for lazy concrete instantiation to
    client classes.
    """

    _storage_manager = StorageManager()

    def __init__(self, package_spreadsheet_id: str, spreadsheet_name):
        self.errors: List[str] = []
        self.valid: bool = True
        self.spreadsheet_id = package_spreadsheet_id
        self.spreadsheet_name = spreadsheet_name
        self._dataframe: pd.DataFrame = Optional[None]
        """
            Initializes the Problems registry for concrete instantiation of
            problems at runtime.
        """
        self._problems_registry = {}
        self._load_problem_registry()

    def load(self):
        base_dataframe = self._storage_manager.get_spreadsheet_as_dataframe(
            self.spreadsheet_id,
            self.spreadsheet_name,
            mammut.assessment.util.DEFAULT_START_COLUMN,
            mammut.assessment.util.DEFAULT_START_ROW,
            mammut.assessment.util.DEFAULT_END_CELL,
        )
        self._dataframe = base_dataframe

        """
           Validates the problems types values for the specified assessments
        """
        if not all(
            base_dataframe[mammut.assessment.util.PROBLEM_TYPE_COLUMN].isin(
                ProblemType.names()
            )
        ):
            self.valid = False
            self.errors += (
                "Invalid Problem(s) type specified in assessments sheet."
            )

    def get_course_max_score(self, course_id) -> float:
        """Returns the sum of all the problems assigned to the Course.
        """
        partial_df: pd.DataFrame = self._dataframe.loc[
            self._dataframe[mammut.assessment.util.COURSE_ID_COLUMN]
            == str(course_id)
        ]
        total_score = sum(
            map(
                lambda w: float(w),
                partial_df[mammut.assessment.util.WEIGHT_COLUMN].array,
            )
        )
        return total_score

    def get_scheduled_assessment(
        self, course_id, schedule
    ) -> Optional[Assessment]:
        """Returns an assessments for a schedule in a course.

        Args:
            course_id(int): course identifier.
            schedule(int): assessment schedule, indicates after which lesson
                should the assessment be evaluated.
            model: Models enum value required for concrete instantiation.

        Returns:
            The Assessment for the given schedule.
        """

        """
            Get only the partial dataframe for the course and lesson schedule.
        """
        partial_df: pd.DataFrame = self._dataframe.loc[
            (
                self._dataframe[mammut.assessment.util.COURSE_ID_COLUMN]
                == str(course_id)
            )
            & (
                self._dataframe[mammut.assessment.util.SCHEDULE_COLUMN]
                == str(schedule)
            )
        ]

        """
            Scheduled assessments are optionals.
        """
        if partial_df.empty:
            return None

        """
            Get the ID of the current assessment.
        """
        assessment_id = partial_df[
            mammut.assessment.util.ASSESSMENT_ID_COLUMN
        ].iloc[0]
        """
            For the assessment get the problem rows, and pass those problems
            to Assessment class constructor. 
        """
        problems = []
        for index, problem_row in partial_df.iterrows():
            problem_type_value = problem_row[
                mammut.assessment.util.PROBLEM_TYPE_COLUMN
            ]
            """
                Get the custom class from the internal problems dictionary, and 
                instantiate an object of that class.
            """
            problem: Problem = self._problems_registry[problem_type_value](
                problem_row[mammut.assessment.util.COURSE_ID_COLUMN],
                problem_row[mammut.assessment.util.ASSESSMENT_ID_COLUMN],
                problem_row[mammut.assessment.util.SCHEDULE_COLUMN],
                problem_row[mammut.assessment.util.PROBLEM_ID_COLUMN],
                problem_row[mammut.assessment.util.PROBLEM_TYPE_COLUMN],
                problem_row[mammut.assessment.util.PARAMETERS_COLUMN],
                problem_row[mammut.assessment.util.LANGUAGE_COMPETENCE_COLUMN],
                problem_row[mammut.assessment.util.WEIGHT_COLUMN],
                problem_row[mammut.assessment.util.RETRY_COLUMN],
                problem_row[mammut.assessment.util.OBSERVATIONS_COLUMN],
            )
            problems.append(problem)

        assessment: Assessment = Assessment(assessment_id, problems, course_id)
        return assessment

    def _load_problem_registry(self):
        """Loads the problems type internal dictionary used in
        concrete instantiation operations.

        The dictionary keys are strings for the problem type, and the
        values are problems custom classes.
        """
        for problem_type in ProblemType.list():
            self._problems_registry[problem_type[0]] = problem_type[1]
