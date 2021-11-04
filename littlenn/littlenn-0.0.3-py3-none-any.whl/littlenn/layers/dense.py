import numpy as np
from littlenn.layers.abstract_layer import Layer

class Dense(Layer):
    def __init__(self, dim_out, activation=None):
        super(Dense, self).__init__()
        self.dim_out = dim_out
        self.act_fn = self.activations[activation]

    def _create_weights(self, dim_in):
        self.dim_in = dim_in
        # Xavier-initialization
        self.W = np.random.randn(self.dim_out, dim_in) * np.sqrt(2 / (dim_in + self.dim_out))
        self.b = np.random.randn(self.dim_out, 1) * np.sqrt(1 / (self.dim_out))

    def _init_optimizers(self, optimizer_factory, params):
        self.W_opt = optimizer_factory.create_instance(params)
        self.b_opt = optimizer_factory.create_instance(params)

    def _get_weights(self):
        weights = np.concatenate((self.W.flatten(), self.b.flatten()), axis=None)
        return weights.reshape(-1, 1)

    def _get_trainable_params(self):
        return self.W.size + self.b.size

    def __call__(self, x, training):
        self.z_prev = x
        self.act = np.matmul(self.W, self.z_prev) + self.b
        return self.act_fn(self.act)

    def grads(self, grads):
        dprev, *_ = grads
        act_deriv = self.act_fn.derivative(self.act)
        dW = np.matmul(dprev * act_deriv, self.z_prev.T)
        db = np.mean(dprev * act_deriv, keepdims=True)
        dprev_new =  np.matmul(self.W.T, dprev * act_deriv)
        return dprev_new, dW, db

    def _apply_grads(self, grads):
        *_, dW, db = grads
        self.W = self.W_opt(self.W, dW)
        self.b = self.b_opt(self.b, db)

    def __str__(self):
        return "DenseBlock : (%s, %s)" % (self.W.shape[1], self.W.shape[0])