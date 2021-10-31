from mammut.curriculum.classroom.ray_classroom import RayClassroom
from mammut.curriculum.core.mammut_session_context import MammutSessionContext
from typing import Set
import ray
import mammut.curriculum.report as report


class ClassroomPool:
    """Pool of RayClassroom instances for client classes.

    RayClassrooms are instantiated at initialization time.
    The number of classrooms is fixed.
    """

    def __init__(
        self,
        classrooms: int,
        package_id: str,
        standard_spreadsheet_id: str,
        mammut_session_context: MammutSessionContext,
        enable_ktt_interpretation: bool,
        package_id_is_spreadsheet: bool
    ):
        """

        Args:
            classrooms(int): number of classrooms to hold in this class.
            package_id(str): package spreadsheet ID / presentation ID to forward to remote classrooms.
            standard_spreadsheet_id(str): standard spreadsheet id to forward to remote classrooms.
            mammut_session_context: The session context to pass down to remote classrooms processes.
            enable_ktt_interpretation (bool): if True, remote classrooms will load an instance of Ktt interpretation
                 course
             package_id_is_spreadsheet (bool): True if the package ID is from a presentation.
        """

        self._mammut_session_context: MammutSessionContext = mammut_session_context

        report.send_message(
            report.CurriculumGeneralDebugMessage(
                "Creating classrooms in remote workers"
            )
        )

        self._available: Set[RayClassroom] = set(
            [
                RayClassroom.remote(self._mammut_session_context)
                for i in range(classrooms)
            ]
        )

        self._known_classrooms = set(
            [ray.get(classroom.id.remote()) for classroom in self._available]
        )

        [classroom.initialize.remote() for classroom in self._available]

        [
            classroom.add_curriculum.remote(
                package_id,
                standard_spreadsheet_id,
                enable_ktt_interpretation=enable_ktt_interpretation,
                package_id_is_spreadsheet=package_id_is_spreadsheet
            )
            for classroom in self._available
        ]

    def available(self) -> bool:
        """Returns True if there are more classrooms available.
        """
        return bool(self._available)

    def take_out(self):
        """Take out a classroom from this pool.

        After calling this method, there will be one less available
        course.

        Returns:
            A classroom instance. None if there aren't any available.
        """
        if self.available():
            report.send_message(
                report.CurriculumGeneralDebugMessage(
                    "Classroom take_out from classrooms pool."
                )
            )
            return self._available.pop()
        else:
            return None

    def put_in(self, classroom: RayClassroom):
        """Put the element back in the pool.

        Raises:
            ValueError: when an unknown classrooms tries to be inserted in the pool.
        """
        if ray.get(classroom.id.remote()) not in self._known_classrooms:
            message = (
                "Wrong classroom argument. No previously known classroom."
            )
            report.send_message(report.CurriculumGeneralErrorMessage(message))
            raise ValueError(message)

        report.send_message(
            report.CurriculumGeneralDebugMessage(
                "Classroom put_in to classrooms pool."
            )
        )
        self._available.add(classroom)
