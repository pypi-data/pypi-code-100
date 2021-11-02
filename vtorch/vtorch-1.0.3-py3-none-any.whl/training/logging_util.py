import math
import os
from typing import Optional

from clearml import Task
from transformers import PretrainedConfig

from vtorch.training import Trainer
from vtorch.training.callbacks import EarlyStopping


def get_language_tag(config_py: str, language_subfolder_depth_id: int) -> str:
    experiment_config_path = config_py.split(os.path.sep)
    return "lang_" + experiment_config_path[language_subfolder_depth_id]


def get_results_subfolder_hierarchy(config_py: str) -> str:
    no_py_extension = 0
    no_config_root_folder = slice(1, None)
    results_subfolder_hierarchy = os.path.splitext(
        os.path.sep.join(config_py.split(os.path.sep)[no_config_root_folder])
    )[no_py_extension]
    return results_subfolder_hierarchy


def log_model_hyperparameters(trainer: Trainer, clearml_task: Task) -> None:
    serializable_params = {}
    if hasattr(trainer.model, "config") and isinstance(trainer.model.config, PretrainedConfig):
        serializable_params = trainer.model.config.to_dict()
    clearml_task.connect({"model_class": trainer.model.__class__.__name__, **serializable_params})


def log_optimization_hyperparameters(trainer: Trainer, clearml_task: Task) -> None:
    defaults = {
        f"optimizer_initial_param_{name}": value for name, value in getattr(trainer.optimizer, "defaults", {}).items()
    }
    clearml_task.connect(
        {
            "optimizer": trainer.optimizer.__class__.__name__,
            "scheduler": None if trainer.lr_scheduler is None else trainer.lr_scheduler.__class__.__name__,
            "grad_norm": getattr(trainer, "grad_norm", None),
            **defaults,
        }
    )


def log_dataset_hyperparameters(trainer: Trainer, clearml_task: Task) -> None:
    get_num_train_instances = getattr(trainer.train_data, "__len__", None)
    get_num_validation_instances = getattr(trainer.validation_data, "__len__", None)

    if get_num_train_instances is not None:
        num_train_instances = get_num_train_instances()
        train_batch_size: Optional[int] = math.ceil(
            num_train_instances / trainer.iterator.get_num_batches(trainer.train_data)
        )
    else:
        num_train_instances = None
        train_batch_size = None

    num_validation_instances = None if get_num_validation_instances is None else get_num_validation_instances()

    clearml_task.connect(
        {
            "train_iterator_class": trainer.iterator.__class__.__name__,
            "train_batch_size": train_batch_size,
            "validation_iterator_class": trainer.validation_iterator.__class__.__name__,
            "num_train_instances": num_train_instances,
            "num_validation_instances": num_validation_instances,
            "shuffle": getattr(trainer, "shuffle", None),
        }
    )


def log_trainer_hyperparameters(trainer: Trainer, clearml_task: Task) -> None:
    if isinstance(trainer.early_stopping_configuration, EarlyStopping):
        clearml_task.connect(trainer.early_stopping_configuration)

    clearml_task.connect(
        {
            "num_epochs": getattr(trainer, "num_epochs", None),
            "accumulation_steps": getattr(trainer, "accumulation_steps", None),
            "gradual_unfreezing_steps": getattr(trainer, "gradual_unfreezing_steps", None),
        }
    )


def log_training_hyperparameters(trainer: Trainer, clearml_task: Task) -> None:
    log_model_hyperparameters(trainer, clearml_task)
    log_optimization_hyperparameters(trainer, clearml_task)
    log_dataset_hyperparameters(trainer, clearml_task)
    log_trainer_hyperparameters(trainer, clearml_task)
