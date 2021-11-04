from typing import List

from .evaluation import Evaluation


class Evaluations:
    """
    Contains all current evaluations and is meant to keep the set up to date during
    the optimization process.
    """

    def __init__(self, evaluations: List[Evaluation] = None):
        if evaluations is None:
            self.__evaluations = []
        else:
            self.__evaluations = evaluations.copy()

    def get_evaluations(self) -> List[Evaluation]:
        return self.__evaluations.copy()

    def add_evaluation(self, evaluation: Evaluation):
        self.__evaluations.append(evaluation)

    def get_pareto_optimal_evaluations(self) -> List[Evaluation]:
        pareto_optima = []

        for evaluation in self.__evaluations:
            if evaluation.is_pareto_optimal():
                pareto_optima.append(evaluation)

        return pareto_optima

    def get_finished_evaluations(self) -> List[Evaluation]:
        finished_evaluations = []

        for evaluation in self.__evaluations:
            if evaluation.get_kpis() is not None:
                finished_evaluations.append(evaluation)

        return finished_evaluations

    def size(self) -> int:
        return len(self.__evaluations)
