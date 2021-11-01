from typing import Optional, Sequence, Tuple

import jax
import time
import optax
import numpy as np
import jax.numpy as jnp
import functools
import flax.linen as nn

from jaxdl.rl.utils.commons import RLAgent
from jaxdl.rl.utils.replay_buffer import Batch
from jaxdl.utils.commons import Module, save_train_state, restore_train_state
from jaxdl.utils.commons import create_train_state
from jaxdl.rl.networks.actor_nets import create_normal_dist_policy_fn
from jaxdl.rl.networks.critic_nets import create_double_critic_network_fn
from jaxdl.rl.networks.constant_nets import create_constant_network_fn
from jaxdl.rl.agents.mpo.utils import update_target
from jaxdl.rl.agents.mpo.critic_fns import critic_step, get_td_target
from jaxdl.rl.agents.mpo.step_fns import e_step, m_step
from jaxdl.utils.commons import PRNGKey, Module, TrainState


@functools.partial(jax.jit)
def sample_actions(
  rng: PRNGKey,
  actor_net: TrainState,
  observations: np.ndarray,
  temperature: float = 1.0) -> Tuple[PRNGKey, jnp.ndarray]:
  dist, _, _ = actor_net.apply_fn(actor_net.params, observations, temperature)
  rng, key = jax.random.split(rng)
  return rng, dist.sample(seed=key)

class MPOAgent(RLAgent):
  def __init__(self,
    seed: int,
    observations: jnp.ndarray,
    actions: jnp.ndarray,
    actor_net_fn: Module = create_normal_dist_policy_fn,
    critic_net_fn: Module = create_double_critic_network_fn,
    discount: float = 0.99,
    actor_lr: float = 3e-4,
    critic_lr: float = 3e-4,
    mu_lr: float = 3e-4,
    std_lr: float = 3e-4,
    eps_eta: float = 0.1,
    eps_mu: float = 5e-4,
    eps_std: float = 1e-5,
    replay_buffer_size: int = 250,
    target_update_period: int = 250):

    self.rng = jax.random.PRNGKey(seed)
    self.rng, actor_key, critic_key, mu_key, std_key = jax.random.split(
      self.rng, 5)
    action_dim = actions.shape[-1]

    # actor networks
    actor_net = create_train_state(
      actor_net_fn(action_dim=action_dim, tanh_squash_distribution=False,
        return_means_and_log_stds=True),
      [actor_key, observations], optax.adam(learning_rate=actor_lr))
    target_actor_net = create_train_state(
      actor_net_fn(action_dim=action_dim, tanh_squash_distribution=False,
        return_means_and_log_stds=True),
      [actor_key, observations], optax.adam(learning_rate=actor_lr))

    # critic networks
    critic_net = create_train_state(
      critic_net_fn(), [critic_key, observations, actions],
      optax.adam(learning_rate=critic_lr))
    target_critic_net = create_train_state(
      critic_net_fn(), [critic_key, observations, actions],
      optax.adam(learning_rate=critic_lr))

    mu_net = create_train_state(
      create_constant_network_fn(initial_value=100.), [mu_key],
      optax.adam(learning_rate=mu_lr))
    std_net = create_train_state(
      create_constant_network_fn(initial_value=1.), [std_key],
      optax.adam(learning_rate=std_lr))

    # networks
    self.actor_net = actor_net
    self.target_actor_net = target_actor_net
    self.critic_net = critic_net
    self.target_critic_net = target_critic_net
    self.mu_net = mu_net
    self.std_net = std_net

    # parameters
    self.temp = 1.
    self.eps_eta = eps_eta
    self.eps_mu = eps_mu
    self.eps_std = eps_std
    self.discount = discount
    self.replay_buffer_size = replay_buffer_size
    self.action_dim = action_dim
    self.target_update_period = target_update_period
    self.step_num = 1

  def sample(
    self, observations: np.ndarray, temperature: float = 1.) -> np.ndarray:
    self.rng, actions = sample_actions(
      self.rng, self.actor_net, observations, temperature)
    actions = np.asarray(nn.tanh(actions))
    return np.clip(actions, -1, 1)

  def update(self, batch: Batch, action_sample_size: int = 20):
    self.step_num += 1

    # update cirtic
    self.rng, target_q = get_td_target(self.rng, self.target_actor_net,
      self.target_critic_net, batch, self.discount)
    self.critic_net, critic_info = critic_step(self.critic_net, batch, target_q)

    # start_time = time.time()
    # evaluation step
    self.rng, self.temp, temp_loss, weights, sampled_actions, states_repeated = e_step(
      self.rng, self.target_actor_net, self.target_critic_net, self.action_dim,
      self.temp, self.eps_eta, batch, action_sample_size)
    # print(f"The E-Step took {time.time() - start_time}")

    # maximization step
    # start_time = time.time()
    self.actor_net, self.mu_net, self.std_net, actor_info = m_step(
      self.actor_net, self.target_actor_net, self.std_net, self.mu_net,
      self.eps_mu, self.eps_std, batch, weights, sampled_actions,
      states_repeated, temp_loss)
    # print(f"The M-Step took {time.time() - start_time}")

    # update target networks
    if self.step_num % self.target_update_period == 0:
      self.target_actor_net = update_target(self.actor_net, self.target_actor_net, 1.)
      self.target_critic_net = update_target(self.critic_net, self.target_critic_net, 1.)

    return {'eta' : self.temp, **critic_info, **actor_info}

  def restore(self, path):
    """Loads the networks of the agents."""
    self.actor_net = restore_train_state(self.actor_net, path, prefix="actor")
    self.critic_net = restore_train_state(self.critic_net, path, prefix="critic")
    self.target_critic_net = restore_train_state(
      self.target_critic_net, path, prefix="target_critic")
    self.target_actor_net = restore_train_state(
      self.target_actor_net, path, prefix="target_actor")
    self.mu_net = restore_train_state(self.mu_net, path, prefix="mu")
    self.std_net = restore_train_state(self.std_net, path, prefix="std")

  def save(self, path):
    """Saves the networks of the agents."""
    save_train_state(self.actor_net, path, prefix="actor")
    save_train_state(self.critic_net, path, prefix="critic")
    save_train_state(self.target_critic_net, path, prefix="target_critic")
    save_train_state(self.target_actor_net, path, prefix="target_actor")
    save_train_state(self.mu_net, path, prefix="mu")
    save_train_state(self.mu_net, path, prefix="std")