import numpy as np
import torch
from collections import OrderedDict
from dataclasses import dataclass
from typing import Any, Tuple, Union, List


@dataclass
class Variable:
    """
    Represents objects that can be stored, e.g. state or reward
    """

    name: str
    dtype: torch.dtype = torch.float32 # data type, should be a torch data type
    shape: Tuple[Tuple[int]] = ((1,),) # Nesting is possible, e.g. if state consists of two tensors with different shapes

class Batch(OrderedDict):

    def __init__(self, **kwargs):
        super().__init__(kwargs)

    def unpack(self):
        return self.values()

class Buffer:
    """
    Implements a Buffer for exactly one type of variable
    The variable may however consists of multiple components with different shapes.
    """
    def __init__(self, size, variable):
        self.variable = variable
        self.buffers = [np.zeros((size,) + tuple(shape)) for shape in self.variable.shape]

    def set(self, idx, variable_instance):
        if len(self.variable.shape) > 1: # more than one component
            for i, component_instance in enumerate(variable_instance):
                self.buffers[i][idx] = component_instance
        else: # only one component
            self.buffers[0][idx] = variable_instance

    def get(self, idx, device):
        if len(self.variable.shape) > 1: # more than one component
            return [torch.from_numpy(self.buffers[i][idx]).to(self.variable.dtype).to(device)
                    for i in range(len(self.variable.shape))]
        else: # only one component
            return torch.from_numpy(self.buffers[0][idx]).to(self.variable.dtype).to(device)


class ReplayBuffer:
    """
    A more flexible replay buffer implementation for use with pytorch

    Can be useful when implementing e.g. n-step returns, when storing continuous actions that have some
    fixed shape, when there is more than one reward signal, [...].
    """


    def __init__(self,
                 size: int,
                 batch_size: int,
                 variables: List[Variable],
                 seed: Any = 0,
                 device=None):
        """

        :param size: Buffer size, i.e. maxmimal number of entries
        :type size: int

        :param batch_size: size of sampled batches
        :type batch_size: int

        :param variables:
        :type variables: List[Variable]

        :param seed:
        :type seed: Any

        :param device:
        """
        self.device = device
        self.size = size
        self.batch_size = batch_size
        self.variables = variables
        self.seed = seed
        self.rng = np.random.default_rng(seed)

        self.buffers = {variable.name : Buffer(size, variable) for variable in variables}
        self.counter = 0
        self.num_stored = 0

    def add(self, **variable_instances):
        for variable_name, variable_instance in variable_instances.items():
            self.buffers[variable_name].set(self.counter, variable_instance)

        self.counter = (self.counter + 1) % self.size
        self.num_stored = min(self.size, self.num_stored + 1)

    def __len__(self):
        return self.num_stored

    def sample(self):
        sample_ids = self.rng.integers(0, len(self), self.batch_size)
        return Batch(**{var.name : self.buffers[var.name].get(sample_ids, self.device) for var in self.variables}).unpack()


# usage example
class StandardReplayBuffer(ReplayBuffer):

    def __init__(self, state_variable_sizes, *args, **kwargs):
        variables = []
        variables.append(Variable("state", shape=tuple(tuple(svs) for svs in state_variable_sizes)))
        variables.append(Variable("action", dtype=torch.long))
        variables.append(Variable("reward"))
        variables.append(Variable("next_state", shape=variables[0].shape))
        variables.append(Variable("done"))
        super().__init__(*args, variables, **kwargs)


# usage example continued
if __name__ == "__main__":
    buf = StandardReplayBuffer([[5,12],[1]], 100, 4)
    for i in range(1000):
        buf.add(state=[np.random.rand(5, 12), 3], action=4, reward=0, next_state=[np.random.rand(5,12), 2], done=0)

    batch = buf.sample()
    state, action, reward, next_state, done = batch.unpack()
    print(state)
