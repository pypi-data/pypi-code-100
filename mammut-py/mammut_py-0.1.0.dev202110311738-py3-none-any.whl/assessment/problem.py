from abc import ABC, abstractmethod
from mammut.curriculum.core.utils import LanguageCompetence
import json
from typing import Dict
from mammut.curriculum.models.model_base import ModelBase
from mammut.curriculum.report.errors.json_parsing_errors import (
    JSONProblemParsingError,
)
from mammut.curriculum.report.utils import Phase
import mammut.assessment.util as assessment_utils


class Problem(ABC):
    """A problem is the minimal unit of assessment
    to a model.

    A problem is the analogy to an exam question.
    An exam will contain any number of problems.

    The problem has a weight that contributes to the
    final course score. If a problem is approved, then
    the problem weight will be added to the course score.
    """

    def __init__(
        self,
        course_id: str,
        assessment_id: str,
        schedule: str,
        problem_id: str,
        problem_type: str,
        parameters: str,
        language_competence: str,
        weight: str,
        retry: str,
        observations: str,
    ):
        """
        Args:
            course_id(str): 'id' value in datasource retrieved data.
            assessment_id(str): 'assessment_id' value in datasource retrieved data.
            schedule(str): 'schedule' value in datasource retrieved data.
            problem_id(str): 'problem_id' value in datasource retrieved data.
            problem_type(str): 'problem_type' value in datasource retrieved data.
                Should be a string value valid for the ProblemType enumeration.
            parameters(str): 'parameters' value in datasource retrieved data.
                Should be a valid JSON string.
            language_competence(str): 'language_competence' value in datasource retrieved data.
                Should be a string value valid for the LanguageCompetence enumeration.
            weight(str): 'weight' value in datasource retrieved data.
            observations(str): 'observations' value in datasource retrieved data.
        """
        self.course_id: int = int(course_id)
        self.assessment_id: int = int(assessment_id)
        self.schedule: int = int(schedule)
        self.problem_id: int = int(problem_id)
        self.problem_type: str = problem_type
        """
            Replace line breaks from json string.
        """
        try:
            self.parameters: Dict = json.loads(parameters.replace("\n", ""))
        except json.JSONDecodeError as e:
            raise JSONProblemParsingError(
                e,
                Phase.LOAD_ASSESSMENT_DATA,
                course_id,
                assessment_id,
                problem_id,
                assessment_utils.PARAMETERS_COLUMN,
            )
        self.language_competence: LanguageCompetence = LanguageCompetence.from_str(
            language_competence
        )
        self.weight: float = float(weight)
        self.observations: str = observations

        """
            If a problem isn't solved by the model, it can be retried 
            as many times as specified.
        """
        self._retry_value: int = int(retry)
        self._retries_count: int = 0

    def is_retry_allowed(self):
        return self._retries_count < self._retry_value

    @property
    def retries_count(self):
        return self._retries_count

    @abstractmethod
    def solve(self, model: ModelBase, **kwargs) -> bool:
        """Apply the problem to a model, and assess the result.

        Args:
            model: model instance
            kwargs: any other required concrete parameter.

        Returns:
            Boolean to indicate if trained model solved the problem
                or not.
        """
        pass

    @abstractmethod
    def get_result_info(self) -> Dict:
        """Get the results information about this problem
        solving, in json format.
        """
        pass
