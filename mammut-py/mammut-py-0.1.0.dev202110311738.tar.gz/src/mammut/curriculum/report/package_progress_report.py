from mammut.common.storage.storage_manager import StorageManager
import pandas as pd
from mammut.curriculum.course.course import Course
from mammut.assessment.assessment import Assessment
import json


class PackageProgress:
    """This class knows encapsulates the progress report functionality
    for the curriculum package document.

    The class contains a pandas.Dataframe which contains the curriculum
    progress in table form.

    The dataframe progressively appends new rows for each applied
    assessment. This allows to follow the progress over time.
    """

    _columns_names = [
        "course_id",
        "course_name",
        "course_attempt",
        "approved",
        "score",
        "assessment",
        "approved_problems",
        "failed_problems",
        "failed_problems_report",
    ]

    def __init__(
        self,
        curriculum: "Curriculum",
        storage_manager: StorageManager,
        progress_sheet_name: str,
        create_sheet: bool = False,
    ):
        self.progress_sheet_name = progress_sheet_name
        self._storage_manager = storage_manager
        self._curriculum_reference = curriculum
        self._dataframe: pd.DataFrame = None
        self._create_report_dataframe()
        if create_sheet:
            self._write_columns_titles()

    def _create_report_dataframe(self):
        self._dataframe = pd.DataFrame([], columns=self._columns_names)

    def write_progress(self, row):
        self._storage_manager.add_rows_to_spreadsheet(
            self._curriculum_reference.package_spreadsheet_id,
            self.progress_sheet_name,
            row.to_numpy().tolist(),
        )

    def _write_columns_titles(self):
        self._storage_manager.delete_sheet(
            self._curriculum_reference.package_spreadsheet_id,
            self.progress_sheet_name,
        )
        self._storage_manager.create_new_sheet(
            self._curriculum_reference.package_spreadsheet_id,
            self.progress_sheet_name,
        )
        self._storage_manager.update_row_from_spreadsheet(
            self._curriculum_reference.package_spreadsheet_id,
            self.progress_sheet_name,
            self._columns_names,
            "1",
            "A",
        )

    def add_progress_entry(self, course: Course, assessment: Assessment):
        row = pd.DataFrame(
            [
                [
                    str(course.course_id),
                    str(course.course_name),
                    str(course.last_attempt),
                    str(course.approved()),
                    str(course.last_score),
                    str(assessment.assessment_id),
                    "".join(str(assessment.approved_problems_id)),
                    "".join(str(assessment.failed_problems_id)),
                    json.dumps(
                        assessment.failed_problems_info,
                        sort_keys=False,
                        indent=4,
                    ),
                ]
            ],
            columns=self._columns_names,
        )
        self.write_progress(row)
        self._dataframe = self._dataframe.append(row)
