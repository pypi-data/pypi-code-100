from typing import Union

from paretos.app.src.command_handler.command_handler import CommandHandler
from paretos.app.src.command_handler.outcome.not_found_failure import NotFoundFailure
from paretos.app.src.command_handler.outcome.outcome import Outcome
from paretos.app.src.service.logger import Logger
from paretos.app.src.service.response_mapper import DataApiResponseMapper
from paretos.optimization import Evaluations
from paretos.socrates.project_api_client import ProjectApiClient


class GetSolutions(CommandHandler):
    _methods = ["POST"]
    _schema = {
        "type": "object",
        "properties": {
            "project": {"type": "string"},
            "only_paretos": {"type": "boolean"},
        },
        "required": ["project"],
    }

    def __init__(
        self,
        logger: Logger,
        api_client: ProjectApiClient,
    ):
        self.__logger = logger
        self.__api_client = api_client

    def process(self, request_data: dict) -> Union[dict, Outcome]:

        only_paretos = True

        if "only_paretos" in request_data.keys():
            only_paretos = request_data["only_paretos"]

        self.__logger.info(
            "getting project solutions",
            solutions_input={
                "project": request_data["project"],
                "only_paretos": only_paretos,
            },
        )

        project = self.__api_client.show_project(project_id=request_data["project"])

        if project is None:
            return NotFoundFailure()

        evaluations = Evaluations(
            self.__api_client.analyze_evaluations(
                project_id=project.get_id(), only_pareto_optimal=only_paretos
            )
        )

        return {
            "evaluations": DataApiResponseMapper.evaluations_to_request(evaluations)
        }
