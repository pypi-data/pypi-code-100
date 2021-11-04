import numpy as np
from littlenn.model.abstract_model import Model
from tqdm import tqdm

class Sequential(Model):
    def __init__(self, input_size):
        super(Sequential, self).__init__()
        self.layers = []
        self.input_size = input_size
        self.__current_input_size = input_size

    def add(self, layer):
        layer._create_weights(self.__current_input_size)
        self.layers.append(layer)
        self.__current_input_size = layer.dim_out

    def __call__(self, x, training=True):
        for layer in self.layers:
            x = layer(x, training)       
        return x

    def _backprop(self, grads):
        for layer in self.layers[::-1]:
            grads = layer.grads(grads)
            try:
                #print('Layer :', layer.dim_in, layer.dim_out)
                #print("Grads :", grads[0].shape, grads[1].shape, grads[2].shape)
                pass
            except Exception:
                pass
            layer._apply_grads(grads)

    def summary(self):
        param_count = 0
        print('MODEL:')
        for layer in self.layers:
            param_count +=  layer._get_trainable_params()
            print(layer, '\ttrainable params : %d' % (layer._get_trainable_params()))
        print('Total trainable parameters : %d' % param_count)
    
    def __batch_generator(self, X, y, batch_size):
        random_indices = np.random.choice(range(0, X.shape[0]), size=X.shape[0], replace=False)
        arr = X[random_indices]
        lab = y[random_indices]
        for i in range(0, arr.shape[0], batch_size):
            yield arr[i:i+batch_size].T, lab[i:i+batch_size].T

    def compile(self, loss, optimizer_params):
        self.optimizer_params = optimizer_params
        self.optimizer_factory = self.optimizers[optimizer_params['name']]
        self.loss = self.losses[loss]
        self.metric = self.metrics[loss]

        for layer in self.layers:
            layer._init_optimizers(self.optimizer_factory, self.optimizer_params)

    def fit(self, X, y, epochs, batch_size):
        tqdm_epoch = tqdm(range(epochs))
        for epoch in tqdm_epoch:
            for batch, batch_labels in self.__batch_generator(X, y, batch_size):
                y_pred = self(batch)
                loss = self.loss(batch_labels, y_pred)
                loss_deriv = self.loss.backprop()
                accuracy = self.metric(batch_labels, y_pred)
                self._backprop(loss_deriv)  
                tqdm_epoch.set_description(f'Epoch {epoch + 1} | loss : {self.loss.result():.3f} | accuracy {self.metric.result() * 100:.1f} %')
                tqdm_epoch.refresh()