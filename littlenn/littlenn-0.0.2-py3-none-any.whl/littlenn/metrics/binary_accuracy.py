import numpy as np

class BinaryAccuracy:
    def __init__(self):
        self.accuracy_sums = 0
        self.iter = 1e-12
    def __call__(self, y_true, y_pred):
        y_pred[y_pred >= 0.5] = 1
        y_pred[y_pred < 0.5] = 0
        accuracy = np.sum(y_pred == y_true) / y_true.size
        self.accuracy_sums += accuracy
        self.iter += 1
    def result(self):
        return self.accuracy_sums / self.iter
    def reset_states(self):
        self.accuracy_sums = 0
        self.iter = 1e-12