import numpy as np

class SGD:
    def __init__(self, learning_rate, exponential_weight):
        self.learning_rate = learning_rate
        self.exponential_weight = 1.
        if exponential_weight != None:
            self.moving_average = None
            self.exponential_weight = exponential_weight

    def __call__(self, weights, derivatives): 
        if self.exponential_weight < 1:
            if self.moving_average is None:
                self.moving_average = np.zeros_like(weights)
            self.moving_average = self.exponential_weight * self.moving_average + (1. - self.exponential_weight) * derivatives 
            derivatives = self.moving_average
        return weights - self.learning_rate * derivatives