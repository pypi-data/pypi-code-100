import abc
from littlenn.activation_functions.relu import ReLU
from littlenn.activation_functions.sigmoid import Sigmoid
from littlenn.activation_functions.linear import Linear

class Layer(abc.ABC):
    def __init__(self):
        self.activations = {"relu" : ReLU(), "sigmoid" : Sigmoid(),
                            "linear" : Linear(), None : Linear()}
    
    @abc.abstractmethod  
    def _create_weights(self, dim_in):
        pass

    @abc.abstractmethod
    def _init_optimizers(self, optimizer_factory, params):
        pass

    @abc.abstractmethod
    def _get_weights(self):
        pass

    @abc.abstractmethod
    def _get_trainable_params(self):
        pass

    @abc.abstractmethod
    def __call__(self, x, training):
        pass

    @abc.abstractmethod
    def grads(self, x):
        pass

    @abc.abstractmethod
    def _apply_grads(self, x):
        pass