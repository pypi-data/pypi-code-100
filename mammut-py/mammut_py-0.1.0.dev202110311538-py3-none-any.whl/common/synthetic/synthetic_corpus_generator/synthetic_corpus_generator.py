from typing import List

from mammut.common.synthetic.synthetic_corpus_generator.morphemes_generator import (
    MorphemesGenerator,
)
import random
import string


def generate_n_random_free(n: int, ext: int) -> List[str]:
    """Generates n unique random strings.

    TODO: Formalize the upper limit of n.

    Args:
        n(int): The number of strings to generate.
        ext(int): The number of chars in the random
            strings.

    Returns:
        The list of generated random strings
    """

    def get_random_char():
        return random.choice(string.ascii_letters)

    def get_random_string():
        s = list(get_random_char())
        for j in range(0, ext - 1):
            t_s = s + list(get_random_char())
            c = 0
            while "".join(t_s) in generated_count:
                t_s = s + list(get_random_char())
                c += 1
                if c == 100:
                    break

            s = t_s
            generated_count.add("".join(s))
        return "".join(s)

    generated_count = set()
    ret = []
    for i in range(0, n):
        ret.append(get_random_string())
    return ret


class SyntheticCorpusGenerator:
    """Synthetic corpus generation class
    Encapsulates the algorithm and considerations
    for the retrieval of a synthetic corpus:
    - Substitution rules for free morphemes character
    - Accountability of frequencies
    - Handling of distributions for each type of
        synthetic corpus
    """

    def __init__(self, morpheme_generator: MorphemesGenerator):
        self.morphemes_generator = morpheme_generator

    def generate_synthetic_corpus(
        self,
        nouns_words: int,
        adjectives_words: int,
        verbs_words: int,
        nouns_bound: int,
        adjectives_bound: int,
        verbs_bound: int,
        free_lemma_words: int,
        random_ext: int = 3
    ) -> List[str]:

        if random_ext < 3:
            raise Exception("Random string length too short. Introduce a value >= 3")

        free_lemma_words_arr = []
        nouns_words_arr = []
        adjectives_words_arr = []
        verbs_words_arr = []
        nouns_bound_arr = []
        adjectives_bound_arr = []
        verbs_bound_arr = []

        if free_lemma_words >= 1:
            free_lemma_words_arr = [m.free for m in self.morphemes_generator.get_free_lemma_from_dictionary() if not m.mixed]
            free_lemma_words_arr = list(set(map(
                lambda morpheme_paradigm: morpheme_paradigm, free_lemma_words_arr
            )))
            for i in range(0, free_lemma_words):
                free_lemma_words_arr = free_lemma_words_arr + free_lemma_words_arr

        if nouns_words >= 1:
            nouns_words_arr = [
                m
                for m in self.morphemes_generator.get_tokens("NOUN", "es")
                if not m.mixed
            ]
            for i in range(0, nouns_words):
                nouns_words_arr = nouns_words_arr + [
                    m
                    for m in self.morphemes_generator.get_tokens("NOUN", "es")
                    if not m.mixed
                ]

        if adjectives_words >= 1:
            adjectives_words_arr = [
                m
                for m in self.morphemes_generator.get_tokens("ADJ", "es")
                if not m.mixed
            ]
            for i in range(0, adjectives_words):
                adjectives_words_arr = adjectives_words_arr + [
                    m
                    for m in self.morphemes_generator.get_tokens("ADJ", "es")
                    if not m.mixed
                ]

        if verbs_words >= 1:
            verbs_words_arr = [
                m
                for m in self.morphemes_generator.get_tokens("VERB", "es")
                if not m.mixed
            ]
            for i in range(0, verbs_words):
                verbs_words_arr = verbs_words_arr + [
                    m
                    for m in self.morphemes_generator.get_tokens("VERB", "es")
                    if not m.mixed
                ]

        if nouns_bound >= 1:
            nouns_bound_arr = list(
                set(
                    [
                        m.bound
                        for m in self.morphemes_generator.get_tokens(
                            "NOUN", "es"
                        )
                        if not m.mixed
                    ]
                )
            )
            for i in range(0, nouns_bound):
                nouns_bound_arr = nouns_bound_arr + list(
                    set(
                        [
                            m.bound
                            for m in self.morphemes_generator.get_tokens(
                                "NOUN", "es"
                            )
                            if not m.mixed
                        ]
                    )
                )

        if adjectives_bound >= 1:
            adjectives_bound_arr = list(
                set(
                    [
                        m.bound
                        for m in self.morphemes_generator.get_tokens(
                            "ADJ", "es"
                        )
                        if not m.mixed
                    ]
                )
            )
            for i in range(0, adjectives_bound):
                adjectives_bound_arr = adjectives_bound_arr + list(
                    set(
                        [
                            m.bound
                            for m in self.morphemes_generator.get_tokens(
                                "ADJ", "es"
                            )
                            if not m.mixed
                        ]
                    )
                )

        if verbs_bound >= 1:
            verbs_bound_arr = list(
                set(
                    [
                        m.bound
                        for m in self.morphemes_generator.get_tokens(
                            "VERB", "es"
                        )
                        if not m.mixed
                    ]
                )
            )
            for i in range(0, verbs_bound):
                verbs_bound_arr = verbs_bound_arr + list(
                    set(
                        [
                            m.bound
                            for m in self.morphemes_generator.get_tokens(
                                "VERB", "es"
                            )
                            if not m.mixed
                        ]
                    )
                )

        return self._generate_tokens(
            nouns_words_arr,
            adjectives_words_arr,
            verbs_words_arr,
            nouns_bound_arr,
            adjectives_bound_arr,
            verbs_bound_arr,
            free_lemma_words_arr,
            random_ext
        )

    def _generate_tokens(
        self,
        nouns_words,
        adjectives_words,
        verbs_words,
        nouns_bound: List[str],
        adjectives_bound: List[str],
        verbs_bound: List[str],
        free_lemmas_words: List[str],
        random_ext: int
    ) -> List[str]:
        ret_list = nouns_words + adjectives_words + verbs_words
        bound_morphemes_set = set([m.bound for m in nouns_words + adjectives_words + verbs_words])
        random_frees = generate_n_random_free(len(ret_list), random_ext)
        free_dict = dict()
        bound_dict = dict()
        ret_list_free_altered = []

        for morpheme in ret_list:
            free_morpheme = random_frees.pop()
            if free_morpheme in free_dict:
                free_dict[free_morpheme] += 1
            else:
                free_dict[free_morpheme] = 1

            if morpheme.bound in bound_dict:
                bound_dict[morpheme.bound] += 1
            else:
                bound_dict[morpheme.bound] = 1

            ret_list_free_altered.append(free_morpheme + morpheme.bound)

        free_lemmas_words = list(free_lemmas_words)
        random_bound = generate_n_random_free(len(free_lemmas_words), random_ext)
        free_lemmas_words_random_suffix = list(
            map(lambda f_w: f_w + random_bound.pop(), free_lemmas_words)
        )

        unsorted_tokens = (
            ret_list_free_altered
            + nouns_bound
            + adjectives_bound
            + verbs_bound
            + free_lemmas_words_random_suffix
        )

        for i in nouns_bound:
            bound_morphemes_set.add(i)
        for i in adjectives_bound:
            bound_morphemes_set.add(i)
        for i in verbs_bound:
            bound_morphemes_set.add(i)

        random.shuffle(unsorted_tokens)
        return list(free_lemmas_words) + list(bound_morphemes_set) + list(unsorted_tokens)
