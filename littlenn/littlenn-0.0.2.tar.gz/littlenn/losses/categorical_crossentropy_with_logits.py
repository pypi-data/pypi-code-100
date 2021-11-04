import numpy as np

class CategoricalCrossEntropyWithLogits:
    def __init__(self):
        self.__softmax = lambda x, ax : np.exp( x - np.max(x, axis=ax)) / np.sum(np.exp( x - np.max(x, axis=ax) ), axis=ax)
        self.total_loss = 0.0
        self.iters = 1e-12

    def __call__(self, y_true, logits):
        self.y_true = y_true
        self.y_pred = np.apply_over_axes(self.__softmax, logits, axes=[0])

        batch_loss = -np.mean(self.y_true * np.log(self.y_pred + 1e-12))

        self.total_loss += batch_loss
        self.iters += 1

        return batch_loss

    def backprop(self):

        return (- self.y_true / ( self.y_pred + 1e-12 ), None)

    def result(self):
        return self.total_loss / self.iters

    def reset_state(self):
        self.__init__()
