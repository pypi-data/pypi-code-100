from collections import deque
from typing import List, Union

import gym
import numpy as np
from gym.spaces import Discrete
from pydantic.dataclasses import dataclass

# internal
from power_cogs.base import Base
from power_cogs.cluster.cluster import Cluster
from power_cogs.config import Config
from power_cogs.config.config import class_config
from power_cogs.rl.gym.gym_agent import GymAgent
from power_cogs.rl.gym.gym_rollout_execution import GymRolloutExecution
from power_cogs.rl.rollout import Rollout, RolloutSet


@dataclass
class ReplayBufferConfig(Config):
    env_name: str = "LunarLander-v2"
    max_env_steps: int = 10 ** 10
    gamma: float = 0.99
    discount_rewards: bool = True
    normalize_rewards: bool = False
    num_workers: int = 5
    max_replay_size: int = 10000
    sample_len: int = 10 ** 10


@class_config(ReplayBufferConfig)
class ReplayBuffer(Base):
    def __init__(self, config={}):
        self.config = config
        self.env_name = config.get("env_name")
        self.max_env_steps = config.get("max_env_steps")
        self.gamma = config.get("gamma")
        self.discount_rewards = config.get("discount_rewards")
        self.normalize_rewards = config.get("normalize_rewards")
        self.num_workers = config.get("num_workers")
        self.max_replay_size = config.get("max_replay_size")
        self.sample_len = config.get("sample_len")

        self.rollout_workers = None

        self.rollouts: List[Rollout] = deque([], maxlen=self.max_replay_size)

    def setup_rollout_workers(
        self, cluster: Cluster, observation_wrapper=None, action_wrapper=None
    ):
        self.rollout_workers = [
            cluster.create_execution(
                GymRolloutExecution,
                env_name=self.env_name,
                max_env_steps=self.max_env_steps,
                stop_criteria=self.stop_criteria,
                observation_wrapper=observation_wrapper,
                action_wrapper=action_wrapper,
            )
            for i in range(self.num_workers)
        ]

    def append(self, rollouts: Union[Rollout, List[Rollout], RolloutSet]):
        if isinstance(rollouts, Rollout):
            self.rollouts.append(rollouts)
        elif isinstance(rollouts, RolloutSet):
            for r in rollouts.rollouts:
                self.rollouts.append(r)
        else:
            for r in rollouts:
                self.rollouts.append(r)

    def sample(self, num_samples: int, replacement: bool = True) -> RolloutSet:
        if replacement:
            random_indices = np.random.randint(0, len(self.rollouts), num_samples)
        else:
            random_indices = np.random.choice(0, len(self.rollouts), num_samples)

        rollouts = [self.rollouts[i] for i in random_indices]
        start_idx = 0
        end_idx = 10 ** 10
        for i in range(len(rollouts)):
            if len(rollouts[i]) - self.sample_len > 0:
                start_idx = np.random.randint(len(rollouts[0]) - self.sample_len)
                end_idx = start_idx + self.sample_len
            rollouts[i] = Rollout(*rollouts[i][start_idx:end_idx])

        return RolloutSet(rollouts)

    def get_env_dims(self):
        # env_type = getattr(env, "env_type", "default")
        env = gym.make(self.env_name)
        state_shape = env.observation_space.shape
        if isinstance(env.action_space, Discrete):
            action_shape = [env.action_space.n]
        else:
            action_shape = env.action_space.shape
        return state_shape, action_shape

    def stop_criteria(self, observation, reward, done, info):
        return False

    def discount_reward(self, rews):
        # dr = [0] * (len(reward_arr) + 1)
        # for i in range(len(reward_arr) - 1, -1, -1):
        #     dr[i] = reward_arr[i] + self.gamma * dr[i + 1]
        # dr = np.array(dr[: len(reward_arr)])
        # return dr
        n = len(rews)
        rtgs = np.zeros_like(rews)
        for i in reversed(range(n)):
            rtgs[i] = rews[i] + (rtgs[i + 1] if i + 1 < n else 0)
        return rtgs

    def get_rollout(
        self,
        cluster: Cluster,
        agent: GymAgent = None,
        observation_wrapper=None,
        action_wrapper=None,
        num_rollouts: int = 32,
        render: bool = False,
    ) -> RolloutSet:
        if self.rollout_workers is None:
            self.setup_rollout_workers(observation_wrapper, action_wrapper)
        rollout_args = [{"agent": agent, "render": render} for i in range(num_rollouts)]
        rollouts = RolloutSet(cluster.execute_list(self.rollout_workers, rollout_args))
        return rollouts

    def rollout(
        self,
        cluster: Cluster,
        agent: GymAgent = None,
        observation_wrapper=None,
        action_wrapper=None,
        num_rollouts: int = 32,
        render: bool = False,
    ) -> RolloutSet:
        rollouts = self.get_rollout(
            cluster, agent, observation_wrapper, action_wrapper, num_rollouts, render
        )
        self.append(rollouts)
        return rollouts

    def __len__(self):
        return len(self.rollouts)
