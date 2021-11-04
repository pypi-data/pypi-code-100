from logging import Logger
from typing import List

from ..optimization import Evaluation, Project
from ..socrates.project_api_client import ProjectApiClient


class EvaluationPlanner:
    """
    Provides new evaluations by fetching designs from the Socrates API and
    saving them to the database.
    """

    def __init__(
        self,
        api_client: ProjectApiClient,
        project: Project,
        logger: Logger,
    ):
        self.__api_client = api_client
        self.__project = project
        self.__logger = logger

    def generate(self, quantity: int) -> List[Evaluation]:
        self.__logger.debug(
            "Fetching new designs from Socrates API", extra={"quantity": quantity}
        )
        evaluations = self.__api_client.plan_evaluation(
            project_id=self.__project.get_id(),
            desiredQuantity=quantity,
        )

        return evaluations
