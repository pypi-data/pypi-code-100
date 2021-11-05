import typing
from dataclasses import astuple
from typing import Any, List, Optional, Tuple

import numpy as np

# import numpy.typing as npt
from pydantic.dataclasses import dataclass


def merge_numpy(set_):
    set_len = len(set_[0])
    rollout_list = []
    for i in range(set_len):
        stacked = np.stack([np.array(subset[i]) for subset in set_])
        rollout_list.append(stacked)
    return rollout_list


@dataclass
class Rollout:
    observations: Any
    actions: Any
    rewards: Any
    dones: Any
    categorical_actions: Optional[Any] = None
    rendered_obs: Optional[Any] = None

    def __post_init_post_parse__(self):
        nones = [None for _ in range(len(self.observations))]
        self.categorical_actions = np.array(nones)

    def set_categorical_actions(self, num_classes: int) -> None:
        zeros = np.zeros((self.actions.shape[0], num_classes))
        for i in range(zeros.shape[0]):
            zeros[i][self.actions[i]] = 1
        self.categorical_actions = zeros

    def __getitem__(self, i: int):
        return (
            self.observations[i],
            self.actions[i],
            self.rewards[i],
            self.dones[i],
            self.categorical_actions[i],
            self.rendered_obs[i],
        )

    def __len__(self) -> int:
        return len(self.observations)

    def astuple(self) -> Tuple[Any]:
        return astuple(self)


@dataclass
class RolloutSet:
    rollouts: List[Rollout]
    numpy_rollouts: typing.Any = None

    def numpy(self) -> Tuple[Any]:
        if self.numpy_rollouts is None:
            tuples = [rollout.astuple() for rollout in self.rollouts]
            self.numpy_rollouts = merge_numpy(tuples)
        return self.numpy_rollouts
