import ray
from typing import Dict
import logging
import mammut.curriculum.report as report
from mammut.curriculum.models.online_models.ktt_interpretation_model import (
    KttInterpretationModel,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@ray.remote
class OnlineModelsRegistry:
    """A online models registry designed to be available across the curriculum
    as a Ray actor.

    This registry is a table where keys are tuples of course ID and lesson ID,
    and values are online models actor handles.

    Each online model must be a Ray actor class. Make sure to use @ray.remote.
    Currently, that can't be generalized in a class because ray doesn't support
    inheriting from actor classes. Thus, each online model must use the
    @ray.remote decorator.
    """

    # Table of available online models to instantiate by name.
    _available_models: Dict = {
        KttInterpretationModel.MODEL_NAME: KttInterpretationModel
    }

    def __init__(self):
        self._table: Dict[str, ray.actor.ActorHandle] = {}

    def add_model_entry(
        self, model_name: str, model_handle: ray.actor.ActorHandle,
    ):
        """Adds a new online model to the registry if it doesn't
        exists in the registry.

        Models are stored in a Key value table where the key is
        the model name, and the value is the ActorHandle of the model.

        Keeping the ActorHandle in the table is a safe way to ensure
        the lifecycle of the actor.

        Currently ActorHandles can't be returned by remote functions in Ray
        (https://github.com/ray-project/ray/issues/1222). Because of that,
        named actors are used for online models. Doing so, they can be accessed
        across the Ray cluster using their name.

        Args:
            model_name: name of the model.
            model_handle: Ray actor handle for the model.
        """
        logger.info(
            f"Adding model handle in OnlineModelsRegistry: ({model_name})"
        )
        if model_name not in self._table:
            self._table[model_name] = model_handle

    def has_model(self, model_name: str) -> bool:
        return model_name in self._table

    @staticmethod
    def get_model_instance(model_name, registry_handle, lesson):
        """Returns an online model stored in this registry. If the models doesn't exists,
        it will be created.

        This method is designed this way to centralize the request of a model
        in this registry code. The method needs the name of the online model because
        of (https://github.com/ray-project/ray/issues/1222).

        Args:
            model_name: The model of the online name to retrieve the named actor handle.
            registry_handle: An actor handle for an instance of this registry.
            lesson: The lessson for which the model will be created.

        Raises:
            KeyError if the named online model isn't in the registry.

        Returns:
            Returns the ActorHandle for the requested model.
        """
        registry_has_model = ray.get(
            registry_handle.has_model.remote(model_name)
        )

        if registry_has_model:
            report.send_message(
                report.CurriculumGeneralDebugMessage(
                    "KttInterpretationLesson model found in registry. Reusing model."
                )
            )
            return ray.get_actor(model_name)

        else:
            report.send_message(
                report.CurriculumGeneralDebugMessage(
                    "KttInterpretationLesson model not found in registry. Creating model."
                )
            )
            model_handle = (
                OnlineModelsRegistry._available_models[model_name]
                .options(name=model_name)
                .remote(
                    lesson.parameters_dict, lesson.course, lesson.lesson_id
                )
            )
            registry_handle.add_model_entry.remote(
                KttInterpretationModel.MODEL_NAME, model_handle
            )
            return model_handle
