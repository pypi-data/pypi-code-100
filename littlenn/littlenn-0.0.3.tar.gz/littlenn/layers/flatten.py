import numpy as np
from littlenn.layers.abstract_layer import Layer

class Flatten(Layer):
    def __init__(self):
        super(Flatten, self).__init__()

    def _create_weights(self, dim_in):
        self.dim_out = np.prod(dim_in)

    def _init_optimizers(self, optimizer_factory, params):
        pass

    def _get_weights(self):
        return None

    def _get_trainable_params(self):
        return 0

    def __call__(self, x, training):
        self.previous_shape = x.shape
        return x.reshape(-1, self.previous_shape[-1])

    def grads(self, grads):
        prev_derivative, *_ = grads
        print('dlatten reshpae :', self.previous_shape)
        return prev_derivative.reshape(self.previous_shape), None, None

    def _apply_grads(self, grads):
        pass

    def __str__(self):
        return "Flatten"