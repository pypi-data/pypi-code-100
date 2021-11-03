from collections import Callable, MutableMapping
from numbers import Number
from typing import Any, Dict, Iterable, List, Tuple, Union

from posterior.random_variables import Outcome, Probability, RandomVariable

Hypothesis = Union[str, float, int]

Likelihood = Union[
    Dict[Hypothesis, Dict[Outcome, Probability]],
    Dict[Hypothesis, Any],
    Callable[[Hypothesis, Outcome], Probability],
]


def flatten_dict(
    dictionary: MutableMapping,
    parent_key: Union[bool, str] = False,
    separator: str = ".",
) -> dict:
    """
    Turns a nested dictionary into a flattened dictionary
    """

    items: List[Tuple[str, Any]] = []

    for key, value in dictionary.items():
        new_key = str(parent_key) + separator + key if parent_key else key

        if isinstance(value, MutableMapping):
            items.extend(flatten_dict(value, new_key, separator).items())
        elif isinstance(value, list):
            for k, v in enumerate(value):
                items.extend(flatten_dict({str(k): v}, new_key).items())
        else:
            items.append((new_key, value))

    return dict(items)


class Hypotheses(RandomVariable[Hypothesis, Probability]):
    def __init__(self, *args, likelihood: Likelihood, **kwargs):
        super().__init__(*args, **kwargs)

        if callable(likelihood):
            self.likelihood = likelihood
            return

        # if likelihood is dict
        self.likelihood = {
            hypo: flatten_dict(outcomes) for hypo, outcomes in likelihood.items()
        }

    def evaluate(self, new_data: Union[Outcome, Iterable[Outcome]]):
        """
        Considers evidence of new data to update believes about hypothesis
        """
        if isinstance(new_data, (Number, str)):
            new_data = [new_data]

        for data in new_data:
            for hypothesis, probability in self.items():
                self[hypothesis] = probability * self.get_likelihood(hypothesis, data)

        self.normalize()

    def get_likelihood(
        self, hypothesis: Hypothesis, new_outcome: Outcome
    ) -> Probability:
        """
        Computes likelihood of a hypothesis given evidence of the data
        """
        if callable(self.likelihood):
            return self.likelihood(hypothesis, new_outcome)

        return self._get_likelihood_from_dict(hypothesis, new_outcome)

    def _get_likelihood_from_dict(
        self, hypothesis: Hypothesis, new_outcome: Outcome
    ) -> Probability:
        hypothesis = self.likelihood.get(hypothesis, None)

        if not hypothesis:
            raise ValueError()

        probability = hypothesis.get(new_outcome, None)

        if probability is None:
            raise ValueError()

        return probability
