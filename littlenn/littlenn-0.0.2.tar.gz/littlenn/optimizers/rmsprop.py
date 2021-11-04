import numpy as np

class RMSProp:
    def __init__(self, learning_rate, beta):
        self.learning_rate = learning_rate
        self.beta = None
        if not beta is None:
            self.moving_squared_average = None
            self.beta = beta

    def __call__(self, weights, derivatives): 
        if not self.beta is None:
            if self.moving_squared_average is None:
                self.moving_squared_average = np.zeros_like(derivatives)
            self.moving_squared_average = self.beta * self.moving_squared_average + (1. - self.beta) * derivatives ** 2 
            derivatives /= ( np.sqrt(self.moving_squared_average) + 1e-8 ) 
        return weights - self.learning_rate * derivatives