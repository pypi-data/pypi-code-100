import warnings
from abc import ABC
from typing import Dict, Optional

import torch


class PredictionPostprocessorI(object):
    def postprocess(self, logits: torch.Tensor) -> torch.Tensor:
        raise NotImplementedError()


class PredictionPostprocessor(PredictionPostprocessorI, ABC):
    def __init__(
        self,
        label_to_index: Dict[str, int],
        named_thresholds: Optional[Dict[str, float]] = None,
        default_threshold: float = 0.5,
    ):
        self._default_threshold = default_threshold
        self._named_thresholds = named_thresholds or {}
        self.thresholds: Optional[torch.Tensor] = None
        self._set_thresholds(label_to_index=label_to_index)

    def _set_thresholds(self, label_to_index: Dict[str, int]) -> None:
        self._label_to_index = label_to_index
        self.thresholds = torch.ones(1, len(self._label_to_index)) * self._default_threshold

        if len(self._named_thresholds) > 0:
            labels_set = set(self._label_to_index.keys())
            named_set = set(self._named_thresholds.keys())
            missing_labels = labels_set.difference(named_set)
            if len(missing_labels) > 0:
                warnings.warn(
                    f"You have not set threshold for the following labels: {missing_labels}\n"
                    f"A default value of {self._default_threshold} will be set",
                    RuntimeWarning,
                )

            wrong_label_names = named_set.difference(labels_set)
            if len(wrong_label_names) > 0:
                raise KeyError(
                    f"The following named_thresholds you have specified are absent in the vocabulary "
                    f"label namespace: {wrong_label_names}"
                )

        for name, value in self._named_thresholds.items():
            if name in self._label_to_index:
                self.thresholds[0, self._label_to_index[name]] = value
