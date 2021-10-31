from mammut.common.lexicon.dictionary import Dictionary
from mammut.common.lexicon.linguistic_standard import LinguisticStandard
from typing import Set, List
from collections import namedtuple
from mammut.common.synthetic.synthetic_corpus_generator.token_generator import TokenGenerator

BoundMorpheme = namedtuple(
    "BoundMorpheme", ["free", "bound", "mixed", "deleted", "added"]
)


class MorphemesGenerator(TokenGenerator):
    """General morphemes generator. Encapsulates bounded morphemes
    generator heuristics for each language.

    TODO: Only 'es' regional settings is supported.
    This module code might be completely changed with new
    morphological paradigms syntax.
    """

    ES_GENRE_VOCALS: Set = {"a", "o"}

    # Baseline models used in nouns. These should not be
    # considered when creating the list of bounded morphemes
    # since they don't have a free morpheme associated.
    NOUNS_BASELINE_MODELS: Set[str] = {
        "NONS-SIMPLE",
        "MS-SIMPLE",
        "NONP-SIMPLE",
        "MP-SIMPLE",
        "PRE_PART-ing",
    }

    # Baseline models used in adjectives. These should not be
    # considered when creating the list of bounded morphemes
    # since they don't have a free morpheme associated.
    ADJECTIVES_BASELINE_MODELS: Set[str] = {
        "ADJECTIVE_SING_MASC",
        "ADJECTIVE_PLU_MASC",
        "EXCLAMATIVE_SING",
        "EXCLAMATIVE_PLU",
        "INDETER_SING",
        "INDETER_PLU",
        "INTERROGATIVE_SING",
        "INTERROGATIVE_PLU",
        "NUMERAL_ADJ_SING",
        "NUMERAL_ADJ_PLU",
        "POSSESSIVE_ADJ_SING",
        "POSSESSIVE_ADJ_PLU",
        "RELATIVE_SING",
        "RELATIVE_PLU",
        "CUANTITATIVO_SING",
        "CUANTITATIVO_PLU",
        "CUYO_RELATIVE",
    }

    # Verbs models used for the retrieval of
    # verbs bounded morphemes
    VERBS_INCLUDED_MODELS: Set[str] = {"AMAR_3", "TEMER_4"}

    def __init__(self, standard: LinguisticStandard,
                 dictionary: Dictionary):
        self.standard = standard
        self.dictionary = dictionary

    # Overriding abstract method
    def get_tokens(
            self, pos: str = "", regional_settings: str = "es"
    ) -> List[BoundMorpheme]:
        """Return the List[BoundMorpheme] that results
        from the application of Standard morpheme paradigms
        to word models.
        """
        if pos == "NOUN":
            return self._generate_nouns(regional_settings)
        elif pos == "ADJ":
            return self._generate_adjectives(regional_settings)
        elif pos == "VERB":
            return self._generate_verbs(regional_settings)
        else:
            return []

    def _get_nouns_morpheme_paradigms(self, regional_settings: str):
        paradigms_producers = self.standard.morpheme_paradigms["NOUN"][
            regional_settings
        ]
        paradigms_producers = dict(
            filter(
                lambda paradigm: not paradigm[0] in self.NOUNS_BASELINE_MODELS,
                paradigms_producers.producers.items(),
            )
        )
        return paradigms_producers

    def _get_adjectives_morpheme_paradigms(self, regional_settings: str):
        # Remove baseline paradigms producers
        paradigms_producers = self.standard.morpheme_paradigms["ADJ"][
            regional_settings
        ]
        paradigms_producers = dict(
            filter(
                lambda paradigm: not paradigm[0]
                                     in self.ADJECTIVES_BASELINE_MODELS,
                paradigms_producers.producers.items(),
            )
        )
        return paradigms_producers

    def _get_verbs_morpheme_paradigms(self, regional_settings: str):
        paradigms_producers = self.standard.morpheme_paradigms["VERB"][
            regional_settings
        ]
        paradigms_producers = dict(
            filter(
                lambda paradigm: paradigm[0] in self.VERBS_INCLUDED_MODELS,
                paradigms_producers.producers.items(),
            )
        )
        return paradigms_producers

    def _generate_nouns(self, regional_settings: str):
        # Remove baseline paradigms producers
        paradigms_producers = self._get_nouns_morpheme_paradigms(regional_settings)
        ret = []
        for key, val in paradigms_producers.items():
            self._process_noun_paradigms(key, val.inflection_rules, ret)

        return ret

    def _generate_adjectives(self, regional_settings: str):
        paradigms_producers = self._get_adjectives_morpheme_paradigms(regional_settings)
        ret = []
        for key, val in paradigms_producers.items():
            self._process_adjective_paradigms(key, val.inflection_rules, ret)

        return ret

    def _generate_verbs(self, regional_settings: str):
        # Keep only relevant paradigms
        paradigms_producers = self._get_verbs_morpheme_paradigms(regional_settings)
        ret = []
        for key, val in paradigms_producers.items():
            self._process_verb_paradigms(key.split("_")[0], val.inflection_rules, ret)

        return ret

    def get_free_lemma_from_dictionary(self) -> List[BoundMorpheme]:
        """Returns the List[BoundMorphemes] that results from
        the application of Standard morpheme paradigms to the
        lexicon lemmas.
        """
        lemmas = self.dictionary.lemmas_entries
        lemmas = list(filter(
            lambda lemma: lemma.postags_entries[0].pos_tag in ["VERB", "NOUN", "ADJ"],
            lemmas
        ))
        lemmas_nouns = list(filter(
            lambda lemma: lemma.postags_entries[0].pos_tag == "NOUN" and
                not lemma.postags_entries[0].morpheme_paradigm in self.NOUNS_BASELINE_MODELS,
            lemmas
        ))
        lemmas_adjectives = list(filter(
            lambda lemma: lemma.postags_entries[0].pos_tag == "ADJ" and
                          not lemma.postags_entries[0].morpheme_paradigm in self.ADJECTIVES_BASELINE_MODELS,
            lemmas
        ))
        lemmas_verbs = list(filter(
            lambda lemma: lemma.postags_entries[0].pos_tag == "VERB" and
                          lemma.postags_entries[0].morpheme_paradigm in self.VERBS_INCLUDED_MODELS,
            lemmas
        ))
        nouns_paradigms_producers = self._get_nouns_morpheme_paradigms('es')
        nouns_ret = []
        for noun_lemma in lemmas_nouns:
            pp = nouns_paradigms_producers[noun_lemma.postags_entries[0].morpheme_paradigm]
            self._process_noun_paradigms(noun_lemma.lemma, pp.inflection_rules, nouns_ret)

        adjectives_paradigms_producers = self._get_adjectives_morpheme_paradigms('es')
        adjectives_ret = []
        for adjective_lemma in lemmas_adjectives:
            pp = adjectives_paradigms_producers[adjective_lemma.postags_entries[0].morpheme_paradigm]
            self._process_adjective_paradigms(adjective_lemma.lemma, pp.inflection_rules, adjectives_ret)

        verbs_paradigms_producers = self._get_verbs_morpheme_paradigms('es')
        verbs_ret = []
        for verb_lemma in lemmas_verbs:
            pp = verbs_paradigms_producers[verb_lemma.postags_entries[0].morpheme_paradigm]
            self._process_verb_paradigms(verb_lemma.lemma, pp.inflection_rules, verbs_ret)

        return nouns_ret + adjectives_ret + verbs_ret

    def _process_noun_paradigms(self, word, rules, ret_list):
        """Apply an heuristic for nouns, for identification
        of free/bound morphemes in the word forms.

        Note: used for 'es' regional settings

        It mutates the reference object ret_list.
        """
        word_model = word.lower()
        for rule in rules:
            morpheme = rule.apply(word_model)
            bound = ""
            free = ""
            mixed = False
            if (
                    word_model == morpheme.text
                    and word_model[len(word_model) - 1] in self.ES_GENRE_VOCALS
            ):
                free = word_model[0: len(word_model) - 1]
                bound = word_model[len(word_model) - 1]
            elif word_model == morpheme.text:
                free = morpheme.text
                mixed = True
            elif not morpheme.deleted:
                if (
                        word_model[len(word_model) - 1] in self.ES_GENRE_VOCALS
                        or word_model[len(word_model) - 1] == "e"
                ):
                    bound = "".join(
                        list(word_model[len(word_model) - 1])
                        + morpheme.added
                    )
                    free = word_model[0: len(word_model) - 1]
                else:
                    bound = "".join(morpheme.added)
                    free = word_model
            elif len(morpheme.deleted) == 1 and (
                    morpheme.deleted[0] == "z"
                    or morpheme.deleted[0] in self.ES_GENRE_VOCALS
            ):
                bound = "".join(morpheme.added)
                free = word_model[0: len(word_model) - 1]
            else:
                bound = "".join(morpheme.deleted + morpheme.added)
                free = word_model[
                       0: len(word_model) - len(morpheme.deleted)
                       ]
            ret_list.append(
                BoundMorpheme(
                    free, bound, mixed, morpheme.deleted, morpheme.added
                )
            )

    def _process_adjective_paradigms(self, word, rules, ret_list):
        """Apply an heuristic for adjectives, for identification
        of free/bound morphemes in the word forms.

        Note: used for 'es' regional settings

        It mutates the reference object ret_list.
        """
        word_model = word.lower()
        for rule in rules:
            morpheme = rule.apply(word_model)
            bound = ""
            free = ""
            mixed = False
            if (
                    word_model == morpheme.text
                    and word_model[len(word_model) - 1] in self.ES_GENRE_VOCALS
            ):
                free = word_model[0: len(word_model) - 1]
                bound = word_model[len(word_model) - 1]
            elif word_model == morpheme.text:
                free = morpheme.text
                mixed = True
            elif not morpheme.deleted:
                if (
                        word_model[len(word_model) - 1] in self.ES_GENRE_VOCALS
                        or word_model[len(word_model) - 1] == "u"
                        or word_model[len(word_model) - 1] == "i"
                ):
                    bound = "".join(
                        list(word_model[len(word_model) - 1])
                        + morpheme.added
                    )
                    free = word_model[0: len(word_model) - 1]
                else:
                    bound = "".join(morpheme.added)
                    free = word_model
            elif len(morpheme.deleted) == 1 and (
                    morpheme.deleted[0] == "z"
                    or morpheme.deleted[0] in self.ES_GENRE_VOCALS
                    or morpheme.deleted[0] == "e"
            ):
                bound = "".join(morpheme.added)
                free = word_model[0: len(word_model) - 1]
            else:
                bound = "".join(morpheme.deleted + morpheme.added)
                free = word_model[
                       0: len(word_model) - len(morpheme.deleted)
                       ]
            ret_list.append(
                BoundMorpheme(
                    free, bound, mixed, morpheme.deleted, morpheme.added
                )
            )

    def _process_verb_paradigms(self, word, rules, ret_list):
        """Apply an heuristic for verbs for identification
        of free/bound morphemes in the word forms.

        Note: used for 'es' regional settings

        It mutates the reference object ret_list.
        """
        word_model = word.lower()
        for rule in rules:
            morpheme = rule.apply(word_model)
            bound = ""
            free = ""
            mixed = False
            if not morpheme.deleted:
                bound = "".join(
                    list(word_model[len(word_model) - 2:])
                    + morpheme.added
                )
                free = word_model[0: len(word_model) - 2]
            else:
                if len(morpheme.deleted) == 2:
                    bound = "".join(morpheme.added)
                    free = word_model[
                           0: len(word_model) - len(morpheme.deleted)
                           ]
                elif len(morpheme.deleted) == 1:
                    bound = "".join(
                        list(word_model[len(word_model) - 2])
                        + morpheme.added
                    )
                    free = word_model[0: len(word_model) - 2]

                else:
                    bound = "".join(
                        list(word_model[len(word_model) - 2:])
                        + morpheme.added
                    )
                    free = word_model[0: len(word_model) - 2]
            ret_list.append(
                BoundMorpheme(
                    free, bound, mixed, morpheme.deleted, morpheme.added
                )
            )