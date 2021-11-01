"""Temperature network implementations"""
import jax.numpy as jnp
from flax import linen as nn

from jaxdl.utils.commons import PRNGKey, Module


def create_constant_network_fn(initial_value: float = 1.0) -> Module:
  """Returns a constant network

  Args:
      initial_value (float, optional): Initial value. Defaults to 1.0.

  Returns:
      Module: Constant network
  """
  return ConstantNet(initial_value=initial_value)


class ConstantNet(nn.Module):
  """Constant network."""
  initial_value: float = 1.0
  is_absolute_value: bool = False

  @nn.compact
  def __call__(self, dtype=jnp.float32) -> jnp.ndarray:
    """Returns the value"""
    value = self.param('value',
      init_fn=lambda _: jnp.full((), jnp.log(self.initial_value)))
    if self.is_absolute_value:
      value = nn.softplus(value)
    return jnp.asarray(value, dtype)