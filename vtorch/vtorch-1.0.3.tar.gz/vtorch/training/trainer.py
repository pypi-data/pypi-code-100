import logging
import math
from copy import deepcopy
from itertools import chain
from typing import Dict, Iterable, List, Optional, Sequence, Tuple, Union

import torch
from clearml import Task
from fastprogress import master_bar, progress_bar
from fastprogress.fastprogress import ConsoleProgressBar, NBProgressBar
from torch.cuda.amp import GradScaler, autocast
from torch.optim.lr_scheduler import _LRScheduler

from vtorch.common.checks import ConfigurationError
from vtorch.common.utils import lazy_groups_of, set_seed
from vtorch.data.iterators.base import DataIterator, InstanceFeatureVectors
from vtorch.metrics import Metric
from vtorch.models.model import IModel
from vtorch.nn import utils as nn_util
from vtorch.training.callbacks import Callbacks, ClearMLReporter, EarlyStopping
from vtorch.training.trainer_base import TrainerBase

from .callbacks.clearml_reporter import ClearMLReporterI, ClearMLReporterNull
from .callbacks.early_stopping import EarlyStoppingI, EarlyStoppingNull

logger = logging.getLogger(__name__)


class Trainer(TrainerBase):
    def __init__(
        self,
        model: IModel,
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
    ) -> None:
        """
        A trainer for doing supervised learning. It just takes a labeled dataset
        and a ``DataIterator``, and uses the supplied ``Optimizer`` to learn the weights
        for your model over some fixed number of epochs. You can also pass in a validation
        dataset and enable early stopping. There are many other bells and whistles as well.

        Parameters
        ----------
        model : ``Model``, required.
            An Vtorch model to be optimized. Pytorch Modules can also be optimized if
            their ``forward`` method returns a dictionary with a "loss" key, containing a
            scalar tensor representing the loss function to be optimized.
            If you are training your model using GPUs, your model should already be
            on the correct device.
        optimizer : ``torch.nn.Optimizer``, required.
            An instance of a Pytorch Optimizer, instantiated with the parameters of the
            model to be optimized.
        iterator : ``DataIterator``, required.
            A method for iterating over a ``Dataset``, yielding padded indexed batches.
        train_dataset : ``Dataset``, required.
            A ``Dataset`` to train on. The dataset should have already been indexed.
        validation_dataset : ``Dataset``, optional, (default = None).
            A ``Dataset`` to evaluate on. The dataset should have already been indexed.
        patience : Optional[int] > 0, optional (default=None)
            Number of epochs to be patient before early stopping: the training is stopped
            after ``patience`` epochs with no improvement. If given, it must be ``> 0``.
            If None, early stopping is disabled.
        validation_iterator : ``DataIterator``, optional (default=None)
            An iterator to use for the validation set.  If ``None``, then
            use the training `iterator`.
        shuffle : ``bool``, optional (default=True)
            Whether to shuffle the instances in the iterator or not.
        num_epochs : int, optional (default = 20)
            Number of training epochs.
        accumulation_steps : int, optional (default = 0)
            Number of training steps to accumulate gradients
        cuda_device : ``Union[int, List[int]]``, optional (default = -1)
            An integer or list of integers specifying the CUDA device(s) to use. If -1, the CPU is used.
        grad_norm : ``float``, optional, (default = None).
            If provided, gradient norms will be rescaled to have a maximum of this value.
        clearml_task: ``Task``, optional  (default = None)
        """
        if isinstance(cuda_device, list) and len(cuda_device) > 1:
            raise NotImplementedError("Distributed training is not supported")

        if patience is not None and (not isinstance(patience, int) or patience <= 0):
            raise ConfigurationError(
                f'{patience} is an invalid value for "patience": it must be a positive integer '
                "or None (if you want to disable early stopping)"
            )

        super().__init__(cuda_device)

        # I am not calling move_to_gpu here, because if the model is
        # not already on the GPU then the optimizer is going to be wrong.
        if len(self._cuda_devices) > 1:
            raise NotImplementedError("Distributed training is not supported")
        torch_device = torch.device(f"cuda:{self._cuda_devices[0]}" if self._cuda_devices[0] >= 0 else "cpu")
        self.model: IModel = model.to(torch_device)
        self.optimizer = optimizer

        self.iterator = iterator
        self.validation_iterator = validation_iterator or iterator
        self.train_data = train_dataset
        self.validation_data = validation_dataset
        self.shuffle = shuffle

        self.lr_scheduler = lr_scheduler

        self.num_epochs = num_epochs
        self.accumulation_steps = accumulation_steps
        self.gradual_unfreezing_steps = gradual_unfreezing_steps or ()

        self.run_validation_each_global_steps = run_validation_each_global_steps

        self.grad_norm = grad_norm

        self.scaler = scaler

        self.metrics = metrics
        self.label_keys = label_keys
        self.validation_metric_names: List[str] = ["loss"] + list(
            chain.from_iterable(metric.NAMES for metric in metrics.values())
        )

        self.seed = seed

        self.early_stopping_configuration: EarlyStoppingI = EarlyStoppingNull()

        if self.validation_data is not None and early_stopping:
            if early_stopping_metric_name not in self.validation_metric_names:
                raise ConfigurationError("Your validation metric should be in model metrics list")
            if patience is None:
                raise ConfigurationError("You should set patience if you want to use early_stopping")
            self.early_stopping_configuration = EarlyStopping(
                patience=patience,
                metric_name=early_stopping_metric_name,
                should_decrease=early_stopping_metric_should_decrease,
            )

        if clearml_task is None:
            self.clearml_reporter: ClearMLReporterI = ClearMLReporterNull()
        else:
            self.clearml_reporter = ClearMLReporter(clearml_task)

        self.callbacks = Callbacks(
            early_stopping=self.early_stopping_configuration, clearml_reporter=self.clearml_reporter
        )

    def set_clearml_task(self, clearml_task: Task) -> None:
        self.clearml_reporter = ClearMLReporter(clearml_task)
        self.callbacks = Callbacks(
            early_stopping=self.early_stopping_configuration, clearml_reporter=self.clearml_reporter
        )

    def _train_mode(self) -> None:
        self.model.train()
        self.model.zero_grad()

    def _eval_mode(self) -> None:
        self.model.eval()

    def _gradual_unfreezing(self, step: int) -> None:
        if self.gradual_unfreezing_steps:
            for name, param in self.model.named_parameters():
                if any(
                    list(chain(*[[i in name for i in group] for group in self.gradual_unfreezing_steps[: step + 1]]))
                ):
                    param.requires_grad = True
                else:
                    param.detach_()
                    param.requires_grad = False

    def _calculate_metrics(
        self, outputs: torch.Tensor, batch_group: List[Tuple[Dict[str, Dict[str, torch.Tensor]], Sequence[int]]]
    ) -> None:
        batch, _ = batch_group[0]
        label_field_name, label_vector_name = self.label_keys
        if isinstance(label_vector_name, list):
            raise NotImplementedError("Measuring metric with more than one label vectors is not implemented")
        labels = batch[label_field_name][label_vector_name]

        for metric in self.metrics.values():
            metric(outputs, labels)

    def _form_metric_dict(self, total_loss: float, num_batches: int, reset: bool) -> Dict[str, float]:
        metrics_to_return = {"loss": total_loss / num_batches if num_batches > 0 else 0.0}
        for metric in self.metrics.values():
            for metric_name, metric_value in metric.get_metric(reset).items():
                if isinstance(metric_value, list):
                    for i, value in enumerate(metric_value):
                        metrics_to_return[f"{metric_name}_{i}"] = value
                else:
                    metrics_to_return[metric_name] = metric_value  # type: ignore
        return metrics_to_return

    def _configure_batch_iterator(
        self,
        iterator: DataIterator,
        data: Iterable[InstanceFeatureVectors],
        master_bar_logger: master_bar,
        shuffle: bool = True,
    ) -> Union[ConsoleProgressBar, NBProgressBar]:

        num_gpus = len(self._cuda_devices)
        raw_generator = iterator(data, shuffle=shuffle)
        generator = lazy_groups_of(raw_generator, num_gpus)  # type: ignore
        num_batches = math.ceil(iterator.get_num_batches(data) / num_gpus)

        return progress_bar(generator, total=num_batches, parent=master_bar_logger, leave=False)

    def _batch_outputs_and_loss(
        self, batch_group: List[Tuple[Dict[str, Dict[str, torch.Tensor]], Sequence[int]]]
    ) -> Sequence[torch.Tensor]:
        """
        Does a forward pass on the given batches and returns the ``loss`` value in the result.
        """
        if len(batch_group) != 1:
            raise NotImplementedError("Distributed training is not supported")
        batch, _ = batch_group[0]
        batch = nn_util.move_to_device(batch, self._cuda_devices[0])

        with autocast(enabled=self.scaler is not None):
            model_outputs, loss = self.model(**batch)

        if self.accumulation_steps > 1:
            loss = loss / self.accumulation_steps

        return model_outputs, loss

    def _backward(self, loss: torch.Tensor) -> None:
        if self.scaler is not None:
            # clip_grad_norm_ within self._step
            self.scaler.scale(loss).backward()
        else:
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.grad_norm)

    def _step(self) -> None:
        if self.scaler is not None:
            # clipping here because of: https://pytorch.org/docs/stable/notes/amp_examples.html#gradient-accumulation
            # note that we will clip accumulated gradients rather than clip them on each step
            self.scaler.unscale_(self.optimizer)
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.grad_norm)

            self.scaler.step(self.optimizer)
            self.scaler.update()
        else:
            self.optimizer.step()

        if self.lr_scheduler is not None:
            self.lr_scheduler.step()  # type: ignore

    def _train_epoch(
        self, master_bar_logger: master_bar, epoch: int, global_steps: int = 0
    ) -> Tuple[Dict[str, float], int]:
        """
        Trains one epoch and returns metrics.
        """
        train_loss = 0.0
        # Set the model to "train" mode.
        self._train_mode()

        batches_this_epoch = 0

        for batch_group in self._configure_batch_iterator(
            iterator=self.iterator, data=self.train_data, master_bar_logger=master_bar_logger
        ):

            batches_this_epoch += 1

            outputs, loss = self._batch_outputs_and_loss(batch_group)
            self._calculate_metrics(outputs=outputs, batch_group=batch_group)

            if torch.isnan(loss):
                raise ValueError("nan loss encountered")

            self._backward(loss)

            train_loss += loss.item()
            if batches_this_epoch % self.accumulation_steps == 0:
                self._step()
                self.model.zero_grad()

                self.callbacks.clearml_report_scalar(
                    title="Training", series="loss", value=loss.item(), iteration=global_steps
                )

                global_steps += 1

                master_bar_logger.child.comment = "loss: {:.4f}".format(train_loss / batches_this_epoch)

            if (
                self.run_validation_each_global_steps is not None
                and (global_steps + 1) % self.run_validation_each_global_steps == 0
            ):
                self._validation_run(master_bar_logger=master_bar_logger, global_steps=global_steps)
                self._train_mode()

        metrics = self._form_metric_dict(total_loss=train_loss, num_batches=batches_this_epoch, reset=True)
        return metrics, global_steps

    def _validation_run(self, master_bar_logger: master_bar, global_steps: int = 0) -> Optional[Dict[str, float]]:
        """
        Computes the validation metrics. Returns it and the number of batches.
        """
        if self.validation_data is None:
            return None

        logger.info("Validating")

        with torch.no_grad():
            self._eval_mode()

            batches_this_epoch = 0
            val_loss = 0
            for batch_group in self._configure_batch_iterator(
                iterator=self.validation_iterator,
                data=self.validation_data,
                master_bar_logger=master_bar_logger,
                shuffle=False,
            ):
                outputs, loss = self._batch_outputs_and_loss(batch_group)
                self._calculate_metrics(outputs=outputs, batch_group=batch_group)
                batches_this_epoch += 1
                val_loss += loss.cpu().numpy()

            val_metrics = self._form_metric_dict(total_loss=val_loss, num_batches=batches_this_epoch, reset=True)

        for metric_name, metric_value in val_metrics.items():
            self.callbacks.clearml_report_scalar(
                title="Validation", series=metric_name, value=metric_value, iteration=global_steps
            )
        return val_metrics

    def train(self) -> IModel:
        """
        Trains the supplied model with the supplied parameters.
        """
        global_steps = 0
        logger.info("Beginning training.")
        mb = master_bar(range(self.num_epochs))
        mb.first_bar.comment = f"{self.model.__class__.__name__} training"
        mb_elements = ["epoch"] + [f"train_{metrics_name}" for metrics_name in self.validation_metric_names]
        if self.validation_data is not None:
            mb_elements.extend([f"val_{metrics_name}" for metrics_name in self.validation_metric_names])

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
                best_model = deepcopy(self.model).cpu()  # TODO: This creates a copy on GPU and then moves to RAM
                #  Thus, GPU memory must hold two copies of a single model at once (before dumping to RAM)
                #  Can we copy directly to RAM?
                # https://discuss.pytorch.org/t/copy-best-model-from-gpu-to-cpu/38683

        return best_model
