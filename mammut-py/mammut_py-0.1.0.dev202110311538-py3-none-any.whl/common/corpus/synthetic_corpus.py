import json

from mammut.common.lexicon.dictionary import Dictionary
from mammut.common.lexicon.linguistic_standard import LinguisticStandard
from mammut.common.synthetic.synthetic_corpus_generator.morphemes_generator import (
    MorphemesGenerator,
)
from mammut.common.synthetic.synthetic_corpus_generator.synthetic_corpus_generator import (
    SyntheticCorpusGenerator,
)
from mammut.common.corpus.corpus_operations import CorpusOperations
from typing import List


class SyntheticCorpus(CorpusOperations):
    """Synthetic Corpus support in corpus map sheet.

    Parameters for the SyntheticCorpusGeneratorClass
    can be specified using the configuration_json column
    in corpus map sheet.
    """

    def __init__(
        self,
        spreadsheet_id: str,
        id,
        dictionary: Dictionary,
        standard: LinguisticStandard,
        regional_settings: str,
        json_parameters,
    ):
        """

        :param spreadsheet_id: spreadsheet id used for corpus indexing
        :param id:
        :param dictionary:
        :param standard:
        :param regional_settings:
        :param json_parameters:
        """
        self.configuration = json.loads(json_parameters)
        self.id = id
        self.spreadsheet_id = spreadsheet_id
        self.regional_settings = regional_settings
        self.events: List[str] = []
        """
            Length to split the synthetic data into substrings of text,
            representing sentences. 
        """
        self._events_tokens_length: int = self.configuration[
            "events_tokens_length"
        ]
        self.morphemes_generator = MorphemesGenerator(standard, dictionary)
        self.synthetic_corpus_generator = SyntheticCorpusGenerator(
            self.morphemes_generator
        )
        self._generate_synthetic_tokens()

    def _generate_synthetic_tokens(self):
        """
            Generates the synthetic tokens for this corpus events.
        """
        tokens_text: List[
            str
        ] = self.synthetic_corpus_generator.generate_synthetic_corpus(
            self.configuration["nouns_words"],
            self.configuration["adjectives_words"],
            self.configuration["verbs_words"],
            self.configuration["nouns_bound"],
            self.configuration["adjectives_bound"],
            self.configuration["verbs_bound"],
            self.configuration["free_lemma_words"],
            self.configuration["random_ext"],
        )
        """
            Segment the list in segments of the specified _event_tokens_length.
            After that, each segmented list is joined as a string separated by 
            space character.
        """
        segmented_tokens = list(map(
            lambda token: " ".join(token),
            [
                tokens_text[x: x + self._events_tokens_length]
                for x in range(0, len(tokens_text), self._events_tokens_length)
            ]
        ))
        self.events = segmented_tokens

    @property
    def indexable(self) -> bool:
        return False

    @property
    def annotable(self) -> bool:
        return False

    def get_events_as_strings(self) -> List[str]:
        return self.events
