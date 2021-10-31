from mammut.common.lexicon.linguistic_standard import LinguisticStandard
from typing import List
from mammut.common.synthetic.synthetic_corpus_generator.token_generator import TokenGenerator


class PrimesGenerator(TokenGenerator):
    """Semantic primes generator class. Encapsulates primes
    generation for other modules
    """

    def __init__(self, standard: LinguisticStandard):
        self.standard = standard

    # Override abstract method
    def get_tokens(
        self, pos: str = "", regional_settings: str = "es"
    ) -> List[str]:
        semantic_primes = self.standard.base_dictionary.lemmas_entries
        semantic_primes = list(
            filter(
                lambda prime: prime.regional_settings_lemma
                == regional_settings,
                semantic_primes,
            )
        )
        semantic_primes = list(map(lambda prime: prime.lemma, semantic_primes))
        return semantic_primes
