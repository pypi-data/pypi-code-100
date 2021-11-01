from typing import Tuple

import functools
import jax
import jax.numpy as jnp
import flax.linen as nn
from flax import optim
from jax.experimental.optimizers import clip_grads

from jaxdl.utils.commons import InfoDict, PRNGKey, TrainState
from jaxdl.rl.utils.replay_buffer import Batch


@functools.partial(jax.jit, static_argnames=('discount'))
def get_td_target(rng: PRNGKey, target_actor_net: TrainState,
  critic_target_net: TrainState, batch: Batch, discount: float
  ) -> Tuple[PRNGKey, jnp.ndarray]:
  rng, key = jax.random.split(rng)

  # call actor
  policy_dist, _, _ = target_actor_net.apply_fn(
    target_actor_net.params, batch.observations)
  next_actions = policy_dist.sample(seed=key)

  # call critic
  q1, q2 = critic_target_net.apply_fn(
    critic_target_net.params, batch.observations, jnp.tanh(next_actions))

  # soft update
  next_q = jnp.minimum(q1, q2)
  target_q = batch.rewards + discount * batch.masks * next_q
  return rng, target_q


@jax.jit
def critic_step(critic_net: TrainState, batch: Batch,
  target_q: jnp.ndarray) -> Tuple[TrainState, InfoDict]:
  """
  The critic is optimized the same way as typical actor critic methods,
  minimizing the TD error.
  """
  def loss_fn(critic_params, batch):
    q1, q2 = critic_net.apply_fn(
      critic_params, batch.observations, batch.actions)
    critic_loss = ((q1 - target_q)**2 + (q2 - target_q)**2).mean()
    return critic_loss, {'critic_loss': critic_loss}

  loss_info, grads = jax.value_and_grad(loss_fn, has_aux=True)(
    critic_net.params, batch)

  # TODO: arb. param.
  grads = clip_grads(grads, 40.0)
  new_critic_net = critic_net.apply_gradients(grads=grads)
  return new_critic_net, loss_info[1]