import typing
from typing import Any, Optional

from gym.spaces import Box, Dict, Discrete, MultiBinary, MultiDiscrete, Space, Tuple

# internal
from power_cogs.rl.agent import Agent


class GymAgent(Agent):
    def __init__(self):
        super(GymAgent, self).__init__()

    def preprocess_observation_func(self, obs: Any) -> Any:
        return obs

    def policy(self, obs: Any) -> typing.Dict[str, Any]:
        """Outputs action probabilities, in addition to other optional params.

        Example:
            {action_probs:np.array([0.1,0.2,0.3])}

        Returns:
            typing.Dict[str, Any]: output
        """
        return None

    def _policy(self, obs: Any) -> typing.Dict[str, Any]:
        preprocessed_obs = self.preprocess_observation_func(obs)
        return self.policy(preprocessed_obs)

    def act_default(self, policy_out: typing.Dict[str, Any]) -> Any:
        return None

    def act_box(self, policy_out: typing.Dict[str, Any], action_space: Box) -> Any:
        raise NotImplementedError("act_box method not implemented")

    def act_dict(self, policy_out: typing.Dict[str, Any], action_space: Dict) -> Any:
        raise NotImplementedError("act_dict method not implemented")

    def act_discrete(
        self, policy_out: typing.Dict[str, Any], action_space: Discrete
    ) -> Any:
        raise NotImplementedError("act_box method not implemented")

    def act_multi_binary(
        self, policy_out: typing.Dict[str, Any], action_space: MultiBinary
    ) -> Any:
        raise NotImplementedError("act_multi_binary method not implemented")

    def act_multi_discrete(
        self, policy_out: typing.Dict[str, Any], action_space: MultiDiscrete
    ) -> Any:
        raise NotImplementedError("act_multi_discrete method not implemented")

    def act_tuple(self, policy_out: typing.Dict[str, Any], action_space: Tuple) -> Any:
        raise NotImplementedError("act_tuple method not implemented")

    def act(self, obs: Any, action_space: Optional[Space] = None) -> Any:
        # change this to cases in 3.9 ya moron
        """Outputs a dict containing action to be passed into env.step, and optional params from the output of policy

        Example:
            {action:np.array([1,2,3,4]), optional_param:2}

        Args:
            obs (Any): obs from env
            action_space (Space): action_space from env

        Returns:
            action: Any
            policy_out: typing.Dict[str, Any]
        """
        policy_out = self._policy(obs)

        if policy_out is None:
            return action_space.sample(), policy_out

        if isinstance(action_space, Box):
            return self.act_box(policy_out, action_space), policy_out
        if isinstance(action_space, Dict):
            return self.act_dict(policy_out, action_space), policy_out
        if isinstance(action_space, Discrete):
            return self.act_discrete(policy_out, action_space), policy_out
        if isinstance(action_space, MultiBinary):
            return self.act_multi_binary(policy_out, action_space), policy_out
        if isinstance(action_space, MultiDiscrete):
            return self.act_multi_discrete(policy_out, action_space), policy_out
        if isinstance(action_space, Tuple):
            return self.act_tuple(policy_out, action_space), policy_out

        return self.act_default(policy_out), policy_out
