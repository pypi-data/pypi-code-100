# coding=utf-8

from mammut.curriculum.lesson import lesson_base
from mammut.common.corpus.corpus_map import CorpusMap
from mammut.curriculum.models import sentencepiece
from mammut.curriculum.core.mammut_session_context import MammutSessionContext


class SentencepieceBPELesson(lesson_base.Lesson):
    """Implements a Lesson to work with Sentencepiece
    BPE sub word model.
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

    def _get_model_instance(self) -> sentencepiece.SentencePieceBPEModel:
        return sentencepiece.SentencePieceBPEModel(
            self.parameters_dict, self.course, self.lesson_id
        )

    def lecture(self):
        """Loads all the prepare knowledge for the lesson.

        Note: for now only loads the corpus.
        """
        self.corpus = self.get_corpus(
            self.corpus_id, self._corpus_map_reference
        )

    def practice(
        self, mammut_session_context: MammutSessionContext,
    ):
        """Process training of sentencepiece model and save the model afterward.

        Training options information at:
        https://github.com/google/sentencepiece/blob/master/doc/options.md

        Args:
            save_path: file system folder path to save the model.
        """
        self._model.train(mammut_session_context, **{"corpus": self.corpus,})
        self._model.save(mammut_session_context)


class SentencepieceNGRAMLesson(lesson_base.Lesson):
    """Implements a Lesson to work with Sentencepiece
    NGRAM subword model
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
        """
        TODO: assessments should be completed and integrated.

        Args:
            lesson_id(str): 'id' string cell value in lesson sheet.
            course(str): 'course' string cell value in lesson sheet.
            order(str): 'order' string cell value in lesson sheet.
            corpus_id(str): 'corpus_id' string string cell value in lesson sheet.

            name(str): 'name' string cell value in lesson sheet.
            language_competence(str): 'language_competence' string cell value in lesson sheet.
            mammut_session_context: The session context from the classroom.
        """
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

    def _get_model_instance(self) -> sentencepiece.SentencePieceNGRAMModel:
        return sentencepiece.SentencePieceNGRAMModel(
            self.parameters_dict, self.course, self.lesson_id
        )

    def lecture(self):
        """Loads all the prepare knowledge for the lesson.

        Note: for now only loads the corpus.
        """
        self.corpus = self.get_corpus(
            self.corpus_id, self._corpus_map_reference
        )

    def practice(self, mammut_session_context: MammutSessionContext):
        """Process training of sentencepiece model and save the model afterward.

        Training options information at:
        https://github.com/google/sentencepiece/blob/master/doc/options.md

        Args:
            save_path: file system folder path to save the model.
        """
        self._model.train(mammut_session_context, **{"corpus": self.corpus,})
        self._model.save(mammut_session_context)
