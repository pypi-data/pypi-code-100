# coding=utf-8
from elasticsearch import Elasticsearch
from mammut import ES_HOSTS, CONCORDANCE_QUERY_SIZE
from mammut.common import corpus
from mammut.common.corpus.constants import CorpusTable


class Concordance:
    NUMBER_OF_WORDS = 8
    NUMBER_OF_CHARS = 50
    SEPARATOR_CHARS = ["*", "(", ")"]

    def __init__(self):
        self.elasticsearch = Elasticsearch(ES_HOSTS)

    def semantic_split(self, sentence, word):
        for i in range(0, len(sentence)):
            if sentence[i] == word[0] and (i - 1 == -1 or sentence[i - 1] == " "):
                if sentence[i:][: len(word)] == word:
                    bottom_sentence = sentence[:i]
                    new_sentence = sentence[i + len(word) :]
                    if len(new_sentence) != 0:
                        if new_sentence[0] == " " or not new_sentence[0].isalpha():
                            return [bottom_sentence] + self.semantic_split(
                                new_sentence, word
                            )
                    else:
                        return [bottom_sentence] + [""]
        return [sentence]

    def semantic_contains(self, sentence, word):
        for i in range(0, len(sentence)):
            if sentence[i] == word[0] and (i - 1 == -1 or sentence[i - 1] == " "):
                if sentence[i:][: len(word)] == word:
                    front_sentence = sentence[i + len(word) :]
                    if len(front_sentence) != 0:
                        if front_sentence[0] == " " or not front_sentence[0].isalpha():
                            return True
                    else:
                        return True
        return False

    def get_data_from_index(self, index, query):
        limits = query.split(Concordance.SEPARATOR_CHARS[1])
        by_regex = True
        if len(limits) == 1:
            by_regex = False
        if by_regex:
            bottom_limit = limits[0]
            front_limit_and_regex = limits[1].split(Concordance.SEPARATOR_CHARS[2])
            front_limit = front_limit_and_regex[1]
            regex = front_limit_and_regex[0]
            tonkens_number_str = regex.split(Concordance.SEPARATOR_CHARS[0])[1]
            if len(tonkens_number_str) == 0:
                tonkens_number = -1
            else:
                tonkens_number = int(tonkens_number_str)
            query_result = self.elasticsearch.search(
                index=index,
                body={
                    "query": {
                        "dis_max": {
                            "queries": [
                                {
                                    "bool": {
                                        "must": [
                                            {
                                                "match_phrase": {
                                                    CorpusTable.EVENT_MESSAGE_COLUMN_NAME(): front_limit
                                                }
                                            },
                                        ],
                                        "should": [
                                            {
                                                "match_phrase_prefix": {
                                                    CorpusTable.EVENT_MESSAGE_COLUMN_NAME(): bottom_limit
                                                    + " "
                                                }
                                            },
                                            {
                                                "match_phrase_prefix": {
                                                    CorpusTable.EVENT_MESSAGE_COLUMN_NAME(): bottom_limit
                                                    + ","
                                                }
                                            },
                                            {
                                                "match_phrase_prefix": {
                                                    CorpusTable.EVENT_MESSAGE_COLUMN_NAME(): bottom_limit
                                                    + "."
                                                }
                                            },
                                            {
                                                "match_phrase_prefix": {
                                                    CorpusTable.EVENT_MESSAGE_COLUMN_NAME(): bottom_limit
                                                    + ":"
                                                }
                                            },
                                            {
                                                "match_phrase_prefix": {
                                                    CorpusTable.EVENT_MESSAGE_COLUMN_NAME(): bottom_limit
                                                    + ";"
                                                }
                                            },
                                            {
                                                "match_phrase_prefix": {
                                                    CorpusTable.EVENT_MESSAGE_COLUMN_NAME(): bottom_limit
                                                    + "?"
                                                }
                                            },
                                            {
                                                "match_phrase_prefix": {
                                                    CorpusTable.EVENT_MESSAGE_COLUMN_NAME(): bottom_limit
                                                    + "!"
                                                }
                                            },
                                            {
                                                "match_phrase_prefix": {
                                                    CorpusTable.EVENT_MESSAGE_COLUMN_NAME(): bottom_limit
                                                    + "\n"
                                                }
                                            },
                                        ],
                                    }
                                }
                            ]
                        }
                    },
                    "size": CONCORDANCE_QUERY_SIZE,
                },
            )
            results = []
            for i in query_result["hits"]["hits"]:
                remainders = self.semantic_split(
                    i["_source"][CorpusTable.EVENT_MESSAGE_COLUMN_NAME()].lower(),
                    bottom_limit.lower(),
                )
                for j in range(0, len(remainders)):
                    result = ""
                    if j + 1 == len(remainders):
                        break
                    else:
                        if remainders[j + 1] != "":
                            if not self.semantic_contains(
                                remainders[j + 1], front_limit.lower()
                            ):
                                pass
                            else:
                                middle_words_and_front_words = self.semantic_split(
                                    remainders[j + 1], front_limit.lower()
                                )
                                middle_words = middle_words_and_front_words[0]
                                if (
                                    len(middle_words.split(" ")) == tonkens_number + 2
                                    or tonkens_number == -1
                                ):
                                    words_behind = remainders[j].split(" ")
                                    words_front = middle_words_and_front_words[1].split(
                                        " "
                                    )
                                    bottom = (
                                        len(words_behind) - Concordance.NUMBER_OF_WORDS
                                    )
                                    if bottom < 0:
                                        bottom = 0
                                    bottom_text = " ".join(words_behind[bottom:])
                                    if len(bottom_text) < Concordance.NUMBER_OF_CHARS:
                                        bottom_text += "_" * (
                                            Concordance.NUMBER_OF_CHARS
                                            - len(bottom_text)
                                        )
                                    result = (
                                        bottom_text
                                        + " <b>"
                                        + bottom_limit.lower()
                                        + " "
                                        + middle_words
                                        + " "
                                        + front_limit
                                        + "</b> "
                                        + " ".join(
                                            words_front[: Concordance.NUMBER_OF_WORDS]
                                        )
                                    )

                    if result != "":
                        results.append(result)
            return results
        else:
            query_result = self.elasticsearch.search(
                index=index,
                body={
                    "query": {
                        "dis_max": {
                            "queries": [
                                {
                                    "match_phrase": {
                                        CorpusTable.EVENT_MESSAGE_COLUMN_NAME(): query
                                    }
                                }
                            ]
                        }
                    },
                    "size": CONCORDANCE_QUERY_SIZE,
                },
            )
            results = []
            for i in query_result["hits"]["hits"]:
                remainders = self.semantic_split(
                    i["_source"][CorpusTable.EVENT_MESSAGE_COLUMN_NAME()].lower(),
                    query.lower(),
                )
                for j in range(0, len(remainders)):
                    result = ""
                    if j + 1 == len(remainders) or remainders[j + 1] == "":
                        break
                    else:
                        if remainders[j + 1] != "":
                            words_behind = remainders[j].split(" ")
                            words_front = remainders[j + 1].split(" ")
                            bottom = len(words_behind) - Concordance.NUMBER_OF_WORDS
                            if bottom < 0:
                                bottom = 0
                            bottom_text = " ".join(words_behind[bottom:])
                            if len(bottom_text) < Concordance.NUMBER_OF_CHARS:
                                bottom_text += "_" * (
                                    Concordance.NUMBER_OF_CHARS - len(bottom_text)
                                )
                            result = (
                                bottom_text
                                + " <b>"
                                + query
                                + "</b> "
                                + " ".join(words_front[: Concordance.NUMBER_OF_WORDS])
                            )

                    if result != "":
                        results.append(result)
            return results
