import enum
from mammut.curriculum.lesson.sentencepiece_lessons import (
    SentencepieceBPELesson,
    SentencepieceNGRAMLesson,
)
from mammut.curriculum.lesson.mock_lesson import MockLesson
from mammut.curriculum.lesson.hugging_face_lessons import (
    HuggingFaceBertBaseLesson,
    HuggingFaceBertTokenClassificationLesson,
    HuggingFaceRobertaTokenClassificationLesson,
    HuggingFaceRobertaSequenceClassificationLesson,
    HuggingFaceRobertaQuestionAnsweringLesson
)
from typing import List, Tuple


class LessonType(enum.Enum):
    """Enumeration for Lessons types, based on models tags.

    Enumeration values are custom classes for lessons types, which encapsulates
    lessons models.

    Each LessonType name maps to a model concrete type class.
    """

    SentencePieceBPE = SentencepieceBPELesson
    SentencePieceNGRAM = SentencepieceNGRAMLesson
    TestMock = MockLesson
    HuggingFaceBertBase = HuggingFaceBertBaseLesson
    HuggingFaceBertTokenClassification = (
        HuggingFaceBertTokenClassificationLesson
    )
    HuggingFaceRobertaTokenClassification = HuggingFaceRobertaTokenClassificationLesson
    HuggingFaceRobertaSequenceClassification = HuggingFaceRobertaSequenceClassificationLesson
    HuggingFaceRobertaQuestionAnswering = HuggingFaceRobertaQuestionAnsweringLesson


    @classmethod
    def list(cls) -> List[Tuple]:
        """Returns a list of pairs for the enumeration names and values
        """
        return list(map(lambda e: (e.name, e.value), cls))

    @classmethod
    def names(cls) -> List[str]:
        """Returns a list of pairs for the enumeration names and values
        """
        return list(map(lambda e: e.name, cls))
