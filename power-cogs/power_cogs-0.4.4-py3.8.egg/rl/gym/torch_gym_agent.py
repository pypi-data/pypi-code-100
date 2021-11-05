import typing
from contextlib import contextmanager
from typing import Any

import torch
from gym.spaces import (  # noqa
    Box,
    Dict,
    Discrete,
    MultiBinary,
    MultiDiscrete,
    Space,
    Tuple,
)
from pydantic.dataclasses import dataclass
from torch.distributions.categorical import Categorical

# internal
from power_cogs.config import Config
from power_cogs.config.config import class_config
from power_cogs.rl.gym.gym_agent import GymAgent


@dataclass
class TorchGymAgentConfig(Config):
    observation_shape: Any = None
    action_shape: Any = None


@class_config(TorchGymAgentConfig)
class TorchGymAgent(GymAgent, torch.nn.Module):
    def __init__(self, config: Any):
        super(TorchGymAgent, self).__init__()
        self.config = config
        self.observation_shape = self.config.get("observation_shape")
        self.action_shape = self.config.get("action_shape")

    def preprocess_observation_func(self, observation):
        return torch.from_numpy(observation).unsqueeze(0).float()

    def act_discrete(
        self, policy_out: typing.Dict[str, Any], action_space: Discrete
    ) -> int:
        action_logits = policy_out.get("action_logits", None)
        action_probs = policy_out.get("action_probs", None)
        if action_logits is not None:
            dist = Categorical(logits=action_logits)
        else:
            dist = Categorical(probs=action_probs)
        return dist.sample().item()

    @contextmanager
    def evaluate(self):
        with torch.no_grad():
            try:
                yield
            finally:
                pass
