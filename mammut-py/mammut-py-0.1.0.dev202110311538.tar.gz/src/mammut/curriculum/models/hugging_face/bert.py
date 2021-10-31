from mammut.curriculum.models.hugging_face.pre_trained_model import (
    HuggingFacePreTrainedModel,
)
from transformers import BertModel, BertTokenizer, BertForTokenClassification
import mammut.curriculum.report as report
from mammut.common.corpus.corpus_map import CorpusMap
from typing import Dict
from mammut.curriculum.core.mammut_session_context import MammutSessionContext


class HuggingFaceBertBaseModel(HuggingFacePreTrainedModel):
    """This is a wrapper for the Bert Model transformer.

    https://huggingface.co/transformers/model_doc/bert.html#bertmodel

    """

    def __init__(
        self,
        parameters: Dict,
        course_id: int,
        lesson_id: int,
        mammut_session_context: MammutSessionContext,
        corpus_id: int,
        corpus_map: CorpusMap,
    ):
        """
       Args:
          parameters: The model parameters parsed JSON.
          course_id (int): the course ID to which this model belongs.
          lesson_id (int): the lesson ID to which this model belongs.
          mammut_session_context: Mammut session context with general information about
               current curriculum instance.
       """
        super(HuggingFaceBertBaseModel, self).__init__(
            parameters, course_id, lesson_id, mammut_session_context, corpus_id, corpus_map
        )

    def load_pretrained_models(self) -> None:
        """Load the pretrained model for this BERT wrapper. """
        self._model = BertModel.from_pretrained(self._name_or_path)
        self._tokenizer = BertTokenizer.from_pretrained(self._name_or_path)

    def train(self, mammut_session_context: MammutSessionContext, **kwargs):
        """Train the Bert base model in the lesson.

        Note: Nothing to train yet.
        Todo: Collaboration between Mammut Corpus (or other data source) and
            this model needs to be defined.
        """
        report.send_message(
            report.CurriculumGeneralDebugMessage(
                "Training HuggingFaceBertBase model"
            )
        )
        pass

    def get_corpus(
        self, corpus_id: int, corpus_map: CorpusMap,
    ):
        """
        Todo: Deprecated. Remove after new Hugging Face Model structure integration.
        """
        return corpus_map.get_corpus_by_id(corpus_id).get_events_as_strings()


class HuggingFaceBertTokenClassificationModel(HuggingFacePreTrainedModel):
    """This is a wrapper for the BertForTokenClassification model

    https://huggingface.co/transformers/model_doc/bert.html#bertfortokenclassification

    """

    def __init__(
        self,
        parameters: Dict,
        course_id: int,
        lesson_id: int,
        mammut_session_context: MammutSessionContext,
        corpus_id: int,
        corpus_map: CorpusMap,
    ):
        """
        Args:
          parameters: The model parameters parsed JSON.
          course_id (int): the course ID to which this model belongs.
          lesson_id (int): the lesson ID to which this model belongs.
          mammut_session_context: Mammut session context with general information about
               current curriculum instance.
       """
        super(HuggingFaceBertTokenClassificationModel, self).__init__(
            parameters, course_id, lesson_id, mammut_session_context, corpus_id, corpus_map
        )

    def load_pretrained_models(self) -> None:
        """Load the pretrained model for this BERT wrapper. """
        self._model = BertForTokenClassification.from_pretrained(
            self._name_or_path
        )
        self._tokenizer = BertTokenizer.from_pretrained(self._name_or_path)

    def train(self, mammut_session_context: MammutSessionContext, **kwargs):
        """Train this NER model in the lesson.

        Note: nothing to train yet.
        Todo: Collaboration between Mammut Corpus (or other data source) and
            this model needs to be defined.
        """
        report.send_message(
            report.CurriculumGeneralDebugMessage(
                "Training HuggingFaceBertTokenClassificationModel model"
            )
        )
        pass

    def get_corpus(
        self, corpus_id: int, corpus_map: CorpusMap,
    ):
        """
        Todo: Deprecated. Remove after new Hugging Face Model structure integration.
        """
        return corpus_map.get_corpus_by_id(corpus_id).get_events_as_strings()
