# coding=utf-8

from collections import *
from nltk.tokenize.regexp import RegexpTokenizer, re
from nltk.probability import FreqDist
from enum import Enum
import sys

from typing import List, Tuple
from mammut.common import WORD_LEXICAL_RELEVANCE_INDEX_ESTIMATOR_ADD_NEW_SAMPLE
from mammut.models.lexical_relevance import LexicalRelevanceIndexEstimator

class PuntuationType(Enum):
    Dot = 1
    Comma = 2
    Exclamation = 3
    Interrogation = 4
    Column = 5
    SemiColumn = 6


class BasicTokenizerResult:
    # expresion regular para espacios en blanco en espanol
    WHITE_SPACE_REGEX_CHARS = r" \t"
    WHITE_SPACE_REGEX_STR = "[" + WHITE_SPACE_REGEX_CHARS + "]*"
    WHITE_SPACE_REGEX = re.compile(WHITE_SPACE_REGEX_STR)
    # expresion regular para palabras en espanol
    WORD_REGEX_CHARS = r"A-ZÑÁÉÍÓÚÜÇa-zñáéíóúüç\-"
    WORD_REGEX_STR = "[" + WORD_REGEX_CHARS + "]+"
    WORD_REGEX = re.compile(WORD_REGEX_STR)
    # expresion regular para numeros
    NUMBER_REGEX_CHARS = r"0-9"
    NUMBER_REGEX_STR = "[" + NUMBER_REGEX_CHARS + "]+"
    NUMBER_REGEX = re.compile(NUMBER_REGEX_STR)
    # expresion regular para signos de puntuacion
    PUNCTUATION_REGEX_CHARS = r"\.,!¡\?¿:;"
    PUNCTUATION_REGEX_STR = (
        r"\.{3}|[" + PUNCTUATION_REGEX_CHARS + "]" + WHITE_SPACE_REGEX_STR
    )
    PUNCTUATION_REGEX = re.compile(PUNCTUATION_REGEX_STR)
    # expresion regular para comillas
    QUOTE_REGEX_CHARS = r'"\''
    QUOTE_REGEX_STR = "[" + QUOTE_REGEX_CHARS + "]" + WHITE_SPACE_REGEX_STR
    QUOTE_REGEX = re.compile(QUOTE_REGEX_STR)
    # expresion regular para comillas
    PARENTHESIS_REGEX_CHARS = r"\(\)"
    PARENTHESIS_REGEX_STR = "[" + PARENTHESIS_REGEX_CHARS + "]" + WHITE_SPACE_REGEX_STR
    PARENTHESIS_REGEX = re.compile(PARENTHESIS_REGEX_STR)
    # expresion regular para finales de linea
    BREAK_REGEX_CHARS = r"\n"
    BREAK_REGEX_STR = WHITE_SPACE_REGEX_STR + BREAK_REGEX_CHARS
    BREAK_REGEX = re.compile(BREAK_REGEX_STR)
    # expresion regular para encontrar variables
    VARIABLE_REGEX_STR = r"\[[Vv]ariable\|[^\]]+\]"
    VARIABLE_REGEX = re.compile(VARIABLE_REGEX_STR)
    # expresion regular para encontrar images
    IMAGE_REGEX_STR = r"\[[Ii]mage\|[^\]]+\]"
    IMAGE_REGEX = re.compile(IMAGE_REGEX_STR)
    # expresion regular para encontrar botones
    VERBS_REGEX_STR = r"\{\{[Kk][Bb]\-[0-9]+\}\}"
    VERBS_REGEX = re.compile(VERBS_REGEX_STR)
    # expression regular para elementos desconocidos
    UNKNOWN_REGEX_STR = r"[^"
    UNKNOWN_REGEX_STR += WORD_REGEX_CHARS
    UNKNOWN_REGEX_STR += NUMBER_REGEX_CHARS
    UNKNOWN_REGEX_STR += PUNCTUATION_REGEX_CHARS
    UNKNOWN_REGEX_STR += QUOTE_REGEX_CHARS
    UNKNOWN_REGEX_STR += PARENTHESIS_REGEX_CHARS
    UNKNOWN_REGEX_STR += r"\s]+"

    def __init__(
        self,
        base_result: List[str],
        original_text: str,
        stats,
        layer: int,
        regional_settings: str,
        knowledge_graph=None,
    ):
        self.base_result = base_result
        self.original_text = original_text
        self.knowledge_graph = knowledge_graph
        self.regional_settings = regional_settings
        self.words = []
        self.numbers = []
        self.puntuations = []
        self.quotes = []
        self.parenthesis = []
        self.breaks = []
        self.variables = []
        self.invalid_variables = []
        self.images = []
        self.invalid_images = []
        self.verbs = []
        self.invalid_verbs = []
        self.unknowns = []
        self.token_offsets = []
        self.sentence_offsets = []
        self._token_cursor = 0
        self._sentence_cursor = 0
        offset_tuple = None
        for item in self.base_result:
            # Handle separators
            separator = ""
            local_token_cursor = self._token_cursor
            while self.original_text[local_token_cursor] != item[0]:
                separator += self.original_text[local_token_cursor]
                local_token_cursor += 1
            if separator:
                offset_tuple = self.create_token_offset(separator)
                if "\n" in separator:
                    self.create_sentence_offset(offset_tuple)
            # Handle tokens
            if self.is_word(item):
                if stats:
                    word = stats.add_word(item, layer)
                else:
                    word = item.lower()
                self.words.append(word)
                offset_tuple = self.create_token_offset(item)
            elif self.is_number(item):
                if stats:
                    stats.add_number(item)
                self.numbers.append(item)
                offset_tuple = self.create_token_offset(item)
            elif self.is_punctuation(item):
                if stats:
                    stats.add_puntuation(item)
                self.puntuations.append(item)
                offset_tuple = self.create_token_offset(item)
            elif self.is_quote(item):
                if stats:
                    stats.add_quote(item)
                self.quotes.append(item)
                offset_tuple = self.create_token_offset(item)
            elif self.is_parenthesis(item):
                if stats:
                    stats.add_parenthesis(item)
                self.parenthesis.append(item)
                offset_tuple = self.create_token_offset(item)
            elif self.is_break(item):
                if stats:
                    stats.add_break(item)
                self.breaks.append(item)
                offset_tuple = self.create_token_offset(item)
            elif self.is_variable(item):
                variable_name = self.get_variable_name(item)
                if stats:
                    stats.add_variable(variable_name)
                self.variables.append(variable_name)
                if (
                    self.knowledge_graph is not None
                    and not self.knowledge_graph.is_valid_variable(variable_name)
                ):
                    self.invalid_variables.append(variable_name)
                offset_tuple = self.create_token_offset(item)
            elif self.is_image(item):
                image_name = self.get_image_name(item)
                if stats:
                    stats.add_image(image_name)
                self.images.append(image_name)
                if (
                    self.knowledge_graph is not None
                    and not self.knowledge_graph.is_valid_image(image_name)
                ):
                    self.invalid_images.append(image_name)
                offset_tuple = self.create_token_offset(item)
            elif self.is_verb(item):
                verb_id = self.get_verb_id(item)
                if stats:
                    stats.add_verb(verb_id)
                self.verbs.append(verb_id)
                if (
                    self.knowledge_graph is not None
                    and not self.knowledge_graph.is_valid_verb(verb_id)
                ):
                    self.invalid_verbs.append(verb_id)
                offset_tuple = self.create_token_offset(item)
            else:
                if stats:
                    unknown = stats.add_unknown(item)
                else:
                    unknown = item.lower()
                self.unknowns.append(unknown)
                offset_tuple = self.create_token_offset(item)
        # Handle last separators
        separator = ""
        local_token_cursor = self._token_cursor
        while local_token_cursor < len(self.original_text):
            separator += self.original_text[local_token_cursor]
            local_token_cursor += 1
        if separator:
            offset_tuple = self.create_token_offset(separator)
        if offset_tuple:
            self.create_sentence_offset(offset_tuple)

    def create_token_offset(self, token: str):
        offset_tuple = (self._token_cursor, self._token_cursor + (len(token) - 1))
        self._token_cursor = offset_tuple[1] + 1
        self.token_offsets.append(offset_tuple)
        return offset_tuple

    def create_sentence_offset(self, token_offset_tuple: Tuple):
        offset_tuple = (self._sentence_cursor, token_offset_tuple[1])
        self._sentence_cursor = offset_tuple[1] + 1
        self.sentence_offsets.append(offset_tuple)
        return offset_tuple

    def get_variable_name(self, item: str):
        variable_name = item.lower().strip("[]")
        variable_name = variable_name.replace("variable|", "")
        return variable_name

    def get_image_name(self, item: str):
        image_name = item.lower().strip("[]")
        image_name = image_name.replace("image|", "")
        return image_name

    def get_verb_id(self, item: str):
        verb_id = item.upper().strip("{}")
        return verb_id

    def is_word(self, item: str):
        res = BasicTokenizerResult.WORD_REGEX.match(item)
        return res != None

    def is_number(self, item: str):
        res = BasicTokenizerResult.NUMBER_REGEX.match(item)
        return res != None

    def is_punctuation(self, item: str):
        res = BasicTokenizerResult.PUNCTUATION_REGEX.match(item)
        return res != None

    def is_quote(self, item: str):
        res = BasicTokenizerResult.QUOTE_REGEX.match(item)
        return res != None

    def is_parenthesis(self, item: str):
        res = BasicTokenizerResult.PARENTHESIS_REGEX.match(item)
        return res != None

    def is_break(self, item: str):
        res = BasicTokenizerResult.BREAK_REGEX.match(item)
        return res != None

    def is_variable(self, item: str):
        res = BasicTokenizerResult.VARIABLE_REGEX.match(item)
        return res != None

    def is_image(self, item: str):
        res = BasicTokenizerResult.IMAGE_REGEX.match(item)
        return res != None

    def is_verb(self, item: str):
        res = BasicTokenizerResult.VERBS_REGEX.match(item)
        return res != None

    def contains_unknown(self):
        return len(self.unknowns) > 0

    def contains_invalid_variables(self):
        return len(self.invalid_variables) > 0

    def contains_invalid_images(self):
        return len(self.invalid_images) > 0

    def contains_invalid_verbs(self):
        return len(self.invalid_verbs) > 0

    def print(self):
        print("Resultado Base: \n{0}".format(self.base_result))
        print("Palabras: \n{0}".format(self.words))
        print("Numeros: \n{0}".format(self.numbers))
        print("Signos de puntuacion: \n{0}".format(self.puntuations))
        print("Comillas: \n{0}".format(self.quotes))
        print("Parentesis: \n{0}".format(self.parenthesis))
        print("Variables: \n{0}".format(self.variables))
        print("Botones: \n{0}".format(self.verbs))
        print("Desconocidas: \n{0}".format(self.unknowns))


class BasicTokenizerStatistics:
    BasicTokenizerStatisticsSnapshot = namedtuple(
        "BasicTokenizerStatisticsSnapshot",
        ["words_count", "undefined_morphemes_count", "definition"],
    )

    def __init__(self, regional_settings: str):
        self.regional_settings = regional_settings
        self.words = FreqDist()
        self.word_list = []
        self.word_layer = {}
        self.word_lexical_relevance_index_estimator = LexicalRelevanceIndexEstimator(
            self.regional_settings, self.words
        )
        self.numbers = FreqDist()
        self.puntuations = FreqDist()
        self.quotes = FreqDist()
        self.parenthesis = FreqDist()
        self.breaks = FreqDist()
        self.variables = FreqDist()
        self.images = FreqDist()
        self.verbs = FreqDist()
        self.unknowns = FreqDist()
        self.definitions = 0
        self.corpus_entries = 0
        self.snapshots = []

    def add_word(self, word: str, layer: int):
        word_lower = word.lower()
        if self.words[word_lower] == 0:
            self.word_list.append(word_lower)
        if word_lower not in self.word_layer or self.word_layer[word_lower] > layer:
            self.word_layer[word_lower] = layer
        if WORD_LEXICAL_RELEVANCE_INDEX_ESTIMATOR_ADD_NEW_SAMPLE:
            self.word_lexical_relevance_index_estimator.add_new_sample(word_lower)
        self.words[word_lower] += 1
        return word_lower

    def add_number(self, number: str):
        self.numbers[number] += 1

    def add_puntuation(self, puntuation: str):
        self.puntuations[puntuation] += 1

    def add_quote(self, quote: str):
        self.quotes[quote] += 1

    def add_parenthesis(self, parenth: str):
        self.parenthesis[parenth] += 1

    def add_break(self, parenth: str):
        self.breaks[parenth] += 1

    def add_variable(self, variable_name: str):
        self.variables[variable_name] += 1
        return variable_name

    def add_image(self, image_name: str):
        self.images[image_name] += 1
        return image_name

    def add_verb(self, verb_id: str):
        self.verbs[verb_id] += 1
        return verb_id

    def add_unknown(self, unknown: str):
        unknown_lower = unknown.lower()
        self.unknowns[unknown_lower] += 1
        return unknown_lower

    def get_words_generator(self, layer: int = 0, with_index: bool = False):
        current_index = 0
        while current_index < len(self.word_list):
            w = self.word_list[current_index]
            if self.word_layer[w] >= 0 and self.word_layer[w] <= layer:
                if with_index:
                    lexical_relevance_index = self.word_lexical_relevance_index_estimator.get_index(
                        w
                    )
                    yield w, lexical_relevance_index
                else:
                    yield w
            current_index += 1

    def get_word_lexical_relevance_index(self, sample, add):
        return self.word_lexical_relevance_index_estimator.get_index(sample, add)

    def is_word_under_layer(self, word: str, layer=0):
        return word in self.get_words_generator(layer)

    def get_words_count(self):
        count = 0
        current_index = 0
        while current_index < len(self.word_list):
            w = self.word_list[current_index]
            if self.word_layer[w] >= 0:
                count = count + 1
            current_index += 1
        return count

    def create_snapshot(self, undefined_morphemes_count, definition):
        snapshot = BasicTokenizerStatistics.BasicTokenizerStatisticsSnapshot(
            self.get_words_count(), undefined_morphemes_count, definition
        )
        self.snapshots.append(snapshot)

    def get_plot_data(self):
        plot_data_words_count = []
        plot_data_words_count_colors = []
        plot_data_undefined_morphemes_count = []
        plot_data_undefined_morphemes_count_colors = []
        for ss in self.snapshots:
            plot_data_words_count.append(ss.words_count)
            plot_data_undefined_morphemes_count.append(ss.undefined_morphemes_count)
            if ss.definition:
                plot_data_words_count_colors.append(0)
                plot_data_undefined_morphemes_count_colors.append(0)
            else:
                plot_data_words_count_colors.append(1)
                plot_data_undefined_morphemes_count_colors.append(1)
        return (
            plot_data_words_count,
            plot_data_words_count_colors,
            plot_data_undefined_morphemes_count,
            plot_data_undefined_morphemes_count_colors,
        )

    def print(self):
        print("Estadisticas:")
        print("Palabras: \n{0}".format(self.words.items()))
        print("Numeros: \n{0}".format(self.numbers.items()))
        print("Signos de puntuacion: \n{0}".format(self.puntuations.items()))
        print("Comillas: \n{0}".format(self.quotes.items()))
        print("Parentesis: \n{0}".format(self.parenthesis.items()))
        print("Variables: \n{0}".format(self.variables.items()))
        print("Botones: \n{0}".format(self.verbs.items()))
        print("Desconocidas: \n{0}".format(self.unknowns.items()))


class BasicTokenizerStatisticsDict(defaultdict):
    def __init__(self):
        super(BasicTokenizerStatisticsDict, self).__init__(BasicTokenizerStatistics)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret


class BasicTokenizer(RegexpTokenizer):
    """http://www.nltk.org/_modules/nltk/tokenize/regexp.html"""

    def __init__(
        self,
        gaps=False,
        discard_empty=True,
        flags=re.UNICODE | re.MULTILINE | re.DOTALL,
    ):
        self.dictionary = None
        self.stats = BasicTokenizerStatisticsDict()
        pattern = BasicTokenizerResult.VARIABLE_REGEX_STR
        pattern += "|" + BasicTokenizerResult.IMAGE_REGEX_STR
        pattern += "|" + BasicTokenizerResult.VERBS_REGEX_STR
        pattern += "|" + BasicTokenizerResult.WORD_REGEX_STR
        pattern += "|" + BasicTokenizerResult.NUMBER_REGEX_STR
        pattern += "|" + BasicTokenizerResult.PUNCTUATION_REGEX_STR
        pattern += "|" + BasicTokenizerResult.QUOTE_REGEX_STR
        pattern += "|" + BasicTokenizerResult.PARENTHESIS_REGEX_STR
        pattern += "|" + BasicTokenizerResult.BREAK_REGEX_STR
        pattern += "|" + BasicTokenizerResult.UNKNOWN_REGEX_STR
        RegexpTokenizer.__init__(self, pattern, gaps, discard_empty, flags)

    def set_dictionary(self, dictionary):
        self.dictionary = dictionary

    def _tokenize(
        self,
        text: str,
        definition: bool,
        layer: int,
        regional_settings: str,
        knowledge_graph=None,
        exclude_from_stats: bool = False,
    ) -> BasicTokenizerResult:
        base_result = RegexpTokenizer.tokenize(self, text)
        stats = None
        if not exclude_from_stats:
            stats = self.stats[regional_settings]
        result = BasicTokenizerResult(
            base_result, text, stats, layer, regional_settings, knowledge_graph
        )
        undefined_morphemes_count = 0
        if self.dictionary is not None:
            undefined_morphemes_count = self.dictionary.get_undefined_morphemes_count(
                regional_settings
            )
        if not exclude_from_stats:
            self.stats[regional_settings].create_snapshot(
                undefined_morphemes_count, definition
            )
        return result

    def tokenize_definition(self, text: str, layer: int, regional_settings: str, knowledge_graph):
        result = self._tokenize(text, True, layer, regional_settings, knowledge_graph)
        self.stats[regional_settings].definitions += 1
        return result

    def tokenize_corpus_entry(self, text: str, add_to_layer_zero: bool, regional_settings: str):
        # the -1 layer is used to indicate that any word in the text must not be
        # counted as word to define.
        layer = -1
        if add_to_layer_zero:
            layer = 0
        result = self._tokenize(text, False, layer, regional_settings)
        self.stats[regional_settings].corpus_entries += 1
        return result

    def tokenize_out_of_stats(self, text: str, regional_settings: str, knowledge_graph=None):
        result = self._tokenize(
            text, True, sys.maxsize, regional_settings, knowledge_graph, True
        )
        return result
