from littlenn.activation_functions.abstract_activation import ActivationFunction

class Linear(ActivationFunction):
    def __call__(self, x):
        return x
    def derivative(self, x):
        return x