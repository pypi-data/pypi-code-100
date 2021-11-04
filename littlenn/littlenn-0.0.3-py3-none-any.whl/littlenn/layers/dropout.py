import numpy as np
from littlenn.layers.abstract_layer import Layer

class Dropout(Layer):
    def __init__(self, keep_prob):
        super(Dropout, self).__init__()
        self.keep_prob = keep_prob

    def _create_weights(self, dim_in):
        self.dim_out = dim_in

    def _init_optimizers(self, optimizer_factory, params):
        pass

    def _get_weights(self):
        return self.W.reshape(-1, 1)

    def _get_trainable_params(self):
        return 0

    def __call__(self, x, training):
        if training:
            self.W = (np.random.rand(x.shape[0], x.shape[1]) <= self.keep_prob) / self.keep_prob
            act = self.W * x
        else:
            act = x
        return act
    
    def grads(self, grads):
        dprev, *z = grads
        return self.W * dprev

    def _apply_grads(self, grads):
        pass

    def __str__(self):
        return "Dropout : (keep_prob = %.1f)" % self.keep_prob