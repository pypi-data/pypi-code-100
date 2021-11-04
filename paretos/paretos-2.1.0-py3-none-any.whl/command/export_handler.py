from logging import Logger
from typing import Dict, List

from paretos.exceptions import ProjectNotFoundError
from paretos.socrates.project_api_client import ProjectApiClient


class ExportHandler:
    def __init__(self, logger: Logger, api_client: ProjectApiClient):
        self.__logger = logger
        self.__api_client = api_client

    def export(self, project_name: str) -> List[Dict]:
        project_id = self.__api_client.get_project_id_by_name(name=project_name)
        if project_id is None:
            self.__logger.error(
                "Project not found.", extra={"projectName": project_name}
            )
            raise ProjectNotFoundError()

        evaluations = self.__api_client.analyze_evaluations(project_id=project_id)

        export_data = []

        for evaluation in evaluations:
            export_row = {
                "project_id": project_id,
                "evaluation_id": evaluation.get_id(),
                "is_pareto_optimal": evaluation.is_pareto_optimal(),
                **{
                    "design__" + param.get_parameter().get_name(): param.get_value()
                    for param in evaluation.get_design().get_values()
                },
                **{
                    "kpi__" + param.get_parameter().get_name(): param.get_value()
                    for param in evaluation.get_kpis().get_values()
                },
            }

            export_data.append(export_row)

        return export_data
