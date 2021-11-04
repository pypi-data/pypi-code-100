import numpy as np
from littlenn.layers.abstract_layer import Layer
import numpy as np

class BatchNorm(Layer):
    def __init__(self, activation=None):
        super(BatchNorm, self).__init__()
        self.act_fn = self.activations[activation]

    def _create_weights(self, dim_in):
        self.dim_out = dim_in
        self.gamma = np.random.randn(self.dim_out, 1) * np.sqrt(1 / (self.dim_out))
        self.beta = np.random.randn(self.dim_out, 1) * np.sqrt(1 / (self.dim_out))
        self.mean = None
        self.variance = None

    def _init_optimizers(self, optimizer_factory, params):
        self.gamma_opt = optimizer_factory.create_instance(params)
        self.beta_opt = optimizer_factory.create_instance(params)

    def _get_weights(self):
        weights = np.concatenate((self.gamma.flatten(), self.beta.flatten()), axis=None)
        return self.weights.reshape(1, -1)

    def _get_trainable_params(self):
        return self.gamma.size + self.beta.size

    def __call__(self, x, training):
        if training:
            if self.mean is None:
                # 0th axis is the minibatch axis
                self.mean = np.mean(x, axis=0).reshape(1, *x.shape[1:])
                self.variance = np.var(x, axis=0).reshape(1, *x.shape[1:])
            # Moving average moving_beta = 0.9
            else:
                self.mean = 0.9 * self.mean + 0.1 * np.mean(x, axis=0).reshape(1, *x.shape[1:])
                self.variance = 0.9 * self.variance + 0.1 * np.var(x, axis=0).reshape(1, *x.shape[1:])
        self.x_norm = (x - self.mean) / (np.sqrt(self.variance) + 1e-8)
        self.act = self.gamma * self.x_norm + self.beta
        return self.act_fn(self.act)
    
    def grads(self, grads):
        dprev, *z = grads
        act_deriv = self.act_fn.derivative(self.act)
        #print('act_deriv : ', act_deriv.shape)
        #print('dprev : ', dprev.shape)
        #print('x_norm : ', self.x_norm.shape)
        dgamma = np.mean(np.matmul(dprev * act_deriv, self.x_norm.T), axis=1, keepdims=True)
        #print('dgamma : ', dgamma.shape)
        dbeta = np.mean(dprev * act_deriv, axis=1, keepdims=True)
        #print('dbeta : ', dbeta.shape)
        dprev_new = dprev * self.gamma * act_deriv
        return dprev_new, dgamma, dbeta

    def _apply_grads(self, grads):
        *z, dgamma, dbeta = grads
        

    def __str__(self):
        return "Dropout : (keep_prob = %.1f)" % self.keep_prob