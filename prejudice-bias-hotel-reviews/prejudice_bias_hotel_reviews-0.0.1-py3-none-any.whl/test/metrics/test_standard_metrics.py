import unittest
import numpy as np
import sklearn.metrics

from src.metrics.standard_metrics import recall_score, precision_score
from src.metrics.standard_metrics import f1_score, f1_macro_score


class TestStandardMetrics(unittest.TestCase):
    def setUp(self):
        self.y_true = np.asarray([0., 1., 0.])
        self.y_pred = np.asarray([0., 0., 1.])

    def test_recall(self):
        recall_own = recall_score(self.y_true, self.y_pred).numpy()
        recall_skl = sklearn.metrics.recall_score(self.y_true, self.y_pred)
        self.assertAlmostEqual(recall_own, recall_skl, places=2)

    def test_precision(self):
        own = precision_score(self.y_true, self.y_pred).numpy()
        skl = sklearn.metrics.precision_score(self.y_true, self.y_pred)
        self.assertAlmostEqual(own, skl, places=2)

    def test_f1(self):
        own = f1_score(self.y_true, self.y_pred).numpy()
        skl = sklearn.metrics.f1_score(self.y_true, self.y_pred)
        self.assertAlmostEqual(own, skl, places=2)

    def test_f1_macro(self):
        own = f1_macro_score(self.y_true, self.y_pred).numpy()
        skl = sklearn.metrics.f1_score(self.y_true,
                                       self.y_pred,
                                       average='macro')
        self.assertAlmostEqual(own, skl, places=2)


if __name__ == '__main__':
    unittest.main()
