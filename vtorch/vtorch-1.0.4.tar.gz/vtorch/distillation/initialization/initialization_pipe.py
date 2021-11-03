import os
from typing import Optional

import transformers
from clearml import Task

from vtorch.common.checks import ConfigurationError
from vtorch.models.model import IModel
from vtorch.training.logging_util import get_language_tag, get_results_subfolder_hierarchy


class InitializationDistillModelPipeline:
    def __init__(
        self,
        project_name: str,
        teacher_model: IModel,
        reduction: int,
        save_folder: str = "results",
        teacher_base_model_attr: str = "_base_model",
        log_by_language: bool = True,
        language_subfolder_depth_id: Optional[int] = None,
    ):
        """
        Parameters
        ----------
        teacher_model: IModel, teacher model
        reduction: the factor of reduction the children model's size
            (e.g with reduction=2 6-layer student would be initialized from the 12-layer teacher)
        save_folder: str (default = "results") folder to store student
        teacher_base_model_attr: str (default = "_base_model") attribute of base model (e.g Transformer) whose
            parameters will be used for initialization
        """
        self.project_name = project_name
        self.teacher_model = teacher_model
        self.reduction = reduction
        self.save_folder = save_folder
        self.teacher_base_model_attr = teacher_base_model_attr
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
            auto_connect_arg_parser=True,
            auto_connect_frameworks={"pytorch": True},
            task_type=Task.TaskTypes.custom,
        )

        clearml_task.set_resource_monitor_iteration_timeout(1e9)
        clearml_task.add_tags(experiment_tags)
        self._log_hyperparameters(clearml_task)
        clearml_task.upload_artifact(name="config", artifact_object=config_py)

        self._initialize()
        self.teacher_model.save(save_folder)

    def _initialize(self) -> None:
        teacher_base_model = getattr(self.teacher_model, self.teacher_base_model_attr)
        teacher_base_model.config.num_hidden_layers = teacher_base_model.config.num_hidden_layers // self.reduction

        student_base_model = getattr(transformers, teacher_base_model.__class__.__name__)(teacher_base_model.config)

        student_base_model_state_dict = student_base_model.state_dict()
        teacher_base_model_state_dict = teacher_base_model.state_dict()

        for student_key in student_base_model_state_dict.keys():
            # e.g "encoder.layer.4.attention.self.query.weight" -> "encoder.layer.9.attention.self.query.weight"
            teacher_key = ".".join(
                str((int(substring) * 2) + 1) if substring.isdigit() else substring
                for substring in student_key.split(".")
            )
            student_base_model_state_dict[student_key] = teacher_base_model_state_dict[teacher_key]

        student_base_model.load_state_dict(student_base_model_state_dict)

        setattr(self.teacher_model, self.teacher_base_model_attr, student_base_model)

    def _log_hyperparameters(self, clearml_task: Task) -> None:
        clearml_task.connect({"reduction": self.reduction})
