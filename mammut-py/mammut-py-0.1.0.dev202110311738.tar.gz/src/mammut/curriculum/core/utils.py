import enum


class LanguageLevel(enum.Enum):
    """Enumeration type for language levels
    in Mammut language architecture.

    https://doc.mammut.io/docs_es/framework/language_arquitecture/
    """

    LexicalMorphological = 1
    LexicalSemantic = 2
    SyntacticSemantic = 3
    SemanticPragmatic = 4

    @staticmethod
    def from_str(label):
        if label == "LexicalMorphological":
            return LanguageLevel.LexicalMorphological
        elif label == "LexicalSemantic":
            return LanguageLevel.LexicalSemantic
        elif label == "SyntacticSemantic":
            return LanguageLevel.SyntacticSemantic
        elif label == "SemanticPragmatic":
            return LanguageLevel.SemanticPragmatic
        else:
            raise NotImplementedError


class LanguageCompetence(enum.Enum):
    """Enumeration type for language competences.

    Language competences are directly evaluated through
    Lessons in the Curriculum.

    Each Lesson will assess a language competence.
    """

    Conjugation = 1
    GenderIdentification = 2
    NumberIdentification = 3
    WordIdentification = 4
    ReadingCapabilities = 5

    @staticmethod
    def from_str(label):
        if label == "Conjugation":
            return LanguageCompetence.Conjugation
        elif label == "GenderIdentification":
            return LanguageCompetence.GenderIdentification
        elif label == "NumberIdentification":
            return LanguageCompetence.NumberIdentification
        elif label == "WordIdentification":
            return LanguageCompetence.WordIdentification
        elif label == "ReadingCapabilities":
            return LanguageCompetence.ReadingCapabilities
        else:
            raise NotImplementedError
