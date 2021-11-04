import abc

class ActivationFunction(abc.ABC):
    @abc.abstractmethod
    def __call__(self, x):
        pass  
    @abc.abstractmethod
    def derivative(self, x):
        pass