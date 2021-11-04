import numpy as np
from littlenn.layers.abstract_layer import Layer

class Conv2D(Layer):
    def __init__(self, channels_out, kernel_size,
                 padding, strides, activation=None):
        super(Conv2D, self).__init__()
        self.channels_out = channels_out
        self.act_fn = self.activations[activation]
        self.padding = padding
        self.strides = strides
        self.kernel_size = kernel_size

    def _create_weights(self, dim_in):
        self.channels_in, self.input_height, self.input_width = dim_in
        # Xavier-initialization
        self.kernels = np.random.randn(
            self.channels_in, self.kernel_size[0], self.kernel_size[1], self.channels_out) * np.sqrt(
                2 / (self.channels_in * self.kernel_size[0] * self.kernel_size[1] * self.channels_out))
        self.biases = np.random.randn(self.channels_out, 1) * np.sqrt(1 / (self.channels_out))
        self.dim_out = (self.channels_out,
          (self.input_height - self.kernel_size[0] + self.padding[0] ) // self.strides[0] + 1,
          (self.input_width - self.kernel_size[1] + self.padding[1] ) // self.strides[1] + 1)

    def _init_optimizers(self, optimizer_factory, params):
        self.kernels_opt = optimizer_factory.create_instance(params)
        self.biases_opt = optimizer_factory.create_instance(params)

    def _get_weights(self):
        weights = np.concatenate((self.kernels.flatten(), self.biases.flatten()), axis=None)
        return weights.reshape(-1, 1)

    def _get_trainable_params(self):
        return self.kernels.size + self.biases.size

    def __correlation(self, x, kernel):
        _, h, w = kernel.shape
        C, H, W, bs = x.shape

        assert kernel.shape[0] == x.shape[0], 'Channels must be equal for kernel and input tensor'

        # H, and W already padded (!)
        H_out = np.floor(( H - h + self.strides[0] ) / self.strides[0]).astype(int)
        W_out = np.floor(( W - w + self.strides[1] ) / self.strides[1]).astype(int)
        
        Y = np.zeros((H_out, W_out, bs))
        
        for i in range(H, self.strides[0]):
            for j in range(W, self.strides[1]):
                Y[:, i, j, :] = np.sum(X[:, i:i+h, j:j+w, :] * kernel)
        
        return Y

    def __pad(self, x):
        return np.pad(
            x, ((0, 0), (self.padding[0], self.padding[0]),
                (self.padding[1], self.padding[1]), (0, 0)),
            mode='constant', constant_values=0)

    def __multichannel_correlation(self, x, kernels=None):
        if kernels is None:
            kernels = self.kernels
        return np.stack([self.__correlation(
                self.__pad(x), k) for k in np.einsum('ijkl->lijk', kernels)])

    def __call__(self, x, training):
        self.previous_output = x
        self.output_before_activation = self.__multichannel_correlation(
            self.previous_output)
        self.output = self.act_fn(self.output_before_activation)
        return self.output

    def grads(self, grads):
        dprev, *_ = grads
        dodx = self.act_fn.derivative(self.output_before_activation)
        #print('dodx, dprev :', dodx.shape, dprev.shape, self.previous_output.shape)
        dK = np.zeros(shape=(self.previous_output.shape[0], self.kernels.shape[1],
                        self.kernels.shape[2], dodx.shape[0]))

        _dodx = np.mean(dodx * dprev, axis=-1, keepdims=True)
        prev_o = np.mean(self.previous_output, axis=-1, keepdims=True)

        for ind, _K in enumerate(_dodx):
            o = self.__correlation(np.einsum('ijkl->ljki', prev_o),
                                np.einsum('ijk->kij', _K)).T
            dK[..., ind] += o

        print('dprev, dodx, K', dprev.shape, dodx.shape, np.einsum('ijkl->ljki', self.kernels).shape)
        dprev_new = self.previous_output #dodx #* self.kernels
        db = np.mean(dodx, axis=(1, 2, 3)).reshape(self.biases.shape)
        
        print('output', self.output.shape, self.previous_output.shape)

        return dprev_new, dK, db

    def _apply_grads(self, grads):
        *_, dK, db = grads
        self.kernels = self.kernels_opt(self.kernels, dK)
        self.biases = self.biases_opt(self.biases, db)

    def __str__(self):
        return "Conv2D : (%s, %s)" % (1, 2)