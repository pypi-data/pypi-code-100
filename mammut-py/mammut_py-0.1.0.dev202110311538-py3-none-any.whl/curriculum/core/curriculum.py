# coding=utf-8
from typing import List, Optional, Set
from mammut.curriculum.core.curriculum_base import CurriculumBase
from mammut.curriculum.classroom.single_classroom import SingleClassroom
from mammut.curriculum.course.course import Course
from mammut.curriculum.core.curriculum_state_machine import (
    CurriculumStateMachineMixin,
)
import mammut.curriculum.report as report


class Curriculum(CurriculumBase, CurriculumStateMachineMixin):
    """Models the Curriculum learning functionality in a single classroom
    environment.

    A Curriculum is composed of a set of courses.
    Each course attempts to train language competences that belongs
    to a language level (https://doc.mammut.io/docs_es/framework/language_arquitecture/).

    The courses in a Curriculum forms a flowchart, which is
    a directed acyclic graph. The flowchart implies that courses are
    meant to be progressive, which allows to organize them into academic
    periods.

    Courses belonging to the same academic period, can be processed
    concurrently.

    This single curriculum doesn't support KtT interpretation.
    """

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
    ):
        super(Curriculum, self).__init__(
            package_id,
            standard_spreadsheet_id,
            curriculum_base_sheet_title,
            lessons_base_sheet_title,
            assessments_sheet_title,
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
            progress_sheet_title,
            package_id_is_spreadsheet,
            show_progress,
            enable_ktt_interpretation=False,
        )
        self._next_academic_period_courses: Optional[Set[Course]] = None
        self.classroom: SingleClassroom = None
        """
            Attribute flag to indicate auto transition
            after first academic period has been executed.
        """
        self._started: bool = False

    def _compute_next_academic_period(self):
        """Select the set of courses for the next academic period.
        """
        courses = list(self.flowchart.graph.nodes)
        approved_courses: List[Course] = []
        unapproved_courses: List[Course] = []

        """
            Courses that are already approved don't count. 
        """
        for c in courses:
            if not c.approved():
                unapproved_courses.append(c)
            else:
                approved_courses.append(c)

        """
            All courses approved.
        """
        if not unapproved_courses:
            report.send_message(
                report.CurriculumGeneralInfoMessage(
                    "All courses has been approved. Curriculum Completed."
                )
            )
            self._next_academic_period_courses = []
            self.trigger(self.CURRICULUM_COMPLETED_TRIGGER)
            return

        """
            Computes the next academic period based on 
            the minimum academic period course(s) that haven't be approved. 
            Only courses with the same academic period can be concurrently processed.
        """
        min_academic_period_course = min(
            unapproved_courses, key=lambda course: course.academic_period
        )

        """
            Assign the unapproved courses from the lowest academic period 
        """
        self._next_academic_period_courses = [
            c
            for c in unapproved_courses
            if c.academic_period == min_academic_period_course.academic_period
        ]

        """
            At this point, it is possible to decide if the curriculum 
            failed. If at least one course from the next academic period
            is not allowed, the curriculum failed. 
        """
        if any(
            list(
                map(
                    lambda course: not course.is_allowed(),
                    self._next_academic_period_courses,
                )
            )
        ):
            report.send_message(
                report.CurriculumGeneralWarningMessage(
                    "Curriculum process failed. Maximum retries reached for course."
                )
            )
            self.trigger(self.FAIL_COURSE_TRIGGER)
            return

        """
            At this point, it's safe to make the transition to the 
            next academic period processing cycle. 
        """
        report.send_message(
            report.CurriculumGeneralInfoMessage(
                f"New academic period. [{min_academic_period_course.academic_period}] academic period "
                f"with [{len(self._next_academic_period_courses)}] assigned courses"
            ),
        )
        if self._started:
            self.trigger(self.BEGIN_COURSES_TRIGGER)

    def _all_courses_completed(self) -> bool:
        """Returns False if there's at least one unapproved.
        """
        return len(self._next_academic_period_courses) == 0

    def _take_courses(self):
        """This is a wrapper function for course executor
        take_courses method.

        It is configured to be invoked when the curriculum
        makes the transition to ASSIGNED_STATE.
        """
        self.classroom.take_courses(
            set(
                map(lambda c: c.course_id, self._next_academic_period_courses)
            ),
            self.package.main_id,
        )

    def _academic_period_finished_callback(self):
        """Callback to update the state when an academic period
        has been finished.

        In this case when the academic period is finished,
        the curriculum will request for the course reports to
        the classroom.

        At first glance, this might be redundant, but this pattern
        is expected to be replicated for the multi-classroom execution mode.
        """

        report.send_message(
            report.CurriculumGeneralDebugMessage(
                "Curriculum academic period finished callback called."
            )
        )

        academic_period_records = self.classroom.get_last_courses_record()

        records_ids = set(map(lambda c: c.course_id, academic_period_records))

        courses = set(
            [
                course
                for course in self.courses
                if course.course_id in records_ids
            ]
        )

        courses_dict = {course.course_id: course for course in courses}

        for course_record in academic_period_records:

            report.send_message(
                report.CurriculumGeneralDebugMessage(
                    f"Update course state for course {course_record.course_id}"
                )
            )

            courses_dict[course_record.course_id].fetch_course_state(
                course_record
            )

        self.trigger(self.ASSIGNED_COURSES_COMPLETED_TRIGGER)

    def _curriculum_process_stop_callback(self):
        """Callback to update the state when an academic period
        has been stopped.

        It allows to change state from associated classes.

        In this case, the classroom stopped the processing, and
        the callback will restore curriculum state to READY.
        """
        self.machine.set_state(self.STATE_READY)

    def load(self):
        """Loads the Curriculum and all the Package information.

        When this method is called, the Curriculum can transition to a
        'ready' state.
        """
        super().load()

        report.send_message(
            report.CurriculumGeneralInfoMessage("Classroom initialization.")
        )

        self.classroom = SingleClassroom(
            self._mammut_session_context,
            self,
            self._academic_period_finished_callback,
            self._curriculum_process_stop_callback,
        )
        self.classroom.initialize()

        report.send_message(
            report.CurriculumGeneralInfoMessage("Curriculum load completed.")
        )

        self.trigger(self.PREPARE_TRIGGER)

    def begin(self):
        """Start the processing of the Curriculum learning.

        Use case: to start all the concurrent/parallel processing
        of lessons.

        The curriculum process will begin from the last checkpoint
        (if exists) or from the curriculum first academic period.

        Preconditions:
            - No Curriculum learning process can be started if the
                curriculum state is different than 'ready'.
        """
        if self.state == self.STATE_READY.name:
            self._started = True
            self.trigger(self.BEGIN_COURSES_TRIGGER)

        else:
            message = "Curriculum isn't in a valid state for begin(). Nothing happens."
            self.errors += message
            report.send_message(
                report.CurriculumGeneralWarningMessage(message)
            )

    def stop(self):
        """Stops the processing of the Curriculum learning.

        Use case: Stop the processing and free the computing
        resources.

        Note: Currently, calling this method does not guarantee the checkpoint
        persistence of the current lessons models being processed.
        """
        if self.state == self.STATE_ASSIGNED.name:
            self.classroom.stop()
