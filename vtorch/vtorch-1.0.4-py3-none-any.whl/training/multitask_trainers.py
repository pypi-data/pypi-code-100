import math
from itertools import chain
from typing import Any, Callable, Dict, Generator, Iterable, Iterator, List, Optional, Sequence, Tuple, Union

import numpy as np
import torch
from clearml import Task
from fastprogress import master_bar, progress_bar
from fastprogress.fastprogress import ConsoleProgressBar, NBProgressBar
from torch.cuda.amp import GradScaler, autocast
from torch.nn.modules.loss import _Loss
from torch.optim.lr_scheduler import _LRScheduler

from vtorch.common.utils import lazy_groups_of
from vtorch.data.entity import InstanceFeatureVectors
from vtorch.data.iterators import DataIterator
from vtorch.data.iterators.data_iterator import BaseDataIterator
from vtorch.metrics import Metric
from vtorch.models.model import IModel
from vtorch.nn.utils import move_to_device
from vtorch.training import DistillationTrainer
from vtorch.training.trainers_with_report import TrainerWithFBetaClearMLReport


class MultiTaskTrainer(TrainerWithFBetaClearMLReport):
    train_data: Dict[str, Iterable[InstanceFeatureVectors]]  # type: ignore
    validation_data: Dict[str, Iterable[InstanceFeatureVectors]]  # type: ignore
    iterator: BaseDataIterator  # type: ignore
    validation_iterator: BaseDataIterator  # type: ignore

    def __init__(self, *args: Any, **kwargs: Any):
        self.up_sample: bool = kwargs.pop("up_sample", False)
        self.task_by_task: bool = kwargs.pop("task_by_task", False)
        self.namespace_to_loss_weight: Optional[Dict[str, torch.Tensor]] = kwargs.pop("namespace_to_loss_weight", None)
        self.namespace_to_batch_size: Optional[Dict[str, int]] = kwargs.pop("namespace_to_batch_size", None)
        super(MultiTaskTrainer, self).__init__(*args, **kwargs)
        self.validation_metric_names: List[str] = list(
            chain(
                *[[f"{namespace}_{name}" for name in metric.NAMES] for namespace, metric in self.metrics.items()],
                [f"{namespace}_loss" for namespace in self.metrics.keys()],
            )
        )

    def _configure_batch_iterator(  # type: ignore[override]
        self,
        iterator: BaseDataIterator,
        data: Dict[str, Iterable[InstanceFeatureVectors]],
        master_bar_logger: master_bar,
        shuffle: bool = True,
    ) -> Union[ConsoleProgressBar, NBProgressBar]:

        n_batches = 0
        namespaces = []
        generators: List[Iterator[List[Tuple[Dict[str, Dict[str, torch.Tensor]], Sequence[int]]]]] = []
        instances_per_namespace = []

        _data: Dict[str, List[InstanceFeatureVectors]] = {
            namespace: list(instances) for namespace, instances in data.items()
        }

        if self.up_sample:
            max_instances = max(len(instances) for instances in _data.values())
            for namespace, instances in _data.items():
                to_sample = max_instances - len(instances)  # type: ignore
                up_sampled_instances = np.random.choice(instances, replace=True, size=to_sample).tolist()
                _data[namespace] = instances + up_sampled_instances

        for namespace, instances in _data.items():
            namespaces.append(namespace)
            if self.namespace_to_batch_size is not None:
                iterator._batch_size = self.namespace_to_batch_size[namespace]
            n_batches += iterator.get_num_batches(instances)
            generators.append(lazy_groups_of(iterator(instances, shuffle=shuffle), len(self._cuda_devices)))
            instances_per_namespace.append(len(instances))

        sample_ratios = [n_batch_groups / sum(instances_per_namespace) for n_batch_groups in instances_per_namespace]

        def sample(
            _sample_ratios: List[float]
        ) -> Generator[Tuple[List[Tuple[Dict[str, Dict[str, torch.Tensor]], Sequence[int]]], str], Any, None]:
            namespace_id = 0  # if self.task_by_task
            num_generators = len(generators)
            while generators:

                if self.task_by_task:
                    namespace_id = namespace_id % num_generators
                else:
                    namespace_id = np.random.choice(range(num_generators), p=_sample_ratios)

                try:
                    yield next(iter(generators[namespace_id])), namespaces[namespace_id]
                except StopIteration:
                    generators.pop(namespace_id)
                    namespaces.pop(namespace_id)
                    _sample_ratios.pop(namespace_id)
                    _sample_ratios = [p / sum(_sample_ratios) for p in _sample_ratios]
                    num_generators -= 1

                namespace_id += 1  # if self.task_by_task

        n_batches = math.ceil(n_batches / len(self._cuda_devices))

        return progress_bar(sample(sample_ratios), total=n_batches, parent=master_bar_logger, leave=False)

    def _batch_outputs_and_loss(  # type: ignore[override]
        self, batch_group: Tuple[Tuple[List[Dict[str, Dict[str, torch.Tensor]]], Sequence[int]], str]
    ) -> Tuple[torch.Tensor, torch.Tensor, str]:

        if len(batch_group[0]) != 1:
            raise NotImplementedError("Distributed training is not supported")
        batch, _ = batch_group[0][0]
        namespace = batch_group[1]
        batch = move_to_device(batch, self._cuda_devices[0])

        with autocast(enabled=self.scaler is not None):
            model_outputs, loss = self.model(namespaces=[namespace], **batch)

        if self.namespace_to_loss_weight is not None:
            loss = loss * self.namespace_to_loss_weight[namespace]

        if self.accumulation_steps > 1:
            loss = loss / self.accumulation_steps

        return model_outputs, loss, namespace

    def _calculate_metrics(  # type: ignore[override]
        self,
        outputs: torch.Tensor,
        batch_group: Tuple[Tuple[List[Dict[str, Dict[str, torch.Tensor]]], Sequence[int]], str],
    ) -> None:

        batch, _ = batch_group[0][0]
        namespace = batch_group[1]
        label_field_name, label_vector_name = self.label_keys
        if isinstance(label_vector_name, list):
            raise NotImplementedError("Measuring metric with more than one label vectors is not implemented")
        labels = batch[label_field_name][label_vector_name]
        for metric_name, metric in self.metrics.items():
            if namespace in metric_name:
                metric(outputs, labels)

    def _form_metric_dict(  # type: ignore[override]
        self, total_loss: Dict[str, float], num_batches: Dict[str, int], reset: bool
    ) -> Dict[str, float]:

        metrics_to_return = {
            f"{namespace}_loss": total_loss[namespace] / num_batches[namespace] if num_batches[namespace] > 0 else 0.0
            for namespace in total_loss.keys()
        }
        for namespace, metric in self.metrics.items():
            for metric_name, metric_value in metric.get_metric(reset).items():
                if isinstance(metric_value, list):
                    for i, value in enumerate(metric_value):
                        metrics_to_return[f"{namespace}_{metric_name}_{i}"] = value
                else:
                    metrics_to_return[f"{namespace}_{metric_name}"] = metric_value  # type: ignore
        return metrics_to_return

    def _train_epoch(
        self, master_bar_logger: master_bar, epoch: int, global_steps: int = 0
    ) -> Tuple[Dict[str, float], int]:
        """
        Trains one epoch and returns metrics.
        """
        train_losses = dict.fromkeys(self.train_data.keys(), 0.0)
        # Set the model to "train" mode.
        self._train_mode()

        batches_this_epoch = dict.fromkeys(self.train_data.keys(), 0)

        for batch_group in self._configure_batch_iterator(
            iterator=self.iterator, data=self.train_data, master_bar_logger=master_bar_logger
        ):

            outputs, loss, namespace = self._batch_outputs_and_loss(batch_group)
            self._calculate_metrics(outputs=outputs, batch_group=batch_group)

            batches_this_epoch[namespace] += 1

            if torch.isnan(loss):
                raise ValueError("nan loss encountered")

            self._backward(loss)

            train_losses[namespace] += loss.item()
            if sum(batches_this_epoch.values()) % self.accumulation_steps == 0:
                self._step()
                self.model.zero_grad()

                self.callbacks.clearml_report_scalar(
                    title="Training", series=f"{namespace}_loss", value=loss.item(), iteration=global_steps
                )

                global_steps += 1

                master_bar_logger.child.comment = "{} loss: {:.4f}".format(
                    namespace, train_losses[namespace] / batches_this_epoch[namespace]
                )

            if (
                self.run_validation_each_global_steps is not None
                and (global_steps + 1) % self.run_validation_each_global_steps == 0
            ):
                self._validation_run(master_bar_logger=master_bar_logger, global_steps=global_steps)
                self._train_mode()

        metrics = self._form_metric_dict(total_loss=train_losses, num_batches=batches_this_epoch, reset=True)
        return metrics, global_steps

    def _validation_run(self, master_bar_logger: master_bar, global_steps: int = 0) -> Optional[Dict[str, float]]:
        """
        Computes the validation metrics. Returns it and the number of batches.
        """
        if self.validation_data is None:
            return None

        with torch.no_grad():
            self._eval_mode()
            batches_this_epoch = dict.fromkeys(self.train_data.keys(), 0)
            val_losses = dict.fromkeys(self.train_data.keys(), 0.0)
            for batch_group in self._configure_batch_iterator(
                iterator=self.validation_iterator,
                data=self.validation_data,
                master_bar_logger=master_bar_logger,
                shuffle=False,
            ):
                outputs, loss, namespace = self._batch_outputs_and_loss(batch_group)
                self._calculate_metrics(outputs=outputs, batch_group=batch_group)
                batches_this_epoch[namespace] += 1
                val_losses[namespace] += loss.detach().cpu().numpy()

            val_metrics = self._form_metric_dict(total_loss=val_losses, num_batches=batches_this_epoch, reset=True)

        for metric_name, metric_value in val_metrics.items():
            self.callbacks.clearml_report_scalar(
                title="Validation", series=metric_name, value=metric_value, iteration=global_steps
            )

        # TODO: restrict type of self.callbacks.early_stopping
        val_metrics[self.callbacks.early_stopping.metric_name] = sum(  # type: ignore
            value
            for name, value in val_metrics.items()
            if self.callbacks.early_stopping.metric_name in name  # type: ignore
        )  # for early stopping

        return val_metrics


class DoubleTeacherDistillationTrainer(DistillationTrainer, MultiTaskTrainer):
    def __init__(
        self,
        student_model: IModel,
        teacher_model: torch.nn.ModuleDict,
        optimizer: torch.optim.Optimizer,
        metrics: Dict[str, Metric],
        label_keys: Tuple[str, Union[str, List[str]]],
        iterator: DataIterator,
        train_dataset: Dict[str, Iterable[InstanceFeatureVectors]],
        num_epochs: int,
        shuffle: bool = True,
        validation_dataset: Optional[Dict[str, Iterable[InstanceFeatureVectors]]] = None,
        validation_iterator: Optional[DataIterator] = None,
        early_stopping: bool = False,
        patience: Optional[int] = None,
        early_stopping_metric_name: str = "loss",
        early_stopping_metric_should_decrease: bool = True,
        accumulation_steps: int = 1,
        cuda_device: Union[int, List[int]] = -1,
        grad_norm: Optional[float] = 1.0,
        lr_scheduler: Optional[_LRScheduler] = None,
        scaler: Optional[GradScaler] = None,
        gradual_unfreezing_steps: Optional[List[List[str]]] = None,
        run_validation_each_global_steps: Optional[int] = None,
        clearml_task: Optional[Task] = None,
        seed: int = 12,
        comparison_loss: Optional[_Loss] = None,
        logits_postprocessing: Optional[Callable[[torch.Tensor], torch.Tensor]] = None,
        comparison_loss_weight: float = 0.5,
        other_teacher_preds_loss_weight: float = 0.0,
        up_sample: bool = False,
        task_by_task: bool = False,
        namespace_to_loss_weight: Optional[Dict[str, Union[float, torch.Tensor]]] = None,
    ) -> None:

        super(DistillationTrainer, self).__init__(
            model=student_model,
            optimizer=optimizer,
            metrics=metrics,
            label_keys=label_keys,
            iterator=iterator,
            train_dataset=train_dataset,
            num_epochs=num_epochs,
            shuffle=shuffle,
            validation_dataset=validation_dataset,
            validation_iterator=validation_iterator,
            early_stopping=early_stopping,
            patience=patience,
            early_stopping_metric_name=early_stopping_metric_name,
            early_stopping_metric_should_decrease=early_stopping_metric_should_decrease,
            accumulation_steps=accumulation_steps,
            cuda_device=cuda_device,
            grad_norm=grad_norm,
            lr_scheduler=lr_scheduler,
            scaler=scaler,
            gradual_unfreezing_steps=gradual_unfreezing_steps,
            run_validation_each_global_steps=run_validation_each_global_steps,
            clearml_task=clearml_task,
            seed=seed,
            up_sample=up_sample,
            task_by_task=task_by_task,
            namespace_to_loss_weight=namespace_to_loss_weight,
        )

        # DistillationTrainer __init__ without "distillation" tag
        self.teacher_model = teacher_model
        if self._cuda_devices[0] >= 0:
            self.teacher_model.to(torch.device(f"cuda:{self._cuda_devices[0]}"))
        self.teacher_model.eval()
        self.comparison_loss_weight = comparison_loss_weight
        if comparison_loss is None:
            comparison_loss = torch.nn.MSELoss()
        self.comparison_loss = comparison_loss
        self.logits_postprocessing = logits_postprocessing

        if self.comparison_loss_weight + other_teacher_preds_loss_weight >= 1:
            # (if == 1 -> we wont take into account loss with ground truth labels)
            raise ValueError("comparison_loss_weight + other_teacher_preds_loss_weight must be less than 1.0")
        self.other_teacher_preds_loss_weight = other_teacher_preds_loss_weight

    def _batch_outputs_and_loss(  # type: ignore[override]
        self, batch_group: Tuple[Tuple[List[Dict[str, Dict[str, torch.Tensor]]], Sequence[int]], str]
    ) -> Tuple[torch.Tensor, torch.Tensor, str]:

        if len(batch_group[0]) != 1:
            raise NotImplementedError("Distributed training is not supported")
        batch, _ = batch_group[0][0]
        namespace = batch_group[1]
        batch = move_to_device(batch, self._cuda_devices[0])

        with autocast(enabled=self.scaler is not None):
            student_outputs, ground_truth_loss = self.model(namespaces=[namespace], **batch)

        this_task_teacher_preds_comparison_loss = self._compute_this_task_teacher_preds_comparison_loss(
            namespace=namespace, batch=batch, student_outputs=student_outputs
        )

        if self.other_teacher_preds_loss_weight > 0:
            other_teachers_preds_comparison_loss = self._compute_other_teachers_preds_comparison_losses(
                namespace=namespace, batch=batch, student_outputs=student_outputs
            )

            loss = (
                self.comparison_loss_weight * this_task_teacher_preds_comparison_loss
                + self.other_teacher_preds_loss_weight * other_teachers_preds_comparison_loss
                + (1 - self.comparison_loss_weight + self.other_teacher_preds_loss_weight) * ground_truth_loss
            )

        else:
            loss = (
                self.comparison_loss_weight * this_task_teacher_preds_comparison_loss
                + (1 - self.comparison_loss_weight) * ground_truth_loss
            )

        if self.accumulation_steps > 1:
            loss = loss / self.accumulation_steps

        return student_outputs[:, self.model.namespace_to_outputs()[namespace]], loss, namespace

    def _compute_this_task_teacher_preds_comparison_loss(
        self, namespace: str, batch: Dict[str, Dict[str, torch.Tensor]], student_outputs: torch.Tensor
    ) -> torch.Tensor:
        with torch.no_grad():
            this_task_teacher_preds = self.teacher_model[namespace](
                **{argument: tensors_dict for argument, tensors_dict in batch.items() if argument != "labels"}
            )[0]

        this_task_teacher_preds_comparison_loss = self.comparison_loss(
            student_outputs[:, self.model.namespace_to_outputs()[namespace]], this_task_teacher_preds
        )

        return this_task_teacher_preds_comparison_loss

    def _compute_other_teachers_preds_comparison_losses(
        self, namespace: str, batch: Dict[str, Dict[str, torch.Tensor]], student_outputs: torch.Tensor
    ) -> torch.Tensor:
        with torch.no_grad():
            other_teachers_preds = {
                _namespace: model(
                    **{argument: tensors_dict for argument, tensors_dict in batch.items() if argument != "labels"}
                )[0]
                for _namespace, model in self.teacher_model.items()
                if _namespace != namespace
            }

        other_teachers_preds_comparison_losses = [
            self.comparison_loss(student_outputs[:, self.model.namespace_to_outputs()[_namespace]], preds)
            for _namespace, preds in other_teachers_preds.items()
        ]

        if len(other_teachers_preds_comparison_losses) == 1:
            other_teachers_preds_comparison_loss = other_teachers_preds_comparison_losses[0]
        else:
            # TODO: mean?
            other_teachers_preds_comparison_loss = torch.sum(torch.tensor(other_teachers_preds_comparison_losses))

        return other_teachers_preds_comparison_loss


class DoubleTeacherTinyDistillationTrainer(DoubleTeacherDistillationTrainer):
    def _batch_outputs_and_loss(  # type: ignore[override]
        self, batch_group: Tuple[Tuple[List[Dict[str, Dict[str, torch.Tensor]]], Sequence[int]], str]
    ) -> Tuple[torch.Tensor, torch.Tensor, str]:

        if len(batch_group[0]) != 1:
            raise NotImplementedError("Distributed training is not supported")
        batch, _ = batch_group[0][0]
        namespace = batch_group[1]
        batch = move_to_device(batch, self._cuda_devices[0])

        with autocast(enabled=self.scaler is not None):
            student_outputs, ground_truth_loss, student_hidden_states, student_attentions = self.model(
                namespaces=[namespace], **batch
            )

        this_task_teacher_preds_comparison_loss = self._compute_this_task_teacher_preds_comparison_loss(
            namespace=namespace,
            batch=batch,
            student_outputs=student_outputs,
            student_hidden_states=student_hidden_states,
            student_attentions=student_attentions,
        )

        if self.other_teacher_preds_loss_weight > 0:
            other_teachers_preds_comparison_loss = self._compute_other_teachers_preds_comparison_losses(
                namespace=namespace,
                batch=batch,
                student_outputs=student_outputs,
                student_hidden_states=student_hidden_states,
                student_attentions=student_attentions,
            )

            loss = (
                self.comparison_loss_weight * this_task_teacher_preds_comparison_loss
                + self.other_teacher_preds_loss_weight * other_teachers_preds_comparison_loss
                + (1 - self.comparison_loss_weight + self.other_teacher_preds_loss_weight) * ground_truth_loss
            )

        else:
            loss = (
                self.comparison_loss_weight * this_task_teacher_preds_comparison_loss
                + (1 - self.comparison_loss_weight) * ground_truth_loss
            )

        if self.accumulation_steps > 1:
            loss = loss / self.accumulation_steps

        return student_outputs[:, self.model.namespace_to_outputs()[namespace]], loss, namespace

    def _compute_this_task_teacher_preds_comparison_loss(
        self,
        namespace: str,
        batch: Dict[str, Dict[str, torch.Tensor]],
        student_outputs: torch.Tensor,
        student_hidden_states: Optional[Tuple[torch.Tensor, ...]] = None,
        student_attentions: Optional[Tuple[torch.Tensor, ...]] = None,
    ) -> torch.Tensor:

        if student_hidden_states is None or student_attentions is None:
            raise ValueError("provide 'student_hidden_states' and 'student_attentions' arguments")

        with torch.no_grad():
            teacher_preds, _, teacher_hidden_states, teacher_attentions = self.teacher_model[namespace](
                **{argument: tensors_dict for argument, tensors_dict in batch.items() if argument != "labels"}
            )

        teacher_preds_comparison_loss = self.comparison_loss(
            student_outputs[:, self.model.namespace_to_outputs()[namespace]], teacher_preds
        )

        teacher_chosen_layer_ids = self._choose_teacher_layer_ids(student_attentions, teacher_attentions)

        teacher_hidden_states_comparison_loss = self._compute_hidden_states_loss(
            student_hidden_states=student_hidden_states,
            teacher_hidden_states=teacher_hidden_states,
            teacher_chosen_layer_ids=teacher_chosen_layer_ids,
        )

        teacher_attention_comparison_loss = self._compute_attention_loss(
            student_attentions=student_attentions,
            teacher_attentions=teacher_attentions,
            teacher_chosen_layer_ids=teacher_chosen_layer_ids,
        )

        return (
            teacher_preds_comparison_loss + teacher_hidden_states_comparison_loss + teacher_attention_comparison_loss
        )

    def _compute_other_teachers_preds_comparison_losses(
        self,
        namespace: str,
        batch: Dict[str, Dict[str, torch.Tensor]],
        student_outputs: torch.Tensor,
        student_hidden_states: Optional[Tuple[torch.Tensor, ...]] = None,
        student_attentions: Optional[Tuple[torch.Tensor, ...]] = None,
    ) -> torch.Tensor:

        if student_hidden_states is None or student_attentions is None:
            raise ValueError("provide 'student_hidden_states' and 'student_attentions' arguments")

        with torch.no_grad():
            other_teachers_outputs = {
                _namespace: model(
                    **{argument: tensors_dict for argument, tensors_dict in batch.items() if argument != "labels"}
                )
                for _namespace, model in self.teacher_model.items()
                if _namespace != namespace
            }

        logits_id = 0
        hidden_states_id = 2
        attentions_id = 3

        teachers_preds_comparison_losses = [
            self.comparison_loss(student_outputs[:, self.model.namespace_to_outputs()[_namespace]], outputs[logits_id])
            for _namespace, outputs in other_teachers_outputs.items()
        ]

        teacher_chosen_layer_ids = self._choose_teacher_layer_ids(
            student_attentions, next(iter(other_teachers_outputs.values()))[attentions_id]  # type: ignore
        )

        teachers_hidden_states_comparison_losses = [
            self._compute_hidden_states_loss(
                student_hidden_states=student_hidden_states,
                teacher_hidden_states=outputs[hidden_states_id],
                teacher_chosen_layer_ids=teacher_chosen_layer_ids,
            )
            for _namespace, outputs in other_teachers_outputs.items()
        ]

        teachers_attention_comparison_losses = [
            self._compute_attention_loss(
                student_attentions=student_attentions,
                teacher_attentions=outputs[attentions_id],
                teacher_chosen_layer_ids=teacher_chosen_layer_ids,
            )
            for _namespace, outputs in other_teachers_outputs.items()
        ]

        if len(teachers_preds_comparison_losses) == 1:
            teachers_preds_comparison_loss = teachers_preds_comparison_losses[0]
            teachers_hidden_states_comparison_loss = teachers_hidden_states_comparison_losses[0]
            teachers_attention_comparison_loss = teachers_attention_comparison_losses[0]
        else:
            # TODO: mean?
            teachers_preds_comparison_loss = torch.sum(torch.tensor(teachers_preds_comparison_losses))
            teachers_hidden_states_comparison_loss = torch.sum(torch.tensor(teachers_hidden_states_comparison_losses))
            teachers_attention_comparison_loss = torch.sum(torch.tensor(teachers_attention_comparison_losses))

        return (
            teachers_preds_comparison_loss
            + teachers_hidden_states_comparison_loss
            + teachers_attention_comparison_loss
        )

    def _compute_attention_loss(
        self,
        student_attentions: Tuple[torch.Tensor, ...],
        teacher_attentions: Tuple[torch.Tensor, ...],
        teacher_chosen_layer_ids: Iterable[int],
    ) -> torch.Tensor:

        _teacher_attentions = [teacher_attentions[i] for i in teacher_chosen_layer_ids]

        _teacher_attentions = torch.cat(_teacher_attentions, dim=0)
        student_attentions = torch.cat(student_attentions, dim=0)

        _teacher_attentions = torch.where(  # type: ignore
            _teacher_attentions <= -1e2,  # type: ignore
            torch.zeros_like(_teacher_attentions, device=self._cuda_devices[0]),
            _teacher_attentions,
        )

        student_attentions = torch.where(  # type: ignore
            student_attentions <= -1e2,  # type: ignore
            torch.zeros_like(student_attentions).to(self._cuda_devices[0]),
            student_attentions,
        )

        return self.comparison_loss(_teacher_attentions, student_attentions)

    def _compute_hidden_states_loss(
        self,
        student_hidden_states: Tuple[torch.Tensor, ...],
        teacher_hidden_states: Tuple[torch.Tensor, ...],
        teacher_chosen_layer_ids: Iterable[int],
    ) -> torch.Tensor:
        # the first element of hidden_states - embeddings, so, we take them and shift layer ids by 1
        _teacher_hidden_states = [teacher_hidden_states[0]] + [
            teacher_hidden_states[i + 1] for i in teacher_chosen_layer_ids
        ]

        _teacher_hidden_states = torch.cat(_teacher_hidden_states, dim=0)
        student_hidden_states = torch.cat(student_hidden_states, dim=0)

        return self.comparison_loss(_teacher_hidden_states, student_hidden_states)

    @staticmethod
    def _choose_teacher_layer_ids(
        student_attentions: Tuple[torch.Tensor, ...], teacher_attentions: Tuple[torch.Tensor, ...]
    ) -> Iterable[int]:
        teacher_layer_num = len(teacher_attentions)
        student_layer_num = len(student_attentions)
        if not teacher_layer_num % student_layer_num == 0:
            raise ValueError("The number of the student model layers must be divisible by number of teacher the model")
        layers_per_block = int(teacher_layer_num / student_layer_num)
        return range(layers_per_block - 1, teacher_layer_num, layers_per_block)
