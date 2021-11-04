from logging import Logger

from paretos import OptimizationResultInterface, optimization
from paretos.exceptions import ProjectNotFoundError
from paretos.export import OptimizationResult
from paretos.socrates.project_api_client import ProjectApiClient


class ObtainHandler:
    def __init__(
        self,
        logger: Logger,
        api_client: ProjectApiClient,
    ):
        self.__logger = logger
        self.__api_client = api_client

    def obtain(self, name: str) -> OptimizationResultInterface:
        done_evaluations = optimization.Evaluations()

        project_id = self.__api_client.get_project_id_by_name(name=name)
        if project_id is None:
            self.__logger.error("Project not found.", extra={"projectName": name})
            raise ProjectNotFoundError()

        project = self.__api_client.show_project(project_id=project_id)

        evaluations = self.__api_client.analyze_evaluations(project_id=project_id)

        if not isinstance(project.get_status(), optimization.project_status.Done):
            self.__logger.warning(
                "Optimization was not finished correctly, data might be incomplete."
            )

        for evaluation in evaluations:
            done_evaluations.add_evaluation(evaluation=evaluation)

        return OptimizationResult(done_evaluations)
