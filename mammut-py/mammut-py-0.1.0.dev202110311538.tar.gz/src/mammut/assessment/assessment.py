from mammut.assessment.problem import Problem
from typing import List, Dict
from mammut.curriculum.lesson import lesson_base


class Assessment:
    """Assessment class bundles multiple problems together.

    The main concern of this class is encapsulate in a single
    unit a set of problems.
    """

    def __init__(self, assessment_id, problems: List[Problem], course_id: int):
        self.assessment_id = int(assessment_id)
        self.errors: List[str] = []
        self.valid = True
        self.problems: List[Problem] = problems
        self.course_id = course_id
        self.approved_problems_weights_sum: float = 0.0
        self.approved_problems_id: List = []
        self.failed_problems_id: List = []
        self.failed_problems_info: Dict = {}

    def apply(self, lesson: lesson_base.Lesson) -> float:
        """This method applies the evaluation process
        encapsulated on each problem, to a trained model
        contained by a Lesson.

        Returns:
            Returns the weights sum for the approved problems.
        """
        self.approved_problems_weights_sum: float = 0.0
        for p in self.problems:
            solved = False
            while not solved and p.is_retry_allowed():
                solved = p.solve(lesson.model)

            if solved:
                self.approved_problems_weights_sum += p.weight
                self.approved_problems_id.append(p.problem_id)
            else:
                self.failed_problems_id.append(p.problem_id)
                p_results = p.get_result_info()
                p_results["retries"] = p.retries_count
                self.failed_problems_info[p.problem_id] = p_results

        return self.approved_problems_weights_sum
