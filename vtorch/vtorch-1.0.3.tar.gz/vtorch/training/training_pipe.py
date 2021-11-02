import os
from typing import Optional

from clearml import Task

from vtorch.common.checks import ConfigurationError
from vtorch.common.persistance import Persistent
from vtorch.training import Trainer
from vtorch.training.logging_util import (
    get_language_tag,
    get_results_subfolder_hierarchy,
    log_training_hyperparameters,
)


class TrainingPipeline:
    def __init__(
        self,
        project_name: str,
        trainer: Trainer,
        vectorizer: Persistent,  # TODO: to Vectorizer in the future, for the MultipleVectorizerContainer usage for now
        save_folder: str = "results",
        log_by_language: bool = True,
        language_subfolder_depth_id: Optional[int] = None,
    ) -> None:
        self.project_name = project_name
        self.trainer = trainer
        self.vectorizer = vectorizer
        self.save_folder = save_folder
        self.log_by_language = log_by_language
        self.language_subfolder_depth_id = language_subfolder_depth_id

    def run(self, experiment_name: str, experiment_name_suffix: str = "") -> None:

        config_py = experiment_name
        results_subfolder_hierarchy = f"{get_results_subfolder_hierarchy(config_py)}_{experiment_name_suffix}"

        save_folder = str(os.path.join(self.save_folder, results_subfolder_hierarchy))
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        experiment_tags = ["vtorch_3.0"]
        if self.log_by_language:
            if self.language_subfolder_depth_id is None:
                raise ConfigurationError(
                    "To use logging by language provide 'language_subfolder_depth_id'"
                    " argument during the initialization"
                )
            experiment_tags.append(get_language_tag(config_py, self.language_subfolder_depth_id))

        clearml_task = Task.init(
            project_name=self.project_name,
            task_name=results_subfolder_hierarchy.replace(os.path.sep, "_"),
            auto_resource_monitoring=True,
            auto_connect_arg_parser=True,
            auto_connect_frameworks={"pytorch": True},
        )
        clearml_task.set_resource_monitor_iteration_timeout(1e9)
        clearml_task.add_tags(experiment_tags)
        log_training_hyperparameters(self.trainer, clearml_task)
        clearml_task.upload_artifact(name="config", artifact_object=config_py)
        self.trainer.set_clearml_task(clearml_task=clearml_task)

        model = self.trainer.train()
        for obj, subfolder in (model, "model"), (self.vectorizer, "vectorizer"):
            obj_save_folder = os.path.join(save_folder, subfolder)
            if not os.path.exists(obj_save_folder):
                os.mkdir(obj_save_folder)
            obj.save(obj_save_folder)
