from copy import deepcopy
from typing import Dict, List, Sequence, Tuple

import pandas as pd
import torch
from fastprogress import master_bar

from vtorch.common.utils import set_seed
from vtorch.metrics.fbeta_measure_with_report import FBetaMeasureWithClearMLReport
from vtorch.nn.utils import move_to_device
from vtorch.training import Trainer


class TrainerWithFBetaClearMLReport(Trainer):

    metrics: Dict[str, FBetaMeasureWithClearMLReport]  # type: ignore

    def _get_labels_from_batch(
        self, batch_group: List[Tuple[Dict[str, Dict[str, torch.Tensor]], Sequence[int]]]
    ) -> torch.Tensor:
        batch, _ = batch_group[0]
        label_field_name, label_vector_name = self.label_keys
        if isinstance(label_vector_name, list):
            raise NotImplementedError("Measuring metric with more than one label vectors is not implemented")
        return move_to_device(batch[label_field_name][label_vector_name], self._cuda_devices[0])

    def _calculate_metrics(
        self, outputs: torch.Tensor, batch_group: List[Tuple[Dict[str, Dict[str, torch.Tensor]], Sequence[int]]]
    ) -> None:
        labels = self._get_labels_from_batch(batch_group)

        for metric in self.metrics.values():
            metric(outputs, labels)

    def train(self) -> torch.nn.Module:
        """
        Trains the supplied model with the supplied parameters.
        """
        global_steps = 0
        mb = master_bar(range(self.num_epochs))
        mb.first_bar.comment = f"{self.model.__class__.__name__} training"
        mb_elements = ["epoch"] + [f"train_{metrics_name}" for metrics_name in self.validation_metric_names]
        if self.validation_data is not None:
            mb_elements.extend([f"val_{metrics_name}" for metrics_name in self.validation_metric_names])

        best_reports: Dict[str, pd.DataFrame] = {}

        mb.write(mb_elements, table=True)
        set_seed(self.seed, len(self._cuda_devices))
        best_model = self.model
        for epoch in mb:
            mb_results = [str(epoch)]
            self._gradual_unfreezing(epoch)

            train_metrics, global_steps = self._train_epoch(mb, epoch, global_steps=global_steps)
            mb_results.extend(["{:.4f}".format(train_metrics[metric]) for metric in self.validation_metric_names])
            for metric_name, metric_value in train_metrics.items():
                self.callbacks.clearml_report_scalar(
                    title="Training", series=metric_name, value=metric_value, iteration=global_steps
                )

            val_metrics = self._validation_run(mb, global_steps=global_steps)
            if val_metrics is not None:
                self.callbacks.add_metric(val_metrics)
                mb_results.extend(["{:.4f}".format(val_metrics[metric]) for metric in self.validation_metric_names])

            mb.write(mb_results, table=True)

            if self.callbacks.should_stop_early():
                break
            elif self.callbacks.is_best_so_far():
                best_model = deepcopy(self.model).cpu()
                for metric_name, metric in self.metrics.items():
                    best_reports[f"{metric_name}_report"] = metric.report

        for name, artifact_object in best_reports.items():
            self.callbacks.clearml_upload_artifact(name=name, artifact_object=artifact_object)

        return best_model
