from dataclasses import field
from typing import Any, List, Optional

import numpy as np
import torch
import torch.nn.functional as F
from pydantic.dataclasses import dataclass

from power_cogs.config.config import class_config

# internal
from power_cogs.rl.gym.torch_gym_agent import TorchGymAgent, TorchGymAgentConfig
from power_cogs.utils.torch_utils import create_linear_network


@dataclass
class MLPAgentConfig(TorchGymAgentConfig):
    hidden_dims: List[int] = field(default_factory=lambda: [32])
    use_normal_init: bool = True
    normal_std: float = 0.01
    zero_bias: bool = False
    output_activation: Optional[str] = None


@class_config(MLPAgentConfig)
class MLPAgent(TorchGymAgent):
    def __init__(self, config: Any = {}):
        super(MLPAgent, self).__init__(config)
        self.hidden_dims = self.config.get("hidden_dims")
        self.use_normal_init = self.config.get("use_normal_init")
        self.normal_std = self.config.get("normal_std")
        self.zero_bias = self.config.get("zero_bias")
        self.output_dims = self.action_shape[0]
        self.input_dims = np.prod(self.observation_shape)

        output_activation = self.config.get("output_activation")
        self.output_activation = output_activation
        if output_activation is not None:
            self.output_activation = eval(output_activation)
        self.net = create_linear_network(
            self.input_dims, self.hidden_dims, self.output_dims
        )

        def init_weights(m):
            if isinstance(m, torch.nn.Linear):
                torch.nn.init.normal_(m.weight, std=self.normal_std)
                if getattr(m, "bias", None) is not None:
                    if self.zero_bias:
                        torch.nn.init.zeros_(m.bias)
                    else:
                        torch.nn.init.normal_(m.bias, std=self.normal_std)

        if self.use_normal_init:
            with torch.no_grad():
                self.apply(init_weights)

    def forward(self, x):
        x = self.net(x)
        x = F.softmax(x, dim=-1)
        return x

    def policy(self, obs):
        return {"action_probs": self.forward(obs)}
