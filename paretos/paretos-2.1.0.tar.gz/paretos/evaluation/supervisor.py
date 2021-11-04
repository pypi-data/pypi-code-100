from logging import Logger
from typing import List

from .. import TerminatorInterface
from ..optimization import Project
from ..socrates.project_api_client import ProjectApiClient


class Supervisor:
    """
    Decides whether more evaluations should be started or not.
    """

    def __init__(
        self,
        api_client: ProjectApiClient,
        terminators: List[TerminatorInterface],
        logger: Logger,
        project: Project,
    ):
        self.__api_client = api_client
        self.__terminators = terminators
        self.__logger = logger
        self.__project = project

    def is_process_finished(self):
        try:
            progress = self.__api_client.track_progress(
                project_id=self.__project.get_id()
            )
        except Exception as api_tracking_error:
            self.__logger.error("Unable to update optimization progress.")
            raise api_tracking_error

        is_process_finished = any(
            [
                terminator.should_terminate(progress=progress)
                for terminator in self.__terminators
            ]
        )

        return is_process_finished
