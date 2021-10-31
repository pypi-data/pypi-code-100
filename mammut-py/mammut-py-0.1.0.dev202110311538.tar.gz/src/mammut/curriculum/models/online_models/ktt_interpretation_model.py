from abc import ABC, abstractmethod
from typing import Optional, Dict, List
import ray
from random import randint

from mammut.curriculum.core.mammut_session_context import MammutSessionContext
from mammut.curriculum.models.model_base import ModelBase


class VerbBuilder(ABC):
    """Abstract VerbBuilder which generalizes the operations of a concrete VerbBuilder
    implementation for Verb instances created in KtT at compile time.
    """

    @abstractmethod
    def get_builder_name(self) -> str:
        """Returns the name of the concrete builder.

        Useful for testing the builder value in real KtT process running in the
        Curriculum processing.
        """
        pass

    @abstractmethod
    def create_verb(
        self,
        title: str,
        micro_experience_type: str,
        parameter_1: str,
        parameter_2: Optional[str],
    ) -> Optional[int]:
        """Creates a Verb and save it as defined by the concrete implementation.

        Returns:
            ID of the created Verb. None if creation of the verb failed.
        """
        pass


@ray.remote
class VerbBuilderMock(VerbBuilder):
    """This VerbBuilderMock is a dummy representation of a VerbBuilder.

    This VerbBuilderMock is useful for testing the functionality with a real KtT
    process running in the Curriculum processing.
    """

    def get_builder_name(self) -> str:
        return "VerbBuilderMock"

    def create_verb(
        self,
        title: str,
        micro_experience_type: str,
        parameter_1: str,
        parameter_2: Optional[str],
    ) -> Optional[int]:
        """Mocks the creations of a Verb and returns it's ID.

        This is useful for testing the return value in the KtT process.

        Returns:
            The ID supposedly created for the Verb.
        """
        return randint(0, 5000)


class UIEventBuilder(ABC):
    """Abstract UIEventBuilder which generalizes the operations of a UIEvent builder implementation
    for UI Events verb instances created in KtT at compile time"""

    @abstractmethod
    def get_builder_name(self) -> str:
        """Returns the name of the concrete builder.

        Useful for testing the builder value in real KtT process running in the
        Curriculum processing.
        """
        pass

    @abstractmethod
    def create_ui_event(
        self,
        uri: str,
        control: str,
        kind: str,
        arguments: Optional[List[str]],
        text: str,
    ) -> Optional[int]:
        """Creates a UIEvent and saves it as defined by the concrete implementation.

        Returns:
             ID of the created UI Event. None if the creation of UI Event failed.
        """
        pass


@ray.remote
class UIEventBuilderMock(UIEventBuilder):
    """This UIEventBuilderMock is a dummy implementation of a UIEvent Builder.

    This is iseful for testing the functionality with a real KtT process running
    in the Curriculum processing.
    """

    def get_builder_name(self) -> str:
        return "UIEVentBuilderMock"

    def create_ui_event(
        self,
        uri: str,
        control: str,
        kind: str,
        arguments: Optional[List[str]],
        text: str,
    ) -> Optional[int]:
        """Mocks the creation of a UI Event and returns it's ID.

        Returns:
            The ID supposedly created for the UI Event.
        """
        return randint(0, 5000)


@ray.remote
class KttInterpretationModel(ModelBase):
    """This KttInterpretationModel is designed to perform the package
    compilation-interpretation process.

    Internally is composed of a ray actor handle for the KtT ray java actor.
    """

    MODEL_NAME = "KttInterpretationModel"

    def __init__(
        self, parameters: Dict, course_id: int, lesson_id: int,
    ):
        # Don't use `super` syntax. It wil cause an error with Ray.
        # https://github.com/ray-project/ray/issues/449#issuecomment-727266380
        ModelBase.__init__(self, parameters, course_id, lesson_id)
        # TODO: This string should be on the configuration files.
        self._ktt_actor_class = ray.java_actor_class(
            "com.mammut.interpreter.raycurriculum.InterpreterMainRayCurriculumService"
        )
        self._ktt_actor_handle: ray.actor.ActorHandle = None
        self._verb_builder: ray.actor.ActorHandle = None
        self._ui_event_builder: ray.actor.ActorHandle = None

    def train(self, mammut_session_context: MammutSessionContext, **kwargs):
        """Train the model this class implements.

        Override this method in child classes. It's defined to `pass`
        here to avoid errors with Ray actor definition.

        Args:
            mammut_session_context: Mammut session context with general information about
                current curriculum instance.
            **kwargs: Named parameters required for the implementation
                in the child class.
        """

        # Creates Verb and UIEvent builders mock. Later the decision of which concrete class to instantiate
        # could be set as a configuration parameter.
        self._verb_builder = VerbBuilderMock.remote()
        self._ui_event_builder = UIEventBuilderMock.remote()

        self._ktt_actor_handle = self._ktt_actor_class.remote(
            "KtT package interpretation",
            mammut_session_context.main_report_actor_handle,
            self._verb_builder,
            self._ui_event_builder,
        )
        # Todo: Mammut-ID needs to be defined. It'll be when KtT mammut-api operations
        #   get decoupled. (https://github.com/mammut-io/mammut-py/issues/150)
        self._ktt_actor_handle.startPackageCompilation.remote(
            mammut_session_context.package_id,
            8264,
            "KtT package interpretation",
        )

    def save(self, mammut_session_context: MammutSessionContext, **kwargs):
        """The model itself has nothing to save.

        The lesson that holds this model are responsible for registering it
        in the OnlineModelsRegistry.

        Args:
            mammut_session_context: Mammut session context with general information about
                current curriculum instance.
            **kwargs: Any other custom attribute.
        """
        pass
