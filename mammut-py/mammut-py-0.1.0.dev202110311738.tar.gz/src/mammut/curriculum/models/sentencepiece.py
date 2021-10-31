from mammut.curriculum.models.model_base import ModelBase
from sentencepiece import SentencePieceTrainer, SentencePieceProcessor
from typing import List
import io
from abc import abstractmethod
from typing import Optional, Dict
import mammut.curriculum.report as report
from mammut.curriculum.core.mammut_session_context import MammutSessionContext


class SentencepieceBaseModel(ModelBase):
    def __init__(self, parameters: Dict, course_id: int, lesson_id: int):
        ModelBase.__init__(self, parameters, course_id, lesson_id)
        """
            Attribute sp_preprocessor contains the SentencePiece 
            preprocessor object developed by third party.
        """
        self.sp_preprocessor: Optional[SentencePieceProcessor] = None
        self._model_io: io.BytesIO = None

    @property
    @abstractmethod
    def model_name(self) -> str:
        pass

    def train(self, mammut_session_context: MammutSessionContext, **kwargs):
        """Train the model this class implements.

        Args:
            **vocabulary_size (int): vocabulary size, default to 8000.
            **whitespace_as_suffix(bool): treat whitespace marker as suffix
                instead of prefix.
        """
        self._model_io = io.BytesIO()
        vocabulary_size = self.parameters["vocabulary_size"]
        whitespace_as_suffix = self.parameters["treat_whitespace_as_suffix"]
        corpus = kwargs["corpus"]
        self._train_subword_unit(vocabulary_size, whitespace_as_suffix, corpus)

    def save(self, mammut_session_context: MammutSessionContext, **kwargs):
        """Persist the model in memory.
        """
        model_file_system_path = self._get_model_file_system_path(
            mammut_session_context.curriculum_save_folder
        )
        report.send_message(
            report.CurriculumGeneralDebugMessage(
                f"Save Sentencepiece model in: {model_file_system_path}"
            )
        )
        pass

    def _train_subword_unit(
        self, vocabulary_sz: int, whitespace_as_suffix: bool, corpus: List[str]
    ):
        # Todo: Study this params and their meaning.
        pad_id = 0
        unk_id = 1
        bos_id = 2
        eos_id = 3
        corpus_iter = corpus.__iter__()
        SentencePieceTrainer.Train(
            sentence_iterator=corpus_iter,
            model_writer=self._model_io,
            vocab_size=vocabulary_sz,
            treat_whitespace_as_suffix=whitespace_as_suffix,
            pad_id=pad_id,
            unk_id=unk_id,
            bos_id=bos_id,
            eos_id=eos_id,
            model_type=self.model_name,
        )
        self._load_subword_model()

    def _load_subword_model(self):
        self.sp_preprocessor = SentencePieceProcessor(
            model_proto=self._model_io.getvalue()
        )


class SentencePieceBPEModel(SentencepieceBaseModel):
    def __init__(self, parameters: Dict, course_id: int, lesson_id: int):
        SentencepieceBaseModel.__init__(self, parameters, course_id, lesson_id)

    @property
    def model_name(self) -> str:
        return "bpe"


class SentencePieceNGRAMModel(SentencepieceBaseModel):
    def __init__(self, parameters: Dict, course_id: int, lesson_id: int):
        SentencepieceBaseModel.__init__(self, parameters, course_id, lesson_id)

    @property
    def model_name(self) -> str:
        return "unigram"
