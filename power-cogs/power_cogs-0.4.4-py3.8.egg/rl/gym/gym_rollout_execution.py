from __future__ import annotations

import time
import typing
from typing import Callable, Optional

import attr
import gym
import numpy as np
import torch

# internal
from power_cogs.rl.gym.gym_agent import GymAgent
from power_cogs.rl.rollout_execution import Rollout, RolloutExecution


@attr.s(repr=False)
class GymRolloutExecution(RolloutExecution):
    env: Optional[gym.Env] = attr.ib(default=None)
    env_name: str = attr.ib(default="LunarLander-v2")
    env_creation: Optional[Callable] = attr.ib(default=None)
    max_env_steps: int = attr.ib(default=10 ** 10)
    stop_criteria: Optional[Callable] = attr.ib(default=None)
    observation_wrapper: Optional[Callable] = attr.ib(default=None)
    action_wrapper: Optional[Callable] = attr.ib(default=None)

    def __attrs_post_init__(self):
        if self.env is None:
            if self.env_creation is not None:
                self.env = self.env_creation()
            else:
                self.env = gym.make(self.env_name)
            if self.observation_wrapper is not None:
                self.env = self.observation_wrapper(self.env)
            if self.action_wrapper is not None:
                self.env = self.action_wrapper(self.env)

    def rollout(
        self, agent: GymAgent = None, render: bool = False, close: bool = False
    ) -> typing.Tuple[np.array, np.array, np.array]:
        """Evaluates  env and model until the env returns "Done".
        Returns:
            xs: A list of observations
            hs: A list of model hidden states per observation
            dlogps: A list of gradients
            drs: A list of rewards.
        """
        if agent is None:
            agent = GymAgent()  # random actions
        with torch.no_grad():
            # Reset the game.
            observation = self.env.reset()
            observations, actions, rewards, dones, rendered_obs = [], [], [], [], []
            done = False
            i = 0
            while not done:
                rendered = None
                if render:
                    rendered = self.env.render(mode="rgb_array")
                    time.sleep(0.01)
                if agent is None:
                    action = self.env.action_space.sample()
                else:
                    action, policy_out = agent.act(observation, self.env.action_space)

                actions.append(action)
                observations.append(observation)
                rendered_obs.append(rendered)
                observation, reward, done, info = self.env.step(action)
                rewards.append(reward)
                dones.append(float(done))
                i += 1
                if i >= self.max_env_steps:
                    done = True
                elif self.stop_criteria is not None:
                    if self.stop_criteria(observation, reward, done, info):
                        done = True

            observations = np.array(observations)
            rendered_obs = np.array(rendered_obs)
            actions = np.array(actions)
            rewards = np.array(rewards)
            dones = np.array(dones)

            if close:
                self.env.close()

            rollout = Rollout(
                observations=observations,
                actions=actions,
                rewards=rewards,
                dones=dones,
                rendered_obs=rendered_obs,
            )
            if getattr(self.env.action_space, "n"):
                rollout.set_categorical_actions(self.env.action_space.n)

            return rollout
