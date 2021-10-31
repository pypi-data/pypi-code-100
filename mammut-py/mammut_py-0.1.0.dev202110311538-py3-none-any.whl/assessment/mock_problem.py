from mammut.assessment.problem import Problem
from mammut.curriculum.models.mock import TestMockModel
import time
from typing import Dict


class MockProblem(Problem):
    """Concrete class to evaluate a Mock curriculum process
    in testing.
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
        Problem.__init__(
            self,
            course_id,
            assessment_id,
            schedule,
            problem_id,
            problem_type,
            parameters,
            language_competence,
            weight,
            retry,
            observations,
        )
        self._sleep_sc = 3

    def solve(self, model: TestMockModel, **kwargs) -> bool:
        """Mocks solving of a problem. Always solved.
        """
        self._retries_count += 1
        time.sleep(self._sleep_sc)
        return True

    def get_result_info(self) -> Dict:
        info = {"Test info": "Nothing, just a mock."}
        return info
