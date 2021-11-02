import logging
from contextlib import contextmanager
from typing import Callable, Dict, Iterable, Iterator, List, Optional, Sequence, Tuple, Union

import torch
from clearml import Task
from torch.cuda.amp import GradScaler, autocast
from torch.nn.modules.loss import _Loss
from torch.optim.lr_scheduler import _LRScheduler

from vtorch.nn import utils as nn_util

from ..data.entity import InstanceFeatureVectors  # noqa: F401
from ..data.iterators.base import DataIterator
from ..metrics import Metric
from ..models.model import IModel
from .trainer import Trainer

logger = logging.getLogger(__name__)


class DistillationTrainer(Trainer):
    def __init__(
        self,
        student_model: IModel,
        teacher_model: torch.nn.Module,  # as teacher model will not be saved, there is no need to use IModel
        optimizer: torch.optim.Optimizer,  # type: ignore
        metrics: Dict[str, Metric],
        label_keys: Tuple[str, Union[str, List[str]]],
        iterator: DataIterator,
        train_dataset: Iterable[InstanceFeatureVectors],
        num_epochs: int,
        shuffle: bool = True,
        validation_dataset: Optional[Iterable[InstanceFeatureVectors]] = None,
        validation_iterator: Optional[DataIterator] = None,
        early_stopping: bool = False,
        patience: Optional[int] = None,
        early_stopping_metric_name: str = "loss",
        early_stopping_metric_should_decrease: bool = True,
        accumulation_steps: int = 1,
        cuda_device: Union[int, List[int]] = -1,
        grad_norm: Optional[float] = 1.0,
        lr_scheduler: Optional[_LRScheduler] = None,  # type: ignore
        scaler: Optional[GradScaler] = None,
        gradual_unfreezing_steps: Optional[List[List[str]]] = None,
        run_validation_each_global_steps: Optional[int] = None,
        clearml_task: Optional[Task] = None,
        seed: int = 12,
        comparison_loss: Optional[_Loss] = None,
        logits_postprocessing: Optional[Callable[[torch.Tensor], torch.Tensor]] = None,
        comparison_loss_weight: float = 0.5,
    ) -> None:

        super().__init__(
            model=student_model,
            optimizer=optimizer,
            metrics=metrics,
            iterator=iterator,
            train_dataset=train_dataset,
            num_epochs=num_epochs,
            shuffle=shuffle,
            validation_dataset=validation_dataset,
            validation_iterator=validation_iterator,
            early_stopping=early_stopping,
            patience=patience,
            label_keys=label_keys,
            accumulation_steps=accumulation_steps,
            cuda_device=cuda_device,
            grad_norm=grad_norm,
            lr_scheduler=lr_scheduler,
            early_stopping_metric_name=early_stopping_metric_name,
            early_stopping_metric_should_decrease=early_stopping_metric_should_decrease,
            seed=seed,
            scaler=scaler,
            gradual_unfreezing_steps=gradual_unfreezing_steps,
            run_validation_each_global_steps=run_validation_each_global_steps,
            clearml_task=clearml_task,
        )

        self.teacher_model = teacher_model
        self.teacher_model.eval()
        self.comparison_loss_weight = comparison_loss_weight
        if comparison_loss is None:
            logger.warning("No `comparison loss was given to a trainer. Defaulting to `torch.nn.MSELoss()`")
            comparison_loss = torch.nn.MSELoss()
        self.comparison_loss = comparison_loss
        self.logits_postprocessing = logits_postprocessing

    def _batch_outputs_and_loss(
        self, batch_group: List[Tuple[Dict[str, Dict[str, torch.Tensor]], Sequence[int]]]
    ) -> Sequence[torch.Tensor]:
        # to not scale by self.accumulation_steps loss twice
        with self._no_accumulation_steps():
            logits_student, loss = super(DistillationTrainer, self)._batch_outputs_and_loss(batch_group=batch_group)

        logits_teacher = self._teacher_forward(batch_group)

        if self.logits_postprocessing is not None:
            logits_student = self.logits_postprocessing(logits_student)
            logits_teacher = self.logits_postprocessing(logits_teacher)

        loss_comparison = self.comparison_loss(logits_student, logits_teacher)

        loss = self.comparison_loss_weight * loss_comparison + (1 - self.comparison_loss_weight) * loss

        if self.accumulation_steps > 1:
            loss = loss / self.accumulation_steps

        return logits_student, loss

    def _teacher_forward(
        self, batch_group: List[Tuple[Dict[str, Dict[str, torch.Tensor]], Sequence[int]]]
    ) -> torch.Tensor:
        if len(batch_group) != 1:
            raise NotImplementedError("Distributed training is not supported")
        batch, _ = batch_group[0]
        batch = nn_util.move_to_device(batch, self._cuda_devices[0])

        with torch.no_grad():  # no autocast here
            # we will avoid loss computation for teacher_model
            model_outputs, _ = self.teacher_model(**{k: v for k, v in batch.items() if k != self.label_keys[0]})

        return model_outputs

    @contextmanager
    def _no_accumulation_steps(self) -> Iterator[None]:
        accumulation_steps = self.accumulation_steps
        self.accumulation_steps = 1
        yield
        self.accumulation_steps = accumulation_steps


class TinyBertStyleDistillation(DistillationTrainer):
    def _batch_outputs_and_loss(
        self, batch_group: List[Tuple[Dict[str, Dict[str, torch.Tensor]], Sequence[int]]]
    ) -> Sequence[torch.Tensor]:

        student_output = self._extended_student_forward(batch_group=batch_group)
        student_logits, student_loss, student_layers_hidden_states, student_attention_matrices = student_output

        teacher_output = self._extended_teacher_forward(batch_group)
        teacher_logits, teacher_layers_hidden_states, teacher_attention_matrices = teacher_output

        if self.logits_postprocessing is not None:
            student_logits = self.logits_postprocessing(student_logits)
            teacher_logits = self.logits_postprocessing(teacher_logits)

        logits_loss = self.comparison_loss(student_logits, teacher_logits)

        teacher_layer_ids = self._choose_teacher_layer_ids(
            teacher_layer_num=len(teacher_attention_matrices), student_layer_num=len(student_attention_matrices)
        )

        attention_loss = self._compute_attention_loss(
            student_attentions=student_attention_matrices,
            teacher_attentions=teacher_attention_matrices,
            teacher_chosen_layer_ids=teacher_layer_ids,
        )

        hidden_states_loss = self._compute_hidden_states_loss(
            student_hidden_states=student_layers_hidden_states,
            teacher_hidden_states=teacher_layers_hidden_states,
            teacher_chosen_layer_ids=teacher_logits,
        )

        loss = (
            self.comparison_loss_weight * (logits_loss + attention_loss + hidden_states_loss)
            + (1 - self.comparison_loss_weight) * student_loss
        )

        if self.accumulation_steps > 1:
            loss = loss / self.accumulation_steps

        return student_logits, loss

    def _extended_teacher_forward(
        self, batch_group: List[Tuple[Dict[str, Dict[str, torch.Tensor]], Sequence[int]]]
    ) -> Tuple[torch.Tensor, Tuple[torch.Tensor, ...], Tuple[torch.Tensor, ...]]:
        if len(batch_group) != 1:
            raise NotImplementedError("Distributed training is not supported")
        batch, _ = batch_group[0]
        batch = nn_util.move_to_device(batch, self._cuda_devices[0])

        with torch.no_grad():  # no autocast here
            logits, _, layers_hidden_states, layers_attention_matrices = self.teacher_model(
                **{k: v for k, v in batch.items() if k != self.label_keys[0]}
            )

        return logits, layers_hidden_states, layers_attention_matrices

    def _extended_student_forward(
        self, batch_group: List[Tuple[Dict[str, Dict[str, torch.Tensor]], Sequence[int]]]
    ) -> Tuple[torch.Tensor, torch.Tensor, Tuple[torch.Tensor, ...], Tuple[torch.Tensor, ...]]:
        if len(batch_group) != 1:
            raise NotImplementedError("Distributed training is not supported")
        batch, _ = batch_group[0]
        batch = nn_util.move_to_device(batch, self._cuda_devices[0])

        with autocast(enabled=self.scaler is not None):
            logits, loss, layers_hidden_states, layers_attention_matrices = self.model(**batch)

        return logits, loss, layers_hidden_states, layers_attention_matrices

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
            torch.zeros_like(student_attentions, device=self._cuda_devices[0]),
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
    def _choose_teacher_layer_ids(teacher_layer_num: int, student_layer_num: int) -> List[int]:
        if not teacher_layer_num % student_layer_num == 0:
            raise ValueError("The number of the student model layers must be divisible by number of teacher the model")
        layers_per_block = int(teacher_layer_num / student_layer_num)
        return list(range(layers_per_block - 1, teacher_layer_num, layers_per_block))
