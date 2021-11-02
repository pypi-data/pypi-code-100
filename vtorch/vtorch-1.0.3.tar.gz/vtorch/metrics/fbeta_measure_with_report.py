from itertools import repeat
from typing import Dict, List

import pandas as pd
import torch

from vtorch.metrics import FBetaMeasure
from vtorch.metrics.fbeta_measure import _prf_divide


class FBetaMeasureWithClearMLReport(FBetaMeasure):
    def _update_for_return_report(  # type: ignore[override]
        self,
        result_dict: Dict[str, Dict[str, float]],
        precision: torch.Tensor,
        recall: torch.Tensor,
        fscore: torch.Tensor,
    ) -> None:

        if self.label_names is None:
            self.label_names = [str(i) for i in range(len(fscore))]

        overall_metric_dict = result_dict
        result_dict: Dict[str, float] = {}  # type: ignore

        df: Dict[str, List[float]] = {"precision": [], "recall": [], "fscore": []}
        for metric_name, class_values in ("precision", precision), ("recall", recall), ("fscore", fscore):
            for class_name, class_value in zip(self.label_names, class_values):
                result_dict[f"{metric_name}_{class_name}"] = class_value.item()
                df[metric_name].append(class_value.item())

        self.report = pd.DataFrame(df, index=self.label_names)
        self.report = self.report.append(pd.DataFrame(overall_metric_dict).T)
        support = self._true_sum.tolist()  # type: ignore
        support.extend(repeat(sum(support), len(self.report) - len(support)))
        self.report["support"] = support

        # format for convenient copy-paste into the sheets
        self.report = self.report.apply(lambda column: column.apply("{:.3f}".format)).reset_index()
        self.report = self.report.apply(lambda column: column.astype(str) + ",").set_index("index")
        self.report.columns = [f"{col}," if i else f",{col}," for i, col in enumerate(self.report.columns)]

        for average, metrics in overall_metric_dict.items():
            for metric_name, value in metrics.items():
                result_dict[f"{average}_{metric_name}"] = value  # type: ignore

        overall_metric_dict.clear()
        overall_metric_dict.update(result_dict)  # type: ignore

    def _update_for_macro(  # type: ignore[override]
        self,
        result_dict: Dict[str, Dict[str, float]],
        precision: torch.Tensor,
        recall: torch.Tensor,
        fscore: torch.Tensor,
    ) -> None:
        result_dict["macro"] = {
            "precision": precision.mean().item(),
            "recall": recall.mean().item(),
            "fscore": fscore.mean().item(),
        }

    def _update_for_micro(self, result_dict: Dict[str, Dict[str, float]]) -> None:  # type: ignore[override]

        beta2 = self._beta ** 2

        tp_sum = self._true_positive_sum.sum()  # type: ignore
        pred_sum = self._pred_sum.sum()  # type: ignore
        true_sum = self._true_sum.sum()  # type: ignore

        micro_precision = _prf_divide(tp_sum, pred_sum)
        micro_recall = _prf_divide(tp_sum, true_sum)
        micro_fscore = (1 + beta2) * micro_precision * micro_recall / (beta2 * micro_precision + micro_recall)
        micro_fscore[tp_sum == 0] = 0.0

        result_dict["micro"] = {
            "precision": micro_precision.item(),
            "recall": micro_recall.item(),
            "fscore": micro_fscore.item(),
        }
