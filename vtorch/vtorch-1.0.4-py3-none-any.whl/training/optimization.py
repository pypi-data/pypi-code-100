import abc
import os
from copy import deepcopy
from operator import itemgetter
from typing import Iterable, List, Optional, Union

import optuna
from clearml import Task
from optuna import Study, Trial
from optuna.visualization import plot_parallel_coordinate

from vtorch.common.checks import ConfigurationError
from vtorch.training import Trainer
from vtorch.training.logging_util import (
    get_language_tag,
    get_results_subfolder_hierarchy,
    log_training_hyperparameters,
)


class TrainerFactory(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_trainer(self, trial: Trial) -> Trainer:
        pass


class Objective(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __call__(self, trial: Trial) -> Union[float, List[float]]:
        pass


class ObjectiveProvider(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_task_objective(self, project_name: str, task_name: str, experiment_tags: Iterable[str]) -> Objective:
        pass


class ModelTrainingObjective(Objective):
    def __init__(
        self,
        project_name: str,
        task_name: str,
        experiment_tags: Iterable[str],
        trainer_factory: TrainerFactory,
        target_metric_name: str,
        target_series_name: str,
        additional_series_names: Optional[Iterable[str]] = None,
        use_best_epoch: bool = True,
        should_decrease: bool = False,
    ) -> None:
        self.experiment_tags = experiment_tags
        self.project_name = project_name
        self.task_name = task_name
        self.trainer_factory = trainer_factory
        self.target_metric_name = target_metric_name
        self.target_series_name = target_series_name
        self.additional_series_names = additional_series_names
        self.use_best_epoch = use_best_epoch
        self.should_decrease = should_decrease

    def __call__(self, trial: Trial) -> Union[float, List[float]]:
        trainer = deepcopy(self.trainer_factory.get_trainer(trial))

        clearml_task = Task.create(
            project_name=self.project_name,
            task_name=f"{self.task_name}_{trial.number}",
            add_task_init_call=True,
            task_type=Task.TaskTypes.training,
        )

        clearml_task.mark_started()
        clearml_task.set_resource_monitor_iteration_timeout(1e9)
        clearml_task.add_tags(sorted(self.experiment_tags))

        trainer.set_clearml_task(clearml_task=clearml_task)
        log_training_hyperparameters(trainer, clearml_task)
        trainer.train()
        clearml_task.completed()

        metric_series = clearml_task.get_reported_scalars()[self.target_metric_name]
        target_metric_series = metric_series[self.target_series_name]["y"]
        if self.use_best_epoch:
            op = min if self.should_decrease else max
            i, metric = op(enumerate(target_metric_series), key=itemgetter(1))
        else:
            i, metric = -1, target_metric_series[-1]

        if self.additional_series_names is None:
            return metric  # type: ignore
        return [metric] + [metric_series[name]["y"][i] for name in self.additional_series_names]  # type: ignore


class ModelTrainingObjectiveProvider(ObjectiveProvider):
    def __init__(
        self,
        trainer_factory: TrainerFactory,
        target_metric_name: str,
        target_series_name: str,
        additional_series_names: Optional[Iterable[str]] = None,
        use_best_epoch: bool = True,
        should_decrease: bool = False,
    ) -> None:
        self.trainer_factory = trainer_factory
        self.target_metric_name = target_metric_name
        self.target_series_name = target_series_name
        self.additional_series_names = additional_series_names
        self.use_best_epoch = use_best_epoch
        self.should_decrease = should_decrease

    def get_task_objective(
        self, project_name: str, task_name: str, experiment_tags: Iterable[str]
    ) -> ModelTrainingObjective:
        return ModelTrainingObjective(
            project_name=project_name,
            task_name=task_name,
            experiment_tags=experiment_tags,
            trainer_factory=self.trainer_factory,
            target_metric_name=self.target_metric_name,
            target_series_name=self.target_series_name,
            additional_series_names=self.additional_series_names,
            use_best_epoch=self.use_best_epoch,
            should_decrease=self.should_decrease,
        )


class OptunaHyperparametersPipe:
    def __init__(
        self,
        project_name: str,
        objective_provider: ObjectiveProvider,
        study: Optional[Study] = None,
        n_trials: Optional[int] = None,
        save_folder: str = "results",
        log_by_language: bool = True,
        language_subfolder_depth_id: Optional[int] = None,
    ) -> None:
        self.project_name = project_name
        self.objective_provider = objective_provider
        self.study = study or optuna.create_study()
        self.n_trials = n_trials
        self.save_folder = save_folder
        self.log_by_language = log_by_language
        self.language_subfolder_depth_id = language_subfolder_depth_id

    def run(self, experiment_name: str, experiment_name_suffix: str = "") -> None:

        config_py = experiment_name
        results_subfolder_hierarchy = f"{get_results_subfolder_hierarchy(config_py)}_{experiment_name_suffix}"

        save_folder = str(os.path.join(self.save_folder, results_subfolder_hierarchy))
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        experiment_tags = ["vtorch_3.0", "hyperparameters_optimization_run"]
        if self.log_by_language:
            if self.language_subfolder_depth_id is None:
                raise ConfigurationError(
                    "To use logging by language provide 'language_subfolder_depth_id'"
                    " argument during the initialization"
                )
            experiment_tags.append(get_language_tag(config_py, self.language_subfolder_depth_id))

        clearml_task = Task.init(
            project_name=self.project_name,
            task_name=results_subfolder_hierarchy.replace(os.path.sep, "_") + "_optimization",
            task_type=Task.TaskTypes.optimizer,
        )
        self._log_hyperparameters(clearml_task)
        clearml_task.upload_artifact(name="config", artifact_object=config_py)

        objective = self.objective_provider.get_task_objective(
            project_name=self.project_name,
            task_name=results_subfolder_hierarchy.replace(os.path.sep, "_"),
            experiment_tags=experiment_tags,
        )
        self.study.optimize(objective, n_trials=self.n_trials, gc_after_trial=True)
        self._log_results(clearml_task)

    def _log_results(self, clearml_task: Task) -> None:
        clearml_task.upload_artifact("study.trials_dataframe", artifact_object=self.study.trials_dataframe())

        logger = clearml_task.get_logger()
        for trial in self.study.best_trials:
            best_params = deepcopy(trial.params)
            for i, value in enumerate(trial.values):
                best_params[f"value_{i}"] = value

            clearml_task.connect(best_params, name=f"Best Trial #{trial.number}")

        for i in range(len(self.study.directions)):
            logger.report_plotly(
                "Parallel Coordinate",
                series=f"Direction {i}",
                iteration=0,
                figure=plot_parallel_coordinate(self.study, target=lambda _trial: _trial.values[i]),
            )

    def _log_hyperparameters(self, clearml_task: Task) -> None:
        clearml_task.connect(
            {
                "n_trials": self.n_trials,
                "sampler": self.study.sampler.__class__.__name__,
                "pruner": self.study.pruner.__class__.__name__,
            }
        )
