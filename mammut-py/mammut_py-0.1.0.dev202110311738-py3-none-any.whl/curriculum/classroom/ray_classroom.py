from mammut.curriculum.classroom.single_classroom import SingleClassroom
import ray
from typing import Set
import transitions
import mammut.curriculum.report as report
from mammut.curriculum.core.mammut_session_context import MammutSessionContext


@ray.remote
class RayClassroom(SingleClassroom):
    """Classroom designed to be a workspace in a multi-classroom ray architecture.
    """

    # States
    """
    Closed state means the classroom was closed by Curriculum control, 
    and no new courses has arrived for new processing.
    """
    STATE_CLOSED = "closed"

    """
    Busy state when the classroom is processing a set of courses.
    A classroom will be busy when new courses arrive for processing 
    after being closed.
    """
    STATE_BUSY = "busy"

    """
    Idle state when the classroom isn't processing anything. 
    After processing a set of courses, the classroom will be idle 
    until control client classes close the classroom.
    """
    STATE_IDLE = "idle"

    STATES = [STATE_BUSY, STATE_IDLE, STATE_CLOSED]

    def __init__(self, mammut_session_context: MammutSessionContext):
        """
        Args:
            mammut_session_context: The session context for this classroom and the
                curriculums in it.
        """
        super().__init__(mammut_session_context)
        self.machine = transitions.Machine(
            model=self, states=self.STATES, initial=self.STATE_CLOSED
        )

        # Configure remote reporting. This process worker will report remotely.
        report.set_mammut_session_context(mammut_session_context)
        report.enable_remote()

    def _process_courses_loop(
        self, courses_ids: Set[int], curriculum_package_id: str
    ) -> None:
        """Process the courses specified for the curriculum.

        When processing starts, this classroom will transition to "busy"
        state. After finishing all courses processing, will go to
        "idle" state. Control classes can use the state value to know when
        to fetch new data remotely.

        Args:
            courses_ids(Set[int]): set of courses IDs to be processed
                from the desired curriculum.
            curriculum_package_id: Spreadsheet ID of the curriculum
                to take courses from.
        """
        self.to_busy()
        curriculum = self._curriculums[curriculum_package_id]
        self._last_courses = set(
            [
                course
                for course in curriculum.courses
                if course.course_id in courses_ids
            ]
        )

        report.send_message(
            report.CurriculumGeneralInfoMessage(
                f"Scheduling {len(self._last_courses)} in Classroom."
            )
        )

        report.send_message(
            report.CurriculumGeneralDebugMessage(
                f"Processing {len(self._last_courses)} courses in "
                f"classroom {self.id()}"
            )
        )

        for c in self._last_courses:
            c.start(curriculum.progress, self._mammut_session_context)

        report.send_message(
            report.CurriculumGeneralDebugMessage(
                f"Process completed in classroom: {self.id()}"
            )
        )

        self.to_idle()

    def stop(self):
        """Currently there's nothing to stop """
        pass

    def get_state(self):
        return self.state

    def close(self):
        self.to_closed()
