import numpy as np

class BinaryCrossEntropy:
    def __init__(self):
        self.total_loss = 0.0
        self.iters = 1e-12

    def __call__(self, y_true, y_pred):
        self.y_true = y_true
        self.y_pred = y_pred

        batch_loss = np.mean(- (y_true * np.log(y_pred + 1e-12) + (1-y_true) * np.log(1-y_pred + 1e-12)))

        self.total_loss += batch_loss
        self.iters += 1

        return batch_loss

    def backprop(self):
        return ((self.y_pred - self.y_true) / (self.y_pred * (1. - self.y_pred) + 1e-12), None)

    def result(self):
        return self.total_loss / self.iters

    def reset_state(self):
        self.__init__()

