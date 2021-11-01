import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from abc import ABC
from sklearn import metrics
from dataclasses import dataclass
from typing import Union, Any, Optional
from SnowML.evaluation.evaluation_utils import print_cm, find_best_threshold


@dataclass
class BaseEvaluator(ABC):
    model: Any
    X_train: Union[pd.Series, np.ndarray]
    X_test: Union[pd.Series, np.ndarray]
    y_train: Union[pd.Series, np.ndarray]
    y_test: Union[pd.Series, np.ndarray]


@dataclass
class ThresholdEvaluator(BaseEvaluator):
    th: Optional[float] = 0.5

    def get_probabilities(self, label_index: int = None):
        """
        Calcualte probabilities for all labels or a single label at 'return_index' in self.X_test
        using 'self.model.predict_proba' .
        :param label_index: The label index to return probabilities for.
        :return: numpy array or n-array for given label(s).
        """

        if label_index is not None:
            return self.model.predict_proba(self.X_test[:, label_index])

        return self.model.predict_proba(self.X_test)

    def get_predictions(self, by_proba=True, positive_label=1, use_best=True):
        """
        Calculate predictions for instance's test set.
        :param by_proba: when true, predictions will be calculated
        from `self.probabilities` and a threshold. probabilities are calculated from `model.predict_proba' or needed
        to be provided to self.probabilities.
        :param positive_label: The positive label to calculate prediction for.
        Suitable only for binary classification.
        :param use_best: if true, using best threshold (found be
        find_best_threshold) for predictions. Using instance's thereshold otherwise. :return:
        """

        if by_proba:
            self.probabilities = self.get_probabilities(positive_label)

            if use_best:
                fpr, tpr, thresholds = metrics.roc_curve(self.y_test, self.probabilities)
                self.best_threshold = find_best_threshold(fpr, tpr, thresholds)
                self.th = self.best_threshold

            self.predictions = (self.probabilities > self.th).astype(int)
        else:
            self.predictions = self.model.predict(self.X_test)

        return self.predictions

    def confusion_matrix(self, labels: list):
        print('****************************************************')
        cm = metrics.confusion_matrix(self.y_test, self.predictions, labels)
        print('Confusion Matrix=')
        print_cm(cm, labels)
        print('classification_report=')
        print(metrics.classification_report(self.y_test, self.predictions, digits=3,
                                            target_names=[str(l) for l in labels]))
        print('FPR:', "{0:.2%}".format(round(metrics.confusion_matrix(self.y_test, self.predictions)[0, 1] /
                                             (metrics.confusion_matrix(self.y_test, self.predictions)[0, 1]
                                              + metrics.confusion_matrix(self.y_test, self.predictions)[0, 0]), 4)))
        self.test_roc_auc_test = round(metrics.roc_auc_score(self.y_test, self.probabilities), 4)
        print('AUC:', "{0:.2%}".format(self.test_roc_auc_test))
        print('Accuracy Score:', "{0:.2%}".format(round(metrics.accuracy_score(self.y_test, self.predictions), 4)))
        print('Best Threshold:', "{0:.2%}".format(round(self.best_threshold, 4)))
        print('****************************************************')

    def plot_roc_auc(self, with_plots: bool = True):

        # Plot test roc
        plt.figure()
        fpr, tpr, thresholds = metrics.roc_curve(self.y_test, self.probabilities)
        plt.plot(fpr, tpr, label='test')

        # Plot train
        probabilities = self.model.predict_proba(self.X_train)[:, 1]
        fpr, tpr, thresholds = metrics.roc_curve(self.y_train, probabilities)
        if with_plots:
            plt.plot(fpr, tpr, label='train')
            plt.plot([0, 1], [0, 1], 'r--', label='random guess')
            plt.title("Area under the ROC = {}".format(self.test_roc_auc_test), fontsize=18)
            plt.legend()
            plt.show()

            rcl_per_disp = metrics.plot_precision_recall_curve(self.model, self.X_test, self.y_test)
            plt.show()

            roc_disp = metrics.plot_roc_curve(self.model, self.X_test, self.y_test)
            plt.cla()
            plt.clf()
            plt.close()
