from sklearn.metrics import confusion_matrix, precision_score, recall_score, roc_curve, auc, f1_score, classification_report
import json

from sklearn.preprocessing import LabelBinarizer
from itertools import chain


class TaggingReport:

    def __init__(self, y_test, y_pred, y_scores, num_features, num_examples, classes, pos_label= None):
        # check number of classes
        # if binary problem calculate roc
        if len(classes) == 2:
            self.average = "binary"
            fpr, tpr, _ = roc_curve(y_test, y_scores, pos_label=pos_label)
            self.true_positive_rate = tpr.tolist()
            self.false_positive_rate = fpr.tolist()
            self.area_under_curve = auc(fpr, tpr)
        else:
            self.average = "micro"
            self.area_under_curve = 0.0
            self.true_positive_rate = []
            self.false_positive_rate = []

        self.report = classification_report(
            y_test,
            y_pred,
            labels = classes,
            output_dict = True
        )

        self.report_str = str(
            classification_report(
                y_test,
                y_pred,
                labels = classes
            )
        )

        self.precision = precision_score(y_test, y_pred, pos_label=pos_label, average=self.average)
        self.f1_score = f1_score(y_test, y_pred, pos_label=pos_label, average=self.average)
        self.confusion = confusion_matrix(y_test, y_pred, labels=classes)

        self.recall = recall_score(y_test, y_pred, pos_label=pos_label, average=self.average)
        self.num_features = num_features
        self.num_examples = num_examples
        self.classes = classes
        self.pos_label = pos_label

    def to_dict(self):
        return {
            "f1_score": round(self.f1_score, 5),
            "precision": round(self.precision, 5),
            "recall": round(self.recall, 5),
            "num_features": self.num_features,
            "num_examples": self.num_examples,
            "confusion_matrix": self.confusion.tolist(),
            "area_under_curve": round(self.area_under_curve, 5),
            "true_positive_rate": self.true_positive_rate,
            "false_positive_rate": self.false_positive_rate,
            "classes": self.classes,
            "pos_label": self.pos_label,
            "report": self.report
        }
