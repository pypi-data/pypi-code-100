from logging import Logger
from typing import List, Optional, Union

from .. import (
    CONTINUITY_DISCRETE,
    AsyncEnvironmentInterface,
    EnvironmentInterface,
    KpiGoalMaximum,
    KpiGoalMinimum,
    OptimizationProblem,
    TerminatorInterface,
    optimization,
)
from ..evaluation.evaluation_planner import EvaluationPlanner
from ..evaluation.evaluator import Evaluator
from ..evaluation.kpi_sanitizer import KpiSanitizer
from ..evaluation.scheduler import Scheduler
from ..evaluation.supervisor import Supervisor
from ..socrates.project_api_client import ProjectApiClient


class OptimizeHandler:
    def __init__(
        self,
        logger: Logger,
        api_client: ProjectApiClient,
    ):
        self.__logger = logger
        self.__api_client = api_client

    async def optimize_async(
        self,
        name: str,
        optimization_problem: OptimizationProblem,
        environment: Union[EnvironmentInterface, AsyncEnvironmentInterface],
        terminators: Optional[List[TerminatorInterface]] = None,
        n_parallel: int = 1,
        resume: bool = False,
    ) -> None:
        """
        Main function the user calls when optimizing with socrates
        :param name: project name which will be added to database then!
        :param optimization_problem: hyper space definition of the problem
        :param environment: simulation environment to use for the execution
            :param terminators: list of all terminator functions which can lead to stop
        :param n_parallel: Number of parallel simulations that can be run on customer side
        :param max_number_of_runs: Absolute maximum to have hard stopping criteria
        :param resume: Set to true to resume the optimization if it already exists.
        """

        project = None

        if resume:
            project_id = self.__api_client.get_project_id_by_name(name=name)
            if project_id is not None:
                project = self.__api_client.show_project(project_id=project_id)

        if project is None:
            problem = self.__create_problem_definition(optimization_problem)
            project = self.__api_client.plan_project(label=name, problem=problem)

            self.__logger.info(
                "Started optimization project.",
                extra={
                    "projectId": project.get_id(),
                    "projectName": project.get_name(),
                },
            )
        else:
            self.__logger.info(
                "Resuming project.", extra={"projectName": project.get_name()}
            )

        if terminators is None:
            terminators = [optimization.DefaultTerminator()]

        await self.__optimize(
            project=project,
            terminators=terminators,
            n_parallel=n_parallel,
            environment=environment,
        )

    def __create_problem_definition(
        self, definition: OptimizationProblem
    ) -> optimization.OptimizationProblem:

        design_parameters = []
        kpi_parameters = []

        for definition_kpi_parameter in definition.get_kpi_parameters():
            name = definition_kpi_parameter.get_name()
            goal_string = definition_kpi_parameter.get_goal()

            if goal_string == KpiGoalMinimum:
                parameter_goal = optimization.goals.Minimum()
            elif goal_string == KpiGoalMaximum:
                parameter_goal = optimization.goals.Maximum()
            else:
                raise RuntimeError("Unexpected KPI parameter goal.")

            kpi_parameter = optimization.kpi.KpiParameter(
                name=name, goal=parameter_goal
            )

            kpi_parameters.append(kpi_parameter)

        for definition_design_parameter in definition.get_design_parameters():
            interface_continuity = definition_design_parameter.get_continuity()
            continuity = optimization.design.continuity.Continuous()

            if interface_continuity == CONTINUITY_DISCRETE:
                continuity = optimization.design.continuity.Discrete()

            design_parameter = optimization.design.DesignParameter(
                name=definition_design_parameter.get_name(),
                minimum=definition_design_parameter.get_minimum(),
                maximum=definition_design_parameter.get_maximum(),
                continuity=continuity,
            )

            design_parameters.append(design_parameter)

        design_space = optimization.design.DesignSpace(design_parameters)
        kpi_space = optimization.kpi.KpiSpace(kpi_parameters)
        computational_effort = definition.get_computational_effort()

        return optimization.OptimizationProblem(
            design_space=design_space,
            kpi_space=kpi_space,
            computational_effort=computational_effort,
        )

    async def __optimize(
        self,
        project: optimization.Project,
        terminators: List[TerminatorInterface],
        n_parallel: int,
        environment: Union[EnvironmentInterface, AsyncEnvironmentInterface],
    ):
        problem = project.get_optimization_problem()

        kpi_sanitizer = KpiSanitizer(
            kpi_space=problem.get_kpi_space(), logger=self.__logger
        )

        evaluator = Evaluator(
            logger=self.__logger,
            environment=environment,
            api_client=self.__api_client,
            kpi_sanitizer=kpi_sanitizer,
        )

        planner = EvaluationPlanner(
            api_client=self.__api_client,
            logger=self.__logger,
            project=project,
        )

        supervisor = Supervisor(
            api_client=self.__api_client,
            terminators=terminators,
            logger=self.__logger,
            project=project,
        )

        scheduler = Scheduler(
            logger=self.__logger,
            max_parallel=n_parallel,
            evaluator=evaluator,
            evaluation_planner=planner,
            supervisor=supervisor,
        )

        await scheduler.run()

        self.__logger.info("Optimization finished.")

        project.finish()

        try:
            self.__api_client.finish_project(project_id=project.get_id())
        except Exception as project_status_update_failed:
            self.__logger.error("Unable to set project to finished.")
            raise project_status_update_failed

        progress = self.__api_client.track_progress(project_id=project.get_id())
        self.__logger.info(
            "Result analyzed.",
            extra={
                "evaluations": progress.get_nr_of_evaluations(),
                "paretoPoints": progress.get_nr_of_pareto_points(),
            },
        )
