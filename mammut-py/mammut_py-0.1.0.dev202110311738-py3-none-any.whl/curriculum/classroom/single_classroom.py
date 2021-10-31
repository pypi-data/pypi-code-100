from mammut.curriculum.classroom.classroom import Classroom
import threading
from typing import Callable, Set, Optional
from mammut.curriculum.core.mammut_session_context import MammutSessionContext


class SingleClassroom(Classroom):
    """
        Single classroom designed for academic period courses
        execution on a single machine.
    """

    def __init__(
        self,
        mammut_session_context: MammutSessionContext,
        curriculum: Optional["Curriculum"] = None,
        academic_period_finished_callback: Optional[Callable] = None,
        curriculum_process_stopped_callback: Optional[Callable] = None,
    ):
        """
        Arguments are optional for subclassing convenience.

        Args:
            mammut_session_context: The session context for this classroom and the
                curriculums in it.
            curriculum: reference for single machine shared curriculum.
            academic_period_finished_callback: callback to notify academic period
                finished.
            curriculum_process_stopped_callback: callback to notify processing stop.
        """
        super().__init__(mammut_session_context)
        if curriculum is not None:
            self.add_curriculum(curriculum_reference=curriculum)

        self._academic_period_finished_callback = (
            academic_period_finished_callback
        )
        self._process_stopped_callback = curriculum_process_stopped_callback

        """
        Classroom processing is performed sequentially in a single thread.
        """
        self._main_thread: threading.Thread = None
        self._stop_main_thread_event: threading.Event = None

    def initialize(self):
        self._stop_main_thread_event = threading.Event()

    def _process_courses_loop(
        self, courses_ids: Set[int], curriculum_spreadsheet_id: str
    ):
        """
        Process courses found in courses_ids. This method communicates with
        Curriculum instance for state changing using provided callbacks.
        """
        if self._stop_main_thread_event.is_set():
            """
            The next academic period wouldn't be processed,
            since Curriculum requested stop. 
            """
            self._process_stopped_callback()
            self._stop_main_thread_event.clear()
            return

        curriculum = self._curriculums[curriculum_spreadsheet_id]
        self._last_courses = set(
            [
                course
                for course in curriculum.courses
                if course.course_id in courses_ids
            ]
        )

        for c in self._last_courses:
            if self._stop_main_thread_event.is_set():
                """
                Curriculum requested stop in the middle of an
                academic period. 
                """
                self._process_stopped_callback()
                self._stop_main_thread_event.clear()
                return
            c.start(curriculum.progress, self._mammut_session_context)

        """
        The academic period finished callback will be invoked 
        in new thread. Doing so, the current thread 
        in charge of current academic period processing will reach 
        it's end.

        The new thread will invoke the callback, it will cause 
        the curriculum to compute next semester, and finally will 
        call the take_courses method again thanks to state transitions.
        """
        transition_thread = threading.Thread(
            target=self._academic_period_finished_callback,
            name="academic_period_finished_transition",
        )
        transition_thread.start()

    def take_courses(
        self, courses_ids: Set[int], curriculum_spreadsheet_id: str
    ):
        self._main_thread = threading.Thread(
            target=self._process_courses_loop,
            args=(courses_ids, curriculum_spreadsheet_id),
            name="academic_period_processing",
        )
        self._main_thread.start()

    def stop(self):
        self._stop_main_thread_event.set()
