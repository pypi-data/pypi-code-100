from typing import Union

from paretos.app.src.command_handler.command_handler import CommandHandler
from paretos.app.src.command_handler.outcome.not_found_failure import NotFoundFailure
from paretos.app.src.command_handler.outcome.outcome import Outcome
from paretos.app.src.service.logger import Logger
from paretos.app.src.service.response_mapper import DataApiResponseMapper
from paretos.socrates.project_api_client import ProjectApiClient


class GetProjectMeta(CommandHandler):
    _methods = ["POST"]
    _schema = {
        "type": "object",
        "properties": {"project": {"type": "string"}},
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
        self.__logger.info(
            "getting project meta",
            project_meta_input={"project": request_data["project"]},
        )

        project = self.__api_client.show_project(project_id=request_data["project"])

        if project is None:
            return NotFoundFailure()

        problem = project.get_optimization_problem()

        return DataApiResponseMapper.problem_to_request(problem)
