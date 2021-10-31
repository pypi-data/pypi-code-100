from mammut.curriculum.lesson import lesson_base
from mammut.curriculum.models.online_models.ktt_interpretation_model import (
    KttInterpretationModel,
)
from mammut.curriculum.models.online_models.online_models import (
    OnlineModelsRegistry,
)
from mammut.curriculum.models.model_base import ModelBase
from mammut.common.corpus.corpus_map import CorpusMap
from mammut.curriculum.core.mammut_session_context import MammutSessionContext
import ray
import logging
import mammut.curriculum.report as report

logger = logging.getLogger(__name__)


class KttInterpretationLesson(lesson_base.Lesson):
    """This KttInterpretationLesson is designed to compose a course to
    compile package corpus in the Mammut Working Memory.

    Internally handles a KttInterpretationModel actor reference.

    This lesson is designed to be the first lesson of the course 0 in academic
    period 0.
    """

    RESERVED_COURSE_ID = 0
    RESERVED_LESSON_ID = 1
    RESERVED_ACADEMIC_PERIOD = 0

    def __init__(
        self,
        lesson_id: str,
        course: str,
        order: str,
        corpus_id: str,
        name: str,
        language_competence: str,
        parameters: str,
        mammut_session_context: MammutSessionContext,
    ):
        """
        Args:
            lesson_id(str): 'id' value in datasource retrieved data.
            course(str): 'course' value in datasource retrieved data.
            order(str): 'order' value in datasource retrieved data.
            corpus_id(str): 'corpus_id' value in datasource retrieved data.
            name(str): 'name' value in datasource retrieved data.
            language_competence(str): 'language_competence' value in datasource retrieved data.
            mammut_session_context: The session context from the classroom.
        """
        super(KttInterpretationLesson, self).__init__(
            lesson_id,
            course,
            order,
            corpus_id,
            None,
            name,
            language_competence,
            parameters,
            mammut_session_context,
        )

    def _get_model_instance(self) -> ModelBase:
        online_models_registry = (
            self._mammut_session_context.online_models_registry
        )
        return OnlineModelsRegistry.get_model_instance(
            KttInterpretationModel.MODEL_NAME, online_models_registry, self
        )

    def lecture(self):
        """Nothing to lecture in this lesson.
        """
        pass

    def practice(self, mammut_session_context: MammutSessionContext):
        """Practice the interpretation of the package corpus.

        This implies the interpretation of the selected corpus.

        The model takes care of creating a new java process where
        the transducer interpretation is executed.

        The model will save be saved in the OnlineModelsRegistry.
        From there, it can be used across processes to perform operations
        in the Working Memory.

        Args:
            mammut_session_context: The session context from the classroom.
        """
        self._model.train.remote(mammut_session_context)
