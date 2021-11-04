import numpy as np
import math

class Adam:
    def __init__(self, learning_rate, exponential_weight, beta):
        self.learning_rate = learning_rate
        self.exponential_weight = None
        if not exponential_weight is None:
            self.moving_average = None
            self.exponential_weight = None
        self.beta = None
        if not beta is None:
            self.moving_squared_average = None
            self.beta = beta

    def __call__(self, weights, derivatives): 
        original_derivatives = derivatives

        if not self.exponential_weight is None:
            if self.moving_average is None:
                self.moving_average = np.zeros_like(original_derivatives)
            self.moving_average = self.exponential_weight * self.moving_average + (1. - self.exponential_weight) * original_derivatives
            derivatives = self.moving_average

        if not self.beta is None:
            if self.moving_squared_average is None:
                self.moving_squared_average = np.zeros_like(original_derivatives)
            self.moving_squared_average = self.beta * self.moving_squared_average + (1. - self.beta) * np.square(original_derivatives)
            derivatives /= (np.sqrt(self.moving_squared_average) + 1e-8)

        return weights - self.learning_rate * derivatives