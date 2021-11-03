import random
from collections import UserDict
from numbers import Number
from typing import Callable, Hashable, Iterable, List, Mapping, Optional, Union, cast

from tabulate import tabulate

from posterior.distributions import CumulativeDistribution

Outcome = Union[str, float, int]
Probability = float

Comparable = Union[float, int, "RandomVariable"]
ProbabilityFunc = Callable[[Outcome], Probability]
InitialOutcomes = Union[Iterable[Outcome], Mapping[Outcome, Probability]]


class RandomVariable(UserDict[Outcome, Probability]):
    """
    Set of outcomes and corresponding probabilities/frequencies of a random variable
    """

    def __init__(
        self,
        outcomes: Optional[InitialOutcomes] = None,
        probability_func: ProbabilityFunc = lambda outcome: 1,
    ):
        if isinstance(outcomes, Iterable):
            outcomes = {outcome: probability_func(outcome) for outcome in outcomes}

        super(RandomVariable, self).__init__(outcomes)
        self.normalize()

    @property
    def total(self):
        return sum(self.values())

    @property
    def mean(self) -> float:
        if not all([isinstance(outcome, Number) for outcome in self.keys()]):
            raise ValueError("Outcomes are not numeric values. Cannot compute the mean")

        return sum(
            [
                cast(float, outcome) * probability
                for outcome, probability in self.items()
            ]
        )

    @property
    def variance(self) -> float:
        if not isinstance(list(self.keys()), Number):
            raise ValueError(
                "Outcomes are not numeric values. Cannot compute the variance"
            )

        mean = self.mean

        return sum(
            [
                probability * (cast(float, outcome) - mean) ** 2
                for outcome, probability in self.items()
            ]
        )

    @property
    def max_likelihood(self) -> Probability:
        return max(self.values())

    def random(self) -> List[Hashable]:
        return random.choices(population=list(self.keys()), weights=list(self.values()))

    def normalize(self, target_total: float = 1.0):
        total = self.total

        if not total:
            return

        norm_factor: float = target_total / total

        for outcome, probability in self.data.items():
            self.data[outcome] = probability * norm_factor

    def __lt__(self, item: Comparable):
        if isinstance(item, RandomVariable):
            # probability that self is less then item
            return sum(
                probability1 * probability2
                for outcome1, probability1 in self.items()
                for outcome2, probability2 in item.items()
                if outcome1 < outcome2
            )

        return sum(
            [probability for outcome, probability in self.items() if probability < item]
        )

    def __gt__(self, item: Comparable):
        if isinstance(item, RandomVariable):
            return sum(
                probability1 * probability2
                for outcome1, probability1 in self.items()
                for outcome2, probability2 in item.items()
                if outcome1 > outcome2
            )

        return sum(
            [probability for outcome, probability in self.items() if probability > item]
        )

    def cdf(self):
        return CumulativeDistribution(self)

    def __repr__(self) -> str:
        """Render component map as a table"""
        table = tabulate(
            self.items(),
            headers=("Outcomes", "Probabilities"),
            tablefmt="fancy_grid",
        )

        return f"{self.__class__.__name__}:\n{table}"
