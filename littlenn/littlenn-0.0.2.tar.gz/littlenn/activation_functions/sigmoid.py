from .abstract_activation import ActivationFunction
import numpy as np

class Sigmoid(ActivationFunction):
    def __init__(self):
        self.__sigmoid = lambda x : 1. / (1. + np.exp(-x))
    def __call__(self, x):
        return self.__sigmoid(x)
    def derivative(self, x):
        return self.__sigmoid(x) * self.__sigmoid(-x)