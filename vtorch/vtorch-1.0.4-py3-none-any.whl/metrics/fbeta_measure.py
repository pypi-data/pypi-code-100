from itertools import chain
from typing import Dict, List, Optional, Union

import torch
from overrides import overrides

from vtorch.common.checks import ConfigurationError
from vtorch.common.utils import tensor_to_ohe
from vtorch.postprocessing.default import PredictionPostprocessorI

from .metric import Metric


class FBetaMeasure(Metric):
    NAMES = ["precision", "recall", "fscore"]

    """Compute precision, recall, F-measure and support for each class.
        The precision is the ratio ``tp / (tp + fp)`` where ``tp`` is the number of
        true positives and ``fp`` the number of false positives. The precision is
        intuitively the ability of the classifier not to string as positive a sample
        that is negative.
        The recall is the ratio ``tp / (tp + fn)`` where ``tp`` is the number of
        true positives and ``fn`` the number of false negatives. The recall is
        intuitively the ability of the classifier to find all the positive samples.
        The F-beta score can be interpreted as a weighted harmonic mean of
        the precision and recall, where an F-beta score reaches its best
        value at 1 and worst score at 0.
        If we have precision and recall, the F-beta score is simply:
        ``F-beta = (1 + beta ** 2) * precision * recall / (beta ** 2 * precision + recall)``
        The F-beta score weights recall more than precision by a factor of
        ``beta``. ``beta == 1.0`` means recall and precision are equally important.
        The support is the number of occurrences of each class in ``y_true``.
        Parameters
        ----------
        beta : ``float``, optional (default = 1.0)
            The strength of recall versus precision in the F-score.
        average : string, [None (default), 'micro', 'macro']
            If ``None``, the scores for each class are returned. Otherwise, this
            determines the type of averaging performed on the data:
            ``'micro'``:
                Calculate metrics globally by counting the total true positives,
                false negatives and false positives.
            ``'macro'``:
                Calculate metrics for each string, and find their unweighted mean.
                This does not take string imbalance into account.
        sequence: list, optional
            The set of sequence to include and their order if ``average is None``.
            Labels present in the data can be excluded, for example to calculate a
            multi-class average ignoring a majority negative class. Labels not present
            in the data will result in 0 components in a macro average.
        """

    def __init__(
        self,
        beta: float = 1.0,
        average: Optional[str] = None,
        predictions_postprocessor: Optional[PredictionPostprocessorI] = None,
        return_report: bool = False,
        label_names: Optional[List[str]] = None,
    ) -> None:
        super().__init__(predictions_postprocessor)
        average_options = (None, "micro", "macro")
        if average not in average_options:
            raise ConfigurationError(f"`average` has to be one of {average_options}.")
        if beta <= 0:
            raise ConfigurationError("`beta` should be >0 in the F-beta score.")

        self._beta = beta
        self._average = average
        self._return_report = return_report
        if return_report:
            self.NAMES = list(chain.from_iterable([f"macro_{metric}", f"micro_{metric}"] for metric in self.NAMES))
        self.label_names = label_names

        # statistics
        # the total number of true positive instances under each class
        # Shape: (num_classes, )
        self._true_positive_sum: Optional[torch.Tensor] = None
        # the total number of instances
        # Shape: (num_classes, )
        self._total_sum: Optional[torch.Tensor] = None
        # the total number of instances under each _predicted_ class,
        # including true positives and false positives
        # Shape: (num_classes, )
        self._pred_sum: Optional[torch.Tensor] = None
        # the total number of instances under each _true_ class,
        # including true positives and false negatives
        # Shape: (num_classes, )
        self._true_sum: Optional[torch.Tensor] = None

    def __call__(self, predictions: torch.Tensor, gold_labels: torch.Tensor) -> None:
        predictions, gold_labels = self.unwrap_to_tensors(predictions, gold_labels)
        if self._predictions_postprocessor is not None:
            predictions = self._predictions_postprocessor.postprocess(predictions)

        num_classes = predictions.size(-1)
        if len(gold_labels.size()) == 1:
            gold_labels = tensor_to_ohe(gold_labels, predictions.size(1))
        assert num_classes == gold_labels.size(-1)

        if self._true_positive_sum is None:
            self._true_positive_sum = torch.zeros(num_classes)
            self._true_sum = torch.zeros(num_classes)
            self._pred_sum = torch.zeros(num_classes)
            self._total_sum = torch.zeros(num_classes)

        true_sum = (gold_labels == 1).sum(dim=0).float()
        true_positive_sum = torch.where(predictions == 1, gold_labels, torch.tensor([0.0])).sum(dim=0)
        pred_sum = (predictions == 1).sum(dim=0).float()

        self._true_positive_sum += true_positive_sum
        self._true_sum += true_sum
        self._pred_sum += pred_sum
        self._total_sum += torch.tensor(len(predictions))

    def get_metric(self, reset: bool = False) -> Dict[str, Union[float, List[float]]]:
        if self._true_positive_sum is None or self._pred_sum is None or self._true_sum is None:
            raise RuntimeError("You never call this metric before.")

        tp_sum = self._true_positive_sum
        pred_sum = self._pred_sum
        true_sum = self._true_sum

        beta2 = self._beta ** 2

        precision = _prf_divide(tp_sum, pred_sum)
        recall = _prf_divide(tp_sum, true_sum)
        fscore = (1 + beta2) * precision * recall / (beta2 * precision + recall)
        fscore[tp_sum == 0] = 0.0

        result_dict: Dict[str, Union[float, List[float]]] = {}

        if self._average == "macro" or self._return_report:
            self._update_for_macro(result_dict=result_dict, precision=precision, recall=recall, fscore=fscore)

        if self._average == "micro" or self._return_report:
            self._update_for_micro(result_dict=result_dict)

        if self._average is None and not self._return_report:
            self._update_for_average_none(result_dict=result_dict, precision=precision, recall=recall, fscore=fscore)

        if self._return_report:
            self._update_for_return_report(result_dict=result_dict, precision=precision, recall=recall, fscore=fscore)

        if reset:
            self.reset()

        return result_dict

    def _update_for_macro(
        self,
        result_dict: Dict[str, Union[float, List[float]]],
        precision: torch.Tensor,
        recall: torch.Tensor,
        fscore: torch.Tensor,
    ) -> None:
        result_dict["macro_precision" if self._return_report else "precision"] = precision.mean().item()
        result_dict["macro_recall" if self._return_report else "recall"] = recall.mean().item()
        result_dict["macro_fscore" if self._return_report else "fscore"] = fscore.mean().item()

    def _update_for_micro(self, result_dict: Dict[str, Union[float, List[float]]]) -> None:

        beta2 = self._beta ** 2

        tp_sum = self._true_positive_sum.sum()  # type: ignore
        pred_sum = self._pred_sum.sum()  # type: ignore
        true_sum = self._true_sum.sum()  # type: ignore

        micro_precision = _prf_divide(tp_sum, pred_sum)
        micro_recall = _prf_divide(tp_sum, true_sum)
        micro_fscore = (1 + beta2) * micro_precision * micro_recall / (beta2 * micro_precision + micro_recall)
        micro_fscore[tp_sum == 0] = 0.0

        result_dict["micro_precision" if self._return_report else "precision"] = micro_precision.item()
        result_dict["micro_recall" if self._return_report else "recall"] = micro_recall.item()
        result_dict["micro_fscore" if self._return_report else "fscore"] = micro_fscore.item()

    def _update_for_return_report(
        self,
        result_dict: Dict[str, Union[float, List[float]]],
        precision: torch.Tensor,
        recall: torch.Tensor,
        fscore: torch.Tensor,
    ) -> None:
        if self.label_names is None:
            self.label_names = [str(i) for i in range(len(fscore))]
        for metric_name, class_values in ("precision", precision), ("recall", recall), ("fscore", fscore):
            for class_name, class_value in zip(self.label_names, class_values):
                result_dict[f"{metric_name}_{class_name}"] = class_value

    @staticmethod
    def _update_for_average_none(
        result_dict: Dict[str, Union[float, List[float]]],
        precision: torch.Tensor,
        recall: torch.Tensor,
        fscore: torch.Tensor,
    ) -> None:
        result_dict["precision"] = precision.tolist()
        result_dict["recall"] = recall.tolist()
        result_dict["fscore"] = fscore.tolist()

    @overrides  # type: ignore
    def reset(self) -> None:
        self._true_positive_sum = None
        self._pred_sum = None
        self._true_sum = None
        self._total_sum = None


def _prf_divide(numerator: torch.Tensor, denominator: torch.Tensor) -> torch.Tensor:
    """Performs division and handles divide-by-zero.
    On zero-division, sets the corresponding result elements to zero.
    """
    result = numerator / denominator
    mask = denominator == 0.0
    if not mask.any():
        return result

    # remove nan
    result[mask] = 0.0
    return result
