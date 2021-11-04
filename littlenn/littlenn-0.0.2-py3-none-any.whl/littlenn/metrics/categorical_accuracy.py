import numpy as np

class CategoricalAccuracy:
    def __init__(self):
        self.accuracy_sums = 0
        self.iter = 1e-12
    def __call__(self, y_true, y_pred):
        print(y_pred.shape)
        y_pred = np.argmax(y_pred, axis=0)
        y_true = np.argmax(y_true, axis=0)
        accuracy = np.sum(y_pred == y_true) / y_true.size
        print(y_pred)
        self.accuracy_sums += accuracy
        self.iter += 1
    def result(self):
        return self.accuracy_sums / self.iter
    def reset_states(self):
        self.accuracy_sums = 0
        self.iter = 1e-12