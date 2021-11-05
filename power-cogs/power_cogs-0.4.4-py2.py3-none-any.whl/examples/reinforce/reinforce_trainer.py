from typing import Any

import hydra.utils
import numpy as np
import torch
from einops import rearrange
from pydantic.dataclasses import dataclass
from torch.distributions.categorical import Categorical

# internal
from power_cogs.base.torch.base_torch_trainer import BaseTorchTrainer
from power_cogs.callbacks import after, setup_callback  # noqa
from power_cogs.config.config import class_config
from power_cogs.config.trainer_config import TorchTrainerConfig
from power_cogs.examples.reinforce.mlp_agent import MLPAgent, MLPAgentConfig
from power_cogs.rl.replay_buffer import ReplayBuffer, ReplayBufferConfig


@dataclass
class ReinforceTrainerConfig(TorchTrainerConfig):
    agent_config: Any = MLPAgentConfig()
    replay_config: Any = ReplayBufferConfig()
    norm_gradient: bool = False
    video_log_interval: int = 100


@class_config(ReinforceTrainerConfig)
class ReinforceTrainer(BaseTorchTrainer):
    def __init__(self, config):
        super(ReinforceTrainer, self).__init__(config)

    def setup(self):
        self.replay_config = self.config.get("replay_config")
        self.agent_config = self.config.get("agent_config")
        self.optimizer_config = self.config.get("optimizer_config")
        self.scheduler_config = self.config.get("scheduler_config")
        self.norm_gradient = self.config.get("norm_gradient")
        self.video_log_interval = self.config.get("video_log_interval")

        self.replay_buffer = ReplayBuffer(self.replay_config)

        self.state_shape, self.action_shape = self.replay_buffer.get_env_dims()
        self.agent_config["observation_shape"] = self.state_shape
        self.agent_config["action_shape"] = self.action_shape
        self.gamma = self.replay_buffer.gamma

        self.model = MLPAgent(self.agent_config)
        print(self.model)
        self.optimizer = hydra.utils.instantiate(
            self.optimizer_config, params=self.model.parameters()
        )
        self.scheduler = hydra.utils.instantiate(
            self.scheduler_config, optimizer=self.optimizer
        )

    def setup_rollout_workers(self):
        self.replay_buffer.setup_rollout_workers(self.cluster)
        self.replay_buffer.rollout(self.cluster)

    def pre_train(self):
        self.setup_rollout_workers()

    def emit_metrics(self, out, step=0):
        metrics = out["metrics"]
        for key in metrics:
            self.logger.tensorboard_writer.add_scalar(key, metrics[key], step)
        if step % self.video_log_interval == 0:
            rollout = self.replay_buffer.get_rollout(
                self.cluster, self.model, num_rollouts=1, render=True
            )
            _, _, _, _, _, rendered_obs = rollout.numpy()

            self.logger.tensorboard_writer.add_video(
                "rollout_video",
                rearrange(rendered_obs, "b t h w c -> b t c h w"),
                global_step=step,
                fps=32,
            )

    def train_iter(self, batch_size: int = 32, epoch: int = 0):
        losses = []
        self.replay_buffer.rollout(self.cluster, self.model, num_rollouts=batch_size)
        rollout_set = self.replay_buffer.sample(batch_size)

        total_rewards = []

        for rollout in rollout_set.rollouts:
            (
                observations,
                actions,
                rewards,
                dones,
                categorical_actions,
                rendered_obs,
            ) = rollout.astuple()

            rewards = np.squeeze(rewards)
            total_rewards.append(np.sum(rewards))
            if self.replay_buffer.discount_rewards:
                rewards = self.replay_buffer.discount_reward(rewards)
            if self.replay_buffer.normalize_rewards:
                rewards = rewards - np.mean(rewards)
                rewards = rewards / (np.std(rewards) + 1e-10)
            observations = torch.from_numpy(observations).float()
            actions = torch.from_numpy(actions).float()
            rewards = torch.from_numpy(rewards).float()

            self.optimizer.zero_grad()

            out = self.model.policy(observations)
            logits = out["action_probs"]
            dist = Categorical(logits)
            log_probs = dist.log_prob(actions)

            loss = -1 * torch.sum(rewards * log_probs)

            if self.norm_gradient:
                for p in self.model.parameters():
                    if p.grad is not None:
                        p.grad /= torch.norm(p.grad) + 1e-10

            loss.backward()
            self.optimizer.step()
            # self.scheduler.step()
            losses.append(loss.item())

        grad_dict = {}
        for n, W in self.model.named_parameters():
            if W.grad is not None:
                grad_dict["{}_grad".format(n)] = float(torch.sum(W.grad).item())
        train_dict = {
            "out": None,
            "metrics": {
                "average_summed_rewards": np.mean(total_rewards),
                "max_summed_rewards": np.max(total_rewards),
                "loss": np.mean(losses),
                "max_loss": np.max(losses),
                "sum_loss": np.sum(losses),
                "epoch": epoch,
                **grad_dict,
            },
            "loss": np.mean(losses),
        }
        return train_dict
