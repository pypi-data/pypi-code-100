from mammut.curriculum.lesson import lesson_base
from mammut.curriculum.models.hugging_face.bert import *
from mammut.curriculum.models.hugging_face.roberta import (
    HuggingFaceRobertaTokenClassificationModel,
    HuggingFaceRobertaSequenceClassificationModel,
    HuggingFaceRobertaQuestionAnsweringModel,
)
from typing import Optional
from mammut.common.corpus.corpus_map import CorpusMap
from mammut.curriculum.core.mammut_session_context import MammutSessionContext


class HuggingFaceBertBaseLesson(lesson_base.Lesson):
    """Implements a concrete Lesson to work with bare Bert
    HuggingFace model curriculum wrapper.
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
        super(HuggingFaceBertBaseLesson, self).__init__(
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

    def _get_model_instance(self) -> HuggingFaceBertBaseModel:
        return HuggingFaceBertBaseModel(
            self.parameters_dict,
            self.course,
            self.lesson_id,
            self._mammut_session_context,
            self.corpus_id,
            self._corpus_map_reference,
        )

    def lecture(self):
        """Loads and prepare the model and tokenizer for this lesson.

        Currently, this data is prepared:
            - Download the pretrained model in memory.
        """
        self._model.load_pretrained_models()

    def practice(self, mammut_session_context: MammutSessionContext):
        """Practice the lessons by training the model with prepared data.

        Todo: There is nothing to train right now. Collaboration between
            corpus (or another data sources) and the model must be defined.

        Args:
            mammut_session_context: The session context from the classroom.
        """
        self._model.save(mammut_session_context)


class HuggingFaceBertTokenClassificationLesson(lesson_base.Lesson):
    """Implements a concrete Lesson to work with the HuggingFaceBertTokenClassificationModel.
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
        super(HuggingFaceBertTokenClassificationLesson, self).__init__(
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

    def _get_model_instance(self) -> HuggingFaceBertTokenClassificationModel:
        return HuggingFaceBertTokenClassificationModel(
            self.parameters_dict,
            self.course,
            self.lesson_id,
            self._mammut_session_context,
            self.corpus_id,
            self._corpus_map_reference,
        )

    def lecture(self):
        """Loads and prepare the model and tokenizer for this lesson.

        Currently, this data is prepared:
            - Download the pretrained model in memory.
        """
        self._model.load_pretrained_models()

    def practice(self, mammut_session_context: MammutSessionContext):
        """Practice the lessons by training the model with prepared data.

        Todo: There is nothing to train right now. Collaboration between
            corpus (or another data sources) and the model must be defined.

        Args:
            mammut_session_context: The session context from the classroom.
        """
        self._model.save(mammut_session_context)


class HuggingFaceRobertaTokenClassificationLesson(lesson_base.Lesson):
    """Implements a concrete Lesson to work with bare Roberta
    HuggingFace model curriculum wrapper.
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
        super(HuggingFaceRobertaTokenClassificationLesson, self).__init__(
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
        self.dataset = self.get_corpus(self.corpus_id, self._corpus_map_reference)
        self.preprocessed_data = None

    def get_corpus(
        self, corpus_id: int, corpus_map: CorpusMap,
    ):
        """Returns a training corpus from the corpus map.

        Args:
        corpus_id(int): corpus id in corpus map sheet
            in package.
        corpus_map: CorpusMap object from within the
            Package used.

        Returns:
        The corpus instance.
        """

        corpus = corpus_map.get_corpus_by_id(corpus_id)
        dataset = corpus.get_hf_dataset()
        return dataset

    def _get_model_instance(
        self,
    ) -> HuggingFaceRobertaTokenClassificationModel:
        return HuggingFaceRobertaTokenClassificationModel(
            self.parameters_dict,
            self.course,
            self.lesson_id,
            self._mammut_session_context,
            self.corpus_id,
            self._corpus_map_reference,
        )

    def lecture(self):
        """Loads and prepare the model and tokenizer for this lesson.

        Currently, this data is prepared:
            - Download the pretrained model in memory.
        """
        self.preprocessed_data = self.model.tokenize_corpus(self.dataset)
        self.model.load_pretrained_models()

    def practice(self, mammut_session_context: MammutSessionContext):
        """Practice the lessons by training the model with prepared data.

        Args:
        mammut_session_context:  The session context from the classroom.
        """
        self.model.train(mammut_session_context, **{"corpus": self.preprocessed_data})
        self.model.save(mammut_session_context)


class HuggingFaceRobertaSequenceClassificationLesson(lesson_base.Lesson):
    """Implements a concrete Lesson to work with bare Roberta
    HuggingFace model curriculum wrapper.
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
        super(HuggingFaceRobertaSequenceClassificationLesson, self).__init__(
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
        self.dataset = self.get_corpus(self.corpus_id, self._corpus_map_reference)
        self.preprocessed_data = None

    def get_corpus(
            self, corpus_id: int, corpus_map: CorpusMap,
    ):
        """Returns a training corpus from the corpus map.

        Args:
        corpus_id(int): corpus id in corpus map sheet
            in package.
        corpus_map: CorpusMap object from within the
            Package used.

        Returns:
        The corpus instance.
        """

        corpus = corpus_map.get_corpus_by_id(corpus_id)
        dataset = corpus.get_hf_dataset()
        return dataset

    def _get_model_instance(
        self,
    ) -> HuggingFaceRobertaSequenceClassificationModel:
        return HuggingFaceRobertaSequenceClassificationModel(
            self.parameters_dict,
            self.course,
            self.lesson_id,
            self._mammut_session_context,
            self.corpus_id,
            self._corpus_map_reference,
        )

    def lecture(self):
        """Loads and prepare the model, tokenizer and data for this lesson.

        Currently, this data is prepared:
            - Download the pretrained model in memory.
        """
        self.preprocessed_data = self.model.tokenize_corpus(self.dataset)
        self.model.load_pretrained_models()

    def practice(self, mammut_session_context: MammutSessionContext):
        """Practice the lessons by training the model with prepared data.

        Args:
            mammut_session_context: The session context from the classroom.
        """
        self.model.train(
            mammut_session_context, **{"corpus": self.preprocessed_data}
        )
        self.model.save(mammut_session_context)


class HuggingFaceRobertaQuestionAnsweringLesson(lesson_base.Lesson):
    """Implements a concrete Lesson to work with bare Roberta
    HuggingFace model curriculum wrapper.
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
        super(HuggingFaceRobertaQuestionAnsweringLesson, self).__init__(
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
        self.dataset = self.get_corpus(self.corpus_id, self._corpus_map_reference)
        self.preprocessed_data = None

    def get_corpus(
            self, corpus_id: int, corpus_map: CorpusMap,
    ):
        """Returns a training corpus from the corpus map.

        Args:
        corpus_id(int): corpus id in corpus map sheet
            in package.
        corpus_map: CorpusMap object from within the
            Package used.

        Returns:
        The corpus instance.
        """

        corpus = corpus_map.get_corpus_by_id(corpus_id)
        dataset = corpus.get_hf_dataset()
        return dataset

    def _get_model_instance(self) -> HuggingFaceRobertaQuestionAnsweringModel:
        return HuggingFaceRobertaQuestionAnsweringModel(
            self.parameters_dict,
            self.course,
            self.lesson_id,
            self._mammut_session_context,
            self.corpus_id,
            self._corpus_map_reference,
        )

    def lecture(self):
        """Loads and prepare the model, tokenizer and data for this lesson.

        Currently, this data is prepared:
            - Download the pretrained model in memory.
        """
        self.preprocessed_data = self.model.tokenize_corpus(self.dataset)
        self.model.load_pretrained_models()

    def practice(self, mammut_session_context: MammutSessionContext):
        """Practice the lessons by training the model with prepared data.

        Args:
        mammut_session_context: The session context from the classroom.
        """
        self.model.train(mammut_session_context, **{"corpus": self.preprocessed_data})
        self.model.save(mammut_session_context)
