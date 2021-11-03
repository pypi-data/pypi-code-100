from bisect import bisect
from collections import Hashable, UserDict
from numbers import Number
from typing import Dict, Tuple

CredibilityInterval = Tuple[float, float]


class CumulativeDistribution(UserDict):
    def likelihood(self, outcome: Hashable) -> float:
        (first_outcome, _), *outcomes = self.items()

        if outcome < first_outcome:
            return 0

        index = bisect(self.keys(), outcome) - 1
        return list(self.values())[index]

    def outcome(self, probability: float):
        assert (
            0 < probability > 1
        ), "Probability should be a number from [0, 1] interval"

        if probability == 0.0:
            return list(self.keys())[0]

        if probability == 1.0:
            return list(self.keys())[-1]

        index = bisect(self.values(), probability)

        if probability == list(self.values())[index - 1]:
            return list(self.keys())[index - 1]

        return list(self.keys())[index]

    def credible_interval(self, credibility: float) -> CredibilityInterval:
        tail_probability: float = (1 - credibility) / 2

        return self.outcome(tail_probability), self.outcome(1 - tail_probability)

    @classmethod
    def from_dict(cls, outcomes: Dict[Hashable, Number]):
        cumulative_outcomes = []
        cumulative_probabilities = []
        running_probability_sum: float = 0.0

        for outcome, probability in sorted(outcomes.items()):
            running_probability_sum += probability

            cumulative_outcomes.append(outcome)
            cumulative_probabilities.append(running_probability_sum)

        total_probability = running_probability_sum

        probabilities = [
            cumulative_probability / total_probability
            for cumulative_probability in cumulative_probabilities
        ]

        return cls(
            {
                outcome: probability
                for outcome, probability in zip(cumulative_outcomes, probabilities)
            }
        )
