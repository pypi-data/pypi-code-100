from mammut.common.corpus.synthetic_corpus import SyntheticCorpus
from mammut.curriculum.models.model_base import ModelBase
import mammut.curriculum.report as report
from transformers import PreTrainedModel
from mammut.common.corpus.corpus_map import CorpusMap
from datasets import *
from mammut.curriculum.core.mammut_session_context import MammutSessionContext
from mammut.curriculum.report.errors.json_parsing_errors import (
    ModelRequiredParameterMissingKey,
)
from typing import Dict


class HuggingFacePreTrainedModel(ModelBase):
    """This is a wrapper for hugging face pretrained models, to provide
    collaboration between hugging face models and currriculum code.

    This provides a `_model` field to store the concrete model instance.
    Child classes are responsibly for correct initialization of `_model`
    field.

    This also provides a `_tokenizer` field to store the tokenizer for the
    model. When pretraining, the tokenizer will be needed. Also, if predictions
    are computed using the model directly, the input needs to be tokenized
    explicitly.

    The Model can easily receive the context from the Lesson as a simple association
    when required.
    """

    # Parameters constants class attributes.
    PRETRAINED_FROM_PARAM_STR = "pretrained_from"

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
        super(HuggingFacePreTrainedModel, self).__init__(
            parameters, course_id, lesson_id
        )

        if self.PRETRAINED_FROM_PARAM_STR not in self.parameters:
            raise ModelRequiredParameterMissingKey(
                self.PRETRAINED_FROM_PARAM_STR, course_id, lesson_id
            )

        else:
            pretrained_from = parameters[self.PRETRAINED_FROM_PARAM_STR]
            if isinstance(pretrained_from, str):
                self._name_or_path = pretrained_from

            elif isinstance(pretrained_from, dict):
                if "course" not in pretrained_from:
                    raise ModelRequiredParameterMissingKey(
                        "pretrained_from.course", course_id, lesson_id
                    )

                if "lesson" not in pretrained_from:
                    raise ModelRequiredParameterMissingKey(
                        "pretrained_from.lesson", course_id, lesson_id
                    )

                pretrained_course_id = pretrained_from["course"]
                pretrained_lesson_id = pretrained_from["lesson"]
                self._name_or_path = self.get_model_file_system_path(
                    mammut_session_context.curriculum_save_folder,
                    pretrained_course_id,
                    pretrained_lesson_id,
                )

        self._model: Optional[PreTrainedModel] = None

    def save(
        self, mammut_session_context: MammutSessionContext, **kwargs
    ) -> None:
        """Saves the model in the file system path provided.

        Args:
            save_model_path: file system path to save the trained model.
            **kwargs: Any other custom attribute.
        """
        model_file_system_path = self._get_model_file_system_path(
            mammut_session_context.curriculum_save_folder
        )
        report.send_message(
            report.CurriculumGeneralDebugMessage(
                f"Saving HuggingFacePretrainedModel in {model_file_system_path}"
            )
        )
        self._model.save_pretrained(model_file_system_path)
        self._tokenizer.save_pretrained(model_file_system_path)

    def load_pretrained_models(self) -> None:
        """Load the pretrained Hugging face model.

        All hugging face models can be load from a pre-trained model,
        which could be stored in the remote hugging face's models hub,
        or in the local file system.
        """
        pass

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
