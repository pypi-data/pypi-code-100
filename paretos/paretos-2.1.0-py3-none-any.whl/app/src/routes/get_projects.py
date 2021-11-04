from typing import Union

from paretos.app.src.command_handler.command_handler import CommandHandler
from paretos.app.src.command_handler.outcome.outcome import Outcome
from paretos.app.src.service.logger import Logger
from paretos.optimization.project_status import Done
from paretos.socrates.project_api_client import ProjectApiClient


class GetProjects(CommandHandler):
    _methods = ["POST"]

    def __init__(
        self,
        logger: Logger,
        api_client: ProjectApiClient,
    ):
        self.__logger = logger
        self.__api_client = api_client

    def process(self, request_data: dict) -> Union[dict, Outcome]:
        self.__logger.info("getting projects", projects_input={})
        project_ids = self.__api_client.list_projects()

        result_projects = []

        for project_id in project_ids:
            project = self.__api_client.show_project(project_id=project_id)

            if project is None:
                raise RuntimeError("There are no data for this project available")

            progress = self.__api_client.track_progress(project_id=project_id)

            n_status = 0.0
            if type(project.get_status()) is Done:
                n_status = 100.0

            problem = project.get_optimization_problem()
            kpis = [kpi.get_name() for kpi in problem.get_kpi_space()]
            result_projects.append(
                {
                    "id": project.get_id(),
                    "description": None,
                    "name": project.get_name(),
                    "targets": kpis,
                    "status": n_status,
                    "number_pareto": progress.get_nr_of_pareto_points(),
                }
            )

        return {"projects": result_projects}
