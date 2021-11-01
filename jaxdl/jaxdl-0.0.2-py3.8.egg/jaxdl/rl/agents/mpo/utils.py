import jax
import jax.numpy as jnp
import numpy as np

from jaxdl.utils.commons import TrainState


def update_target(net: TrainState, target_net: TrainState,
  tau: float) -> TrainState:
  """Function to update the target net network

  Args:
    net (TrainState): net network
    target_net (TrainState): Target net network
    tau (float): Linear interpolation parameter

  Returns:
    TrainState: Target net network
  """
  new_target_net_params = jax.tree_multimap(
    lambda params, target_params: tau*params + (1 - tau) * target_params,
    net.params, target_net.params)
  return target_net.replace(params=new_target_net_params)