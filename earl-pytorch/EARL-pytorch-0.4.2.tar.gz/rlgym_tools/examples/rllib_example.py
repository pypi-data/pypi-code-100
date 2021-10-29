import logging
import os

import numpy as np
import ray
from gym.spaces import Box
from ray.rllib.agents.ppo import PPOTorchPolicy, PPOTrainer
from ray.tune import register_env, tune

from rlgym.envs import Match
from rlgym.gym import Gym
from rlgym.utils.obs_builders import AdvancedObs
from rlgym.utils.reward_functions.common_rewards import VelocityReward
from rlgym.utils.state_setters import DefaultState
from rlgym.utils.terminal_conditions.common_conditions import TimeoutCondition, GoalScoredCondition
from rlgym_tools.rllib_utils import RLLibEnv

if __name__ == '__main__':
    # ray.init(namespace="rlgym", logging_level=logging.DEBUG)
    ray.init(address='127.0.0.1:6379', _redis_password='5241590000000000', logging_level=logging.DEBUG)
    # ray.init(address='ray://127.0.0.1:6379')
    # tune.run(PPOTrainer, config={"env": "CartPole-v0", "num_workers": 2, "num_cpus_per_worker": 1,
    #                              "num_envs_per_worker": 1})  # "log_level": "INFO" for verbose,
    # "framework": "tfe"/"tf2" for eager,
    # "framework": "torch" for PyTorch
    # exit(0)
    # ray.init(logging_level=logging.DEBUG, memory=4e9, object_store_memory=4e9)

    # ray start --head --port=6379 --ray-client-server-port=6968 --gcs-server-port=6969 --dashboard-port=8265
    # docker run --shm-size=4.07gb -i -p 6379:6379 -p 8265:8265 -p 6969:6969 -p 6968:6968 b926c8b4c92b

    rl_path = r"C:\Program Files\Epic Games\rocketleague\Binaries\Win64\RocketLeague.exe"


    def create_env(env_config):
        env = Gym(
            match=Match(
                self_play=True,
                obs_builder=AdvancedObs(),
                reward_function=VelocityReward(negative=True),
                state_setter=DefaultState(),
                terminal_conditions=[TimeoutCondition(15 * 120 // 8), GoalScoredCondition()]
            ),
            pipe_id=os.getpid(),
            path_to_rl=rl_path,
            use_injector=True
        )
        return RLLibEnv(env)


    register_env("RLGym", create_env)

    policy = PPOTorchPolicy, Box(-np.inf, np.inf, (107,)), Box(-1.0, 1.0, (8,)), {}
    # policy = PPOTorchPolicy, Box(-np.inf, np.inf, (4,)), Discrete(2), {}

    tune.run(
        PPOTrainer,
        config={
            "env": "RLGym",  # "CartPole-v0",
            "multiagent": {
                "policies": {"ppo_policy": policy},
                "policy_mapping_fn": (lambda agent_id, **kwargs: "ppo_policy"),
                "policies_to_train": ["ppo_policy"],
            },
            # "env_config": {
            #     "num_agents": 2
            # },
            "model": {
                "vf_share_layers": True,
            },
            # Use GPUs iff `RLLIB_NUM_GPUS` env var set to > 0.
            # "num_gpus": int(os.environ.get("RLLIB_NUM_GPUS", "0")),
            "num_workers": 1,
            "num_cpus_per_worker": 1,
            "num_envs_per_worker": 1,
            "remote_worker_envs": True,
            "sample_async": True,
            "framework": "torch"
        },
    )

    # for i in range(1000000):
    #     print("== Iteration", i, "==")
    #
    #     # improve the PPO policy
    #     print("-- PPO --")
    #     result_ppo = ppo_trainer.train()
    #     print(pretty_print(result_ppo))
    # print("Done training")

    # # This does not work for some reason
    # tune.run(
    #     "PPO",
    #     config={
    #         "env": MultiAgentCartPole,
    #         "env_config": {
    #             "num_agents": 2
    #         },
    #         "multiagent": {
    #             "policies": {"ppo_policy": policy},
    #             "policy_mapping_fn": (lambda agent_id, **kwargs: "ppo_policy"),
    #             "policies_to_train": ["ppo_policy"],
    #         },
    #         "model": {
    #             "vf_share_layers": True,
    #         },
    #         # Use GPUs iff `RLLIB_NUM_GPUS` env var set to > 0.
    #         "num_gpus": int(os.environ.get("RLLIB_NUM_GPUS", "0")),
    #         "num_workers": 2,
    #         "num_cpus_per_worker": 1,
    #         "num_workers_per_env": 2,
    #         "remote_worker_envs": True,
    #         "sample_async": True,
    #         "framework": "torch"
    #     }
    # )
