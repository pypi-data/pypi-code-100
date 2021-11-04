from typing import Dict, List, Optional, Union

from ..optimization import Evaluation, OptimizationProblem, Progress, Project
from ..optimization.design import DesignParameter, DesignSpace, DesignValues
from ..optimization.design.continuity import Continuous, Discrete
from ..optimization.goals import Maximum, Minimum
from ..optimization.kpi import KpiParameter, KpiSpace, KpiValues
from ..optimization.parameter import Parameter, ParameterValue
from ..optimization.project_status import Done, Ready
from .socrates_api_http_session import SocratesApiHttpSession


class ProjectApiClient(object):
    def __init__(self, session: SocratesApiHttpSession):
        self.__session = session

    def get_project_id_by_name(self, name: str) -> Optional[str]:
        for id in self.list_projects():
            project = self.show_project(project_id=id)
            if project.get_name() == name:
                return project.get_id()
        return None

    def list_projects(self) -> List[str]:
        response = self.__session.authenticated_request(
            path="project/list", version="v2", data={}, contains_sensitive_data=False
        )

        return response["project_ids"]

    def plan_project(self, label: str, problem: OptimizationProblem) -> Project:
        design_definition = {}
        for param in problem.get_design_space():
            design_definition[param.get_name()] = {
                "name": param.get_name(),
                "minimum": param.get_minimum(),
                "maximum": param.get_maximum(),
                "continuity": self.__continuity_2_api(param.get_continuity()),
            }

        target_definition = {}
        for param in problem.get_kpi_space():
            target_definition[param.get_name()] = {
                "name": param.get_name(),
                "goal": self.__goal_2_api(param.get_goal()),
            }

        data = {
            "label": label,
            "design_definition": design_definition,
            "target_definition": target_definition,
        }
        response = self.__session.authenticated_request(
            path="project/plan", version="v2", contains_sensitive_data=False, data=data
        )

        project_id = response["project_id"]
        project = Project(uuid=project_id, name=label, problem=problem)
        return project

    def show_project(self, project_id: str) -> Project:
        data = {"project_id": project_id}
        response = self.__session.authenticated_request(
            path="project/show", version="v2", contains_sensitive_data=False, data=data
        )

        return self.__map_project(project_data=response)

    def finish_project(self, project_id: str):
        data = {"project_id": project_id}
        self.__session.authenticated_request(
            path="project/finish",
            version="v2",
            contains_sensitive_data=False,
            data=data,
        )

    def analyze_project(
        self, project_id: str, only_pareto_optimal: bool = False
    ) -> Dict[str, bool]:
        data = {"project_id": project_id, "onlyParetoOptimal": only_pareto_optimal}
        response = self.__session.authenticated_request(
            path="project/analyze",
            version="v2",
            contains_sensitive_data=False,
            data=data,
        )
        return {
            data["evaluation_id"]: data["isParetoOptimal"]
            for data in response["evaluations"]
        }

    def plan_evaluation(
        self, project_id: str, desiredQuantity: int
    ) -> List[Evaluation]:
        data = {
            "project_id": project_id,
            "desiredQuantity": desiredQuantity,
        }
        response = self.__session.authenticated_request(
            path="evaluations/plan",
            version="v2",
            contains_sensitive_data=False,
            data=data,
        )
        return [self.__map_evaluation(data) for data in response["plannedEvaluations"]]

    def show_evaluations(self, evaluation_ids: List[str]) -> List[dict]:
        response = self.__session.authenticated_request(
            path="evaluations/show",
            version="v2",
            contains_sensitive_data=False,
            data=evaluation_ids,
        )
        return response["evaluations"]

    def submit_evaluation(self, evaluation: Evaluation):
        target_values = {}
        for kpi in evaluation.get_kpis():
            target_values[kpi.get_parameter().get_name()] = kpi.get_value()
        data = [{"evaluation_id": evaluation.get_id(), "targetValues": target_values}]
        self.__session.authenticated_request(
            path="evaluations/submit",
            version="v2",
            contains_sensitive_data=False,
            data=data,
        )

    def analyze_evaluations(
        self, project_id: str, only_pareto_optimal: bool = False
    ) -> List[Evaluation]:
        analyzation = self.analyze_project(
            project_id=project_id, only_pareto_optimal=only_pareto_optimal
        )
        evaluation_ids = [*analyzation]
        evaluations = self.show_evaluations(evaluation_ids)
        return [
            self.__map_evaluation(data, analyzation[data["id"]]) for data in evaluations
        ]

    def track_progress(self, project_id):
        data = {"project_id": project_id}
        response = self.__session.authenticated_request(
            path="project/progress/track",
            version="v2",
            contains_sensitive_data=False,
            data=data,
        )
        return Progress(
            nr_of_evaluations=response["nrOfEvaluations"],
            nr_of_pareto_points=response["nrOfParetoPoints"],
        )

    def __map_project(self, project_data) -> Project:
        id = project_data["id"]
        label = project_data["label"]
        problem = self.__map_problem(
            design=project_data["design_definition"],
            target=project_data["target_definition"],
        )
        status = Ready() if project_data["finished_at"] is None else Done()
        project = Project(uuid=id, name=label, problem=problem, status=status)
        return project

    def __map_problem(self, design, target) -> OptimizationProblem:
        design_params = []
        target_params = []
        for param in design.values():
            name = param["name"]
            minimum = param["minimum"]
            maximum = param["maximum"]
            continuity = param["continuity"]
            design_params.append(
                DesignParameter(
                    name=name,
                    uuid=name,
                    minimum=minimum,
                    maximum=maximum,
                    continuity=continuity,
                )
            )

        for param in target.values():
            name = param["name"]
            goal = Minimum() if param["goal"] == "minimize" else Maximum()
            target_params.append(KpiParameter(name=name, uuid=name, goal=goal))

        design_space = DesignSpace(parameters=design_params)
        kpi_space = KpiSpace(parameters=target_params)
        problem = OptimizationProblem(design_space=design_space, kpi_space=kpi_space)
        return problem

    def __map_evaluation(self, data, is_pareto_optimal: bool = False) -> Evaluation:
        uuid = data["id"]
        design_values = DesignValues(self.__map_parameter_values(data["design"]))
        kpis = None
        if "target" in data:
            kpis = KpiValues(self.__map_parameter_values(data["target"]))
        evaluation = Evaluation(
            uuid=uuid,
            design=design_values,
            kpis=kpis,
            is_pareto_optimal=is_pareto_optimal,
        )
        return evaluation

    def __map_parameter_values(self, params) -> List[ParameterValue]:
        return [
            ParameterValue(
                parameter=Parameter(name=param["name"], uuid=param["name"]),
                value=param["value"],
            )
            for param in params.values()
        ]

    def __goal_2_api(self, goal: Union[Minimum, Maximum]) -> str:
        if isinstance(goal, Minimum):
            return "minimize"
        else:
            return "maximize"

    def __continuity_2_api(self, continuity: Union[Continuous, Discrete]) -> str:
        if isinstance(continuity, Continuous):
            return "continuous"
        else:
            return "discrete"
