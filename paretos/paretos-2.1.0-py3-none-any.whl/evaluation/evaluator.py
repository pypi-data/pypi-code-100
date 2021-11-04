from logging import Logger
from typing import Union

from .. import AsyncEnvironmentInterface, EnvironmentInterface, optimization
from ..socrates.project_api_client import ProjectApiClient
from .kpi_sanitizer import KpiSanitizer


class Evaluator:
    """
    Performs the evaluation by executing the individual Environment implementation
    with a specific design, validating the resulting KPIs and saving them to the
    database.
    """

    def __init__(
        self,
        logger: Logger,
        environment: Union[EnvironmentInterface, AsyncEnvironmentInterface],
        api_client: ProjectApiClient,
        kpi_sanitizer: KpiSanitizer,
    ):
        self.__logger = logger
        self.__environment = environment
        self.__api_client = api_client
        self.__kpi_sanitizer = kpi_sanitizer

    async def evaluate(self, evaluation: optimization.Evaluation):
        design_values = evaluation.get_design().to_dict()

        self.__logger.info(
            "Starting evaluation.",
            extra={
                "evaluationId": evaluation.get_id(),
                "design": design_values,
            },
        )

        try:
            if isinstance(self.__environment, AsyncEnvironmentInterface):
                original_kpis = await self.__environment.evaluate_async(
                    design_values=design_values
                )
            elif isinstance(self.__environment, EnvironmentInterface):
                original_kpis = self.__environment.evaluate(design_values=design_values)
            else:
                raise RuntimeError(
                    "Unexpected environment object type. Make sure to inherit from "
                    "one of the provided environment interfaces."
                )
        except Exception as simulation_exception:
            self.__logger.error(
                "Evaluation failed.",
                extra={"evaluationId": evaluation.get_id()},
            )

            raise simulation_exception

        kpis = self.__kpi_sanitizer.clean_kpis(
            original_kpis=original_kpis,
            evaluation_uuid=evaluation.get_id(),
        )

        self.__logger.info(
            "Evaluation successful.",
            extra={"evaluationId": evaluation.get_id(), "kpis": original_kpis},
        )

        evaluation.add_result(kpis)

        try:
            self.__api_client.submit_evaluation(evaluation=evaluation)
        except Exception as database_error:
            self.__logger.error("Saving evaluation result failed.")
            raise database_error
