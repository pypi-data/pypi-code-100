from typing import List, Optional, Set
from mammut.curriculum.core.curriculum_base import CurriculumBase
from mammut.curriculum.classroom.ray_classroom import RayClassroom
from mammut.curriculum.classroom.classroom_pool import ClassroomPool
from mammut.curriculum.models.online_models.online_models import OnlineModelsRegistry
from mammut.curriculum.course.course import Course
from mammut.curriculum.course.course_state import CourseState
from mammut.curriculum.core.curriculum_state_machine import (
    CurriculumStateMachineMixin,
)
from mammut.curriculum.report.reporters.ray_reporter_registry import (
    RayReportersRegistry,
)
import mammut.curriculum.report as report
import threading
import time
import logging
import ray
import os

log = logging.getLogger(__name__)


class DistributedCurriculum(CurriculumBase, CurriculumStateMachineMixin):
    """Models the Curriculum learning in a multi classroom environment.

    A Curriculum is composed of a set of courses.
    Each course attempts to train language competences that belongs
    to a language level (https://doc.mammut.io/docs_es/framework/language_arquitecture/).

    The courses in a Curriculum forms a flowchart, which is
    a directed acyclic graph. The flowchart implies that courses are
    meant to be progressive, which allows to organize them into academic
    periods.
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
        enable_ktt_interpretation: bool = True,
    ):
        super(DistributedCurriculum, self).__init__(
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
            enable_ktt_interpretation=enable_ktt_interpretation,
        )
        self._next_academic_period_courses: Set[Course] = set()
        self._next_academic_period_assigned_classrooms: List[
            RayClassroom
        ] = list()
        self.classroom_pool: Optional[ClassroomPool] = None
        """
        Attribute flag to indicate auto transition
        after first academic period has been executed.
        """
        self._started: bool = False
        self._processing_polling_thread: threading.Thread = None
        self._remote_reporting_listener_thread: threading.Thread = None

        # Todo: this search path fot KtT Transducer must be taken from configuration.
        #   Currently, there's another branch incorporating configuration.
        ktt_jar_search_path = (
            os.path.expanduser("~")
            + "/.mammut-py/ktt/mammut-transducer-ktt.jar"
        )

        # initializes the remote RayReportersRegistry actor
        # Todo: this ray initialization will probably change of place in the future.
        if not ray.is_initialized():
            ray.init(
                log_to_driver=False,
                job_config=ray.job_config.JobConfig(
                    code_search_path=[ktt_jar_search_path]
                ),
            )

        self._mammut_session_context.main_report_actor_handle = (
            RayReportersRegistry.remote()
        )

        self._mammut_session_context.online_models_registry = (
            OnlineModelsRegistry.remote()
        )

    def _compute_next_academic_period(self):
        """Select the set of courses and classrooms for the next academic period.
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
            Right now, the max number of classrooms equals the max number of 
            parallel courses in the academic periods. 
        """
        for i in range(len(self._next_academic_period_courses)):
            self._next_academic_period_assigned_classrooms.append(
                self.classroom_pool.take_out()
            )

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
            )
        )
        if self._started:
            self.trigger(self.BEGIN_COURSES_TRIGGER)

    def _all_courses_completed(self) -> bool:
        """Returns False if there's at least one unapproved.
        """
        return len(self._next_academic_period_courses) == 0

    def _update_course_state(self, records: Set[CourseState]):

        report.send_message(
            report.CurriculumGeneralDebugMessage("Update courses records.")
        )

        courses_table = self.flowchart.graph_dict

        for record in records:
            course: Course = courses_table[record.course_id]
            course.fetch_course_state(record)

    def _poll_academic_period_state(self):
        """Request for the courses state and the messages reports to classrooms.

        When all the courses has been processed, this method will
        request the course records to fetch the head curriculum state,
        and finally will invoke COURSES_COMPLETED_TRANSITION transition.
        """
        sleep_interval = 20

        # Classrooms are closed (at least one) they haven't started the processing.
        while not all(
            list(
                map(
                    lambda classroom: ray.get(classroom.get_state.remote())
                    != RayClassroom.STATE_CLOSED,
                    self._next_academic_period_assigned_classrooms,
                )
            )
        ):
            time.sleep(5)  # Wait 5 seconds

        # Classrooms (at least one) are busy processing courses.
        while not all(
            list(
                map(
                    lambda classroom: ray.get(classroom.get_state.remote())
                    != RayClassroom.STATE_BUSY,
                    self._next_academic_period_assigned_classrooms,
                )
            )
        ):
            time.sleep(sleep_interval)

        # Get course state from distributed classrooms.
        states: List[CourseState] = []
        for classroom in self._next_academic_period_assigned_classrooms:
            states += list(ray.get(classroom.get_last_courses_record.remote()))

        # finally, closes the classrooms and puts the back in the pool
        self._close_classrooms()
        report.send_message(
            report.CurriculumGeneralDebugMessage(
                "Classrooms processing completed for academic period."
            )
        )

        self._update_course_state(states)
        self.trigger(self.ASSIGNED_COURSES_COMPLETED_TRIGGER)

    def _close_classrooms(self):
        """Close the current academic period classrooms, and puts them back
        in the pool.
        """
        for course in self._next_academic_period_assigned_classrooms:
            course.close.remote()

        for classroom in self._next_academic_period_assigned_classrooms:
            self.classroom_pool.put_in(classroom)

        self._next_academic_period_assigned_classrooms = []

    def _take_courses(self):
        """This is a wrapper function for course executor
        take_courses method.

        It is configured to be invoked when the curriculum
        makes the transition to ASSIGNED_STATE.

        Right now, the max number of classroom is the max number
        of parallel courses in the same academic period. Given so, it's safe
        to assume that courses and classrooms containers have the same length.
        """
        assigned_courses_classrooms = list(
            zip(
                self._next_academic_period_assigned_classrooms,
                self._next_academic_period_courses,
            )
        )

        # Send courses to remote classrooms
        [
            classroom.take_courses.remote(
                set([course.course_id]), self.package.main_id
            )
            for classroom, course in assigned_courses_classrooms
        ]

        report.send_message(
            report.CurriculumGeneralDebugMessage(
                "Courses scheduled in distributed classrooms."
            )
        )
        polling_thread = threading.Thread(
            target=self._poll_academic_period_state,
            name="poll_multi_classrooms",
        )
        polling_thread.start()

    def _remote_reporting_listener(self):
        """Function to be executed concurrently,
        requesting new messages from the remote reporting.

        TODO: sleep interval between updates should be a config
            value.
        """
        interval = 10

        while True:
            new_messages = ray.get(
                self._mammut_session_context.main_report_actor_handle.get_messages.remote()
            )
            for message in new_messages:
                report.send_message(message)
            time.sleep(interval)

    def load(self):
        """Loads the Curriculum and all the Package information.

        When this method is called, the Curriculum can transition to a
        'ready' state.
        """
        super().load()

        self._remote_reporting_listener_thread = threading.Thread(
            target=self._remote_reporting_listener,
            name="remote_reporting_listener",
            daemon=True,
        )
        self._remote_reporting_listener_thread.start()

        report.send_message(
            report.CurriculumGeneralInfoMessage(
                "Main report registry configured."
            )
        )

        report.send_message(
            report.CurriculumGeneralInfoMessage(
                "Multi classrooms initialization"
            )
        )

        self.classroom_pool = ClassroomPool(
            self.flowchart.get_max_parallel_courses(),
            self.package.main_id,
            self.package.standard_spreadsheet_id,
            self._mammut_session_context,
            self._enable_ktt_interpretation,
            self.package.package_id_is_spreadsheet,
        )

        report.send_message(
            report.CurriculumGeneralInfoMessage("Curriculum load completed.")
        )

        # TODO: transition is called here, but the classrooms will be loading remotely.
        #   that should be considered in some kind of mechanism.
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
            self.classroom_pool.stop()
