# coding=utf-8
import logging
import mammut.curriculum.core.utils as curriculum_utils
from mammut.common.corpus.corpus_map import CorpusMap
from abc import ABC, abstractmethod
from typing import List
import enum
from typing import Optional, Dict
import json
from mammut.curriculum.models.model_base import ModelBase
from mammut.curriculum.report.errors.json_parsing_errors import (
    JSONLessonParsingError,
)
from mammut.curriculum.report.utils import Phase
from mammut.curriculum.core.mammut_session_context import MammutSessionContext

log = logging.getLogger(__name__)


class CorpusType(enum.Enum):
    """Enumeration type for corpus supported in Lessons.

    Currently supported:
        - synthetic
        - raw
    """

    Synthetic = 1
    Raw = 2

    @staticmethod
    def from_str(label):
        if label == "synthetic":
            return CorpusType.Synthetic
        elif label == "raw":
            return CorpusType.Raw
        else:
            raise NotImplementedError


class Lesson(ABC):
    """Lesson class models a unit of model training
    and evaluation.

    A Lessons encapsulates:
    - A model to train
    - Parameters for the model
    - Input data

    A lesson should be subclassed based on the model to be used.
    Each lesson is associated with a course.
    """

    ID_COLUMN = "id"
    COURSE_COLUMN = "course"
    ORDER_COLUMN = "order"
    CORPUS_ID_COLUMN = "corpus_id"
    MODEL_COLUMN = "model"
    NAME_COLUMN = "name"
    LANGUAGE_COMPETENCE_COLUMN = "language_competence"
    PARAMETERS_COLUMN = "parameters"

    DEFAULT_START_CELL = "A1"
    DEFAULT_START_COLUMN = "A"
    DEFAULT_START_ROW = "1"
    DEFAULT_END_CELL = "H"

    def __init__(
        self,
        lesson_id: str,
        course: str,
        order: str,
        corpus_id: str,
        corpus_map: Optional[CorpusMap],
        name: str,
        language_competence: str,
        parameters: str,
        mammut_session_context: MammutSessionContext,
    ):
        """
        Note: Arguments are received as strings from storage manager retrieved
        dataset.

        Args:
            lesson_id(str): 'id' value in datasource retrieved data.
            course(str): 'course' value in datasource retrieved data.
            order(str): 'order' value in datasource retrieved data.
            corpus_id(str): 'corpus_id' value in datasource retrieved data.
            corpus_map: reference to the Package corpus map object.
            name(str): 'name' value in datasource retrieved data.
            language_competence(str): 'language_competence' value in datasource retrieved data.
            parameters(str): json string parameters for the model.
        """
        self.lesson_id: int = int(lesson_id)
        self.course: int = int(course)
        self.order: int = int(order)
        self.corpus_id: int = int(corpus_id)
        """
            Currently, only supported plain corpus as input data. 
            (A list of string tokens). More elaborated corpus elements 
            might be necessary in the future. 
        """
        self.name = name
        self.language_competence: curriculum_utils.LanguageCompetence = curriculum_utils.LanguageCompetence.from_str(
            language_competence
        )
        try:
            self.parameters_dict: Dict = json.loads(
                parameters.replace("\n", "")
            )
        except json.JSONDecodeError as e:
            raise JSONLessonParsingError(
                e,
                Phase.LOAD_CURRICULUM_LESSONS_DATA,
                course,
                lesson_id,
                self.PARAMETERS_COLUMN,
            )
        self._mammut_session_context: MammutSessionContext = mammut_session_context
        self._corpus_map_reference: CorpusMap = corpus_map
        self._model: ModelBase = self._get_model_instance()
        self.corpus = Optional[None]

    @abstractmethod
    def _get_model_instance(self) -> ModelBase:
        """Factory method for concrete instantiation of model at
        initialization time
        :param **kwargs: """
        pass

    @abstractmethod
    def lecture(self):
        """Loads all the knowledge resources required to train the model.

        This includes (but is not limited to) for example:
        - Load the training data for the model
        - Load pre-trained models if required
        - Pre-train a part of the model
        """
        pass

    @abstractmethod
    def practice(self, mammut_session_context: MammutSessionContext):
        """Process the training of the model and save the model after
        training.

        Note: each Lesson subclass can implement specific code to
        this method according to the specific language model object
        it's using.

        Args:
            save_path: file system folder path to save the model.
        """
        pass

    @property
    def model(self) -> ModelBase:
        """Model used by the lesson.

        Models are integrated through the curriculum.models.base.ModelBase
        interface.

        Returns:
            The object instance of the model,
                self._model.
        """
        return self._model

    @staticmethod
    def get_corpus(corpus_id: int, corpus_map: CorpusMap,) -> List[str]:
        """Returns a training corpus from the corpus map.

        Args:
            corpus_id(int): corpus id in corpus map sheet
                in package.
            corpus_map: CorpusMap object from within the
                Package used.

        Returns:
            The corpus instance.
        """
        corpus = next(
            filter(
                lambda c: c.id == str(corpus_id), corpus_map.get_all_corpus()
            ),
            None,
        )
        if corpus is None:
            log.info(f"Training Corpus not found. Corpus ID: {corpus_id}")
            raise RuntimeError(
                f"Training Corpus not found. Corpus ID: {corpus_id}"
            )
        return corpus.get_events_as_strings()
