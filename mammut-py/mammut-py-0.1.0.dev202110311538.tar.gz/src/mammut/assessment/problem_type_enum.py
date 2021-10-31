import enum
from mammut.assessment import (
    sentence_piece_problem,
    mock_problem,
    tokenizer_problems,
    token_classification_problems,
)
from typing import List, Tuple


class ProblemType(enum.Enum):
    """Enumeration for checklist test types.

    Enumeration values are custom classes for problem types.

    Enumeration naming follows a convention:

        Problem category name + "_" +  Model name

    For example: For a minimal functionality test problem
    implemented for Sentencepiece, the enum name will be:

        MFT_Sentencepiece
    """

    """
        Minimal functionality test problems
    """
    MFT_SentencePiece = sentence_piece_problem.SentencepieceProblemMFT
    MFT_SpecialToken = tokenizer_problems.SpecialTokenProblemMFT
    MFT_TokenClassification = token_classification_problems.RobertaTokenClassificationProblemMFT

    """
        Invariance functionality test
    """
    INV_SentencePiece = sentence_piece_problem.SentencepieceProblemINV

    """
        General category. (Problem not tied to any specific category)
    """
    General_Mock = mock_problem.MockProblem

    @classmethod
    def list(cls) -> List[Tuple]:
        """Returns a list of pairs for the enumeration names and values.
        """
        return list(map(lambda e: (e.name, e.value), cls))

    @classmethod
    def names(cls) -> List[str]:
        """Returns the list of enumeration names
        """
        return list(map(lambda e: e.name, cls))
