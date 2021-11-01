from typing import Tuple

import functools
import jax
import jax.numpy as jnp

import flax.linen as nn
from flax import optim
from jax import random
from jax.experimental.optimizers import clip_grads
from scipy.optimize import minimize
from jax.scipy.special import logsumexp
from tensorflow_probability.substrates import jax as tfp
tfb = tfp.bijectors
tfd = tfp.distributions

from jaxdl.utils.commons import InfoDict, PRNGKey, TrainState
from jaxdl.rl.utils.replay_buffer import Batch
from jaxdl.utils.commons import InfoDict


@functools.partial(
  jax.jit, static_argnames=('action_sample_size', 'action_dim', 'batch_size'))
def sample_actions_and_evaluate(rng: PRNGKey, target_actor_net: TrainState,
  target_critic_net: TrainState, action_dim: int, batch: Batch, batch_size: int,
  action_sample_size: int) -> Tuple[PRNGKey, jnp.ndarray, jnp.ndarray, jnp.ndarray]:


  states_repeated = jnp.repeat(batch.observations, action_sample_size, axis=0)

  # TODO: can we use inbuilt jit sampling
  dist, mu, log_std = target_actor_net.apply_fn(
    target_actor_net.params, states_repeated)
  rng, key = jax.random.split(rng)
  sampled_actions = dist.sample(seed=key)

  sampled_actions = sampled_actions.reshape(
   (batch_size * action_sample_size, action_dim))
  sampled_actions = jax.lax.stop_gradient(sampled_actions)

  # evaluate each of the sampled actions at their corresponding state
  q1, q2 = target_critic_net.apply_fn(
    target_critic_net.params, states_repeated, jnp.tanh(sampled_actions))

  q = jnp.minimum(q1, q2)
  q = q.reshape((batch_size, action_sample_size))
  q = jax.lax.stop_gradient(q)
  return rng, q, sampled_actions, states_repeated

@jax.jit
def mu_lagrange_step(mu_net: TrainState,
  reg: float) -> Tuple[TrainState, InfoDict]:

  def loss_fn(mu_params):
    mu = mu_net.apply_fn(mu_params)
    loss = (mu * reg).mean()
    return loss, {'mu_loss': loss, 'mu': mu}

  loss_info, grads = jax.value_and_grad(loss_fn, has_aux=True)(
    mu_net.params)
  new_mu_net = mu_net.apply_gradients(grads=grads)
  return new_mu_net, loss_info[1]

@jax.jit
def std_lagrange_step(std_net: TrainState,
  reg: float) -> Tuple[TrainState, InfoDict]:
  def loss_fn(std_params):
    mu = std_net.apply_fn(std_params)
    loss = (mu * reg).mean()
    return loss, {'std_loss': loss, 'std': mu}

  loss_info, grads = jax.value_and_grad(loss_fn, has_aux=True)(
    std_net.params)
  new_mu_net = std_net.apply_gradients(grads=grads)
  return new_mu_net, loss_info[1]

# @functools.partial(jax.jit, static_argnames=('eps_eta'))
# def dual(q1: jnp.ndarray, eps_eta: float, temp: jnp.ndarray) -> float:
#   """
#   g(η) = η*ε + η \\mean \\log (\\mean \\exp(Q(a, s)/η))
#   """
#   out = temp * (
#     eps_eta + jnp.mean(logsumexp(q1 / temp, axis=1))
#   )
#   return out.sum()

def e_step(rng: PRNGKey, target_actor_net: TrainState,
  target_critic_net: TrainState, action_dim: int, temp: float, eps_eta: float,
  batch: Batch, action_sample_size: int
  ) -> Tuple[PRNGKey, float, jnp.ndarray, jnp.ndarray, jnp.ndarray, jnp.ndarray]:

  rng, q, sampled_actions, states_repeated = sample_actions_and_evaluate(
    rng, target_actor_net, target_critic_net, action_dim, batch,
    batch.observations.shape[0], action_sample_size)

  # jac = jax.grad(dual, argnums=2)
  # jac = functools.partial(jac, q1, eps_eta)

  # # use nonconvex optimizer to minimize the dual of the temperature parameter
  # # we have direct access to the jacobian function with jax so we can take
  # # advantage of it here
  # this_dual = functools.partial(dual, q1, eps_eta)
  # bounds = [(1e-6, None)]
  # res = minimize(this_dual, temp, jac=jac, method="SLSQP", bounds=bounds)
  # temp = jax.lax.stop_gradient(res.x)

  tempered_q_values = q / temp
  weights = jax.nn.softmax(tempered_q_values, axis=0)
  weights = jax.lax.stop_gradient(weights)

  q_log_sum_exp = logsumexp(tempered_q_values, axis=0)
  log_num_actions = jnp.log(q.shape[0])
  loss = eps_eta + (q_log_sum_exp).mean() - log_num_actions
  loss = temp * loss

  weights = weights.reshape(
    (batch.observations.shape[0] * action_sample_size))
  return rng, temp, weights, loss, sampled_actions, states_repeated


@functools.partial(jax.jit, static_argnames=('eps_mu', 'eps_std', 'alpha'))
def m_step(actor_net: TrainState, target_actor_net: TrainState,
  std_net: optim.Optimizer, mu_net: optim.Optimizer, eps_mu: float,
  eps_std: float, batch: Batch, weights: jnp.ndarray, sampled_actions: jnp.ndarray,
  states_repeated: jnp.ndarray, temp_loss: jnp.ndarray
  ) -> Tuple[TrainState, TrainState, TrainState, InfoDict]:

  @jax.jit
  def loss_fn(actor_params, mu_net, std_net):
    _, means, log_std = actor_net.apply_fn(
      actor_params, states_repeated)
    # target policy
    target_policy_dist, target_means, target_log_std = target_actor_net.apply_fn(
      target_actor_net.params, states_repeated)
    target_means = jax.lax.stop_gradient(target_means)
    target_log_std = jax.lax.stop_gradient(target_log_std)
    target_policy_dist = jax.lax.stop_gradient(target_policy_dist)

    # new policies
    dist_stds_k = tfd.MultivariateNormalDiag(
      loc=means, scale_diag=jnp.exp(target_log_std))
    dist_means_k = tfd.MultivariateNormalDiag(
      loc=target_means, scale_diag=jnp.exp(log_std))

    # actor loss
    actor_loss = -(weights*dist_stds_k.log_prob(sampled_actions)).mean() - \
      (weights*dist_means_k.log_prob(sampled_actions)).mean()
    std_kl = tfp.distributions.kl_divergence(
      target_policy_dist, dist_stds_k).mean()
    means_kl = tfp.distributions.kl_divergence(
      target_policy_dist, dist_means_k).mean()

    actor_loss -= jax.lax.stop_gradient(mu_net.apply_fn(mu_net.params))*(eps_mu - means_kl)
    actor_loss -= jax.lax.stop_gradient(std_net.apply_fn(std_net.params))*(eps_std - std_kl)
    actor_loss -= temp_loss

    return actor_loss, {
      'actor_loss': actor_loss, 'mu_net': mu_net, 'std_net': std_net,
      } # **mu_info, **std_info}

  loss_info, grads = jax.value_and_grad(loss_fn, has_aux=True)(
    actor_net.params, mu_net, std_net)

  grads = clip_grads(grads, 100.0)
  new_actor_net = actor_net.apply_gradients(grads=grads)
  return new_actor_net, loss_info[1]['mu_net'], loss_info[1]['std_net'], loss_info[1]