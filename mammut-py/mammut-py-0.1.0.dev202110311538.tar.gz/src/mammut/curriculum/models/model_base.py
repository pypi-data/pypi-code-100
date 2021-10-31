import enum
import logging
from abc import ABC, abstractmethod
from typing import Dict
from mammut.curriculum.core.mammut_session_context import MammutSessionContext

log = logging.getLogger(__name__)


class ModelBase(ABC):
    """ Base API for Curriculum models.

    This class exposes a basic API that allows to use
    different models for Curriculum client code.

    """

    def __init__(self, parameters: Dict, course_id: int, lesson_id: int):
        """
        Args:
            parameters: Dictionary with lessons parameters to forward to this model.
            course_id (int): the course ID to which this model belongs.
            lesson_id (int): the lesson ID to which this model belongs.
        """
        self.parameters: Dict = parameters
        self.course_id: int = course_id
        self.lesson_id: int = lesson_id

    @abstractmethod
    def train(self, mammut_session_context: MammutSessionContext, **kwargs):
        """Train the model this class implements.

        Args:
            **kwargs: Named parameters required for the implementation
                in the child class.
        """
        pass

    @abstractmethod
    def save(self, mammut_session_context: MammutSessionContext, **kwargs):
        """Persist the model in memory.

        Args:
            mammut_session_context: Mammut session context with general information about
                current curriculum instance.
            **kwargs: Any other custom attribute.
        """
        pass

    def _get_model_file_system_path(self, file_system_prefix_path: str) -> str:
        """Return the file system path for saving this model.

        The prefix path is the same for all curriculum models, with
        specific directories for each course/lesson. This method concatenates
        those specific directories.

        An example of a full file system path for a curriculum model is:
            /home/user/.mammut-py/curriculum/14/3

            The prefix path is: /home/user/.mammut-py/curriculum/
            The last folders: /14/3 refers to the course 14 and lesson 3

        Args:
            file_system_prefix_path: prefix of the path.
        """
        save_folder = (
            file_system_prefix_path + f"/{self.course_id}/{self.lesson_id}"
        )
        return save_folder

    @classmethod
    def get_model_file_system_path(
        cls, file_system_prefix_path: str, course_id: str, lesson_id: str
    ) -> str:
        """Returns the file system path for a trained model, given a course ID
        and a lesson ID.

        Args:
            file_system_prefix_path: prefix of the path.
            course_id: some course ID
            lesson_id: some lesson ID.
        """
        save_folder = file_system_prefix_path + f"/{course_id}/{lesson_id}"
        return save_folder
