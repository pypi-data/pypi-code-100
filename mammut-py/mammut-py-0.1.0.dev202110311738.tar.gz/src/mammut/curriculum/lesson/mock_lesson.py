# coding=utf-8

from mammut.curriculum.lesson import lesson_base
from mammut.common.corpus.corpus_map import CorpusMap
from mammut.curriculum.models import mock
from mammut.curriculum.core.mammut_session_context import MammutSessionContext


class MockLesson(lesson_base.Lesson):
    """Implements a Lesson mock for unit testing of Curriculum.
    """

    def __init__(
        self,
        lesson_id: str,
        course: str,
        order: str,
        corpus_id: str,
        corpus_map: CorpusMap,
        name: str,
        language_competence: str,
        parameters: str,
        mammut_session_context: MammutSessionContext,
    ):
        lesson_base.Lesson.__init__(
            self,
            lesson_id,
            course,
            order,
            corpus_id,
            corpus_map,
            name,
            language_competence,
            parameters,
            mammut_session_context,
        )
        self._model = self._get_model_instance()

    def lecture(self):
        pass

    def practice(self, mammut_session_context: MammutSessionContext):
        """
        Args:
            save_path: file system folder path to save the model after trained.
        """
        self._model.train(mammut_session_context)
        self._model.save(mammut_session_context)

    def _get_model_instance(self):
        return mock.TestMockModel(self.course, self.lesson_id)
