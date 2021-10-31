from enum import Enum


class ElasticsearchParams(Enum):
    """
    Enum with the list of constant required to interact with Elasticsearch.
    """

    RESULT_RESPONSE_KEY = "result"
    FOUND_RESPONSE_KEY = "found"
    SOURCE_RESPONSE_KEY = "_source"

    def __repr__(self):
        return str(self.value)

    def __call__(self, *args, **kwargs):
        return str(self.value)


class DictionaryTable(Enum):
    """
    Enum with the list of constant required by the Dictionary table.
    """

    LEMMA_COLUMN_NAME = "lemma"
    WORD_TYPE_COLUMN_NAME = "word_type"
    REGIONAL_SETTINGS_LEMMA_COLUMN_NAME = "regional_settings_lemma"
    AFI_COLUMN_NAME = "AFI"
    POS_PARADIGM_COLUMN_NAME = "pos_paradigm"
    MORPH_PARADIGM_COLUMN_NAME = "morph_paradigm"
    MISS_PARADIGM_COLUMN_NAME = "miss_paradigm"
    FET_PARADIGM_COLUMN_NAME = "fet_paradigm"
    DEFINITION_INDEX_COLUMN_NAME = "definition_index"
    FEATURES_COLUMN_NAME = "features"
    SOURCE_COLUMN_NAME = "source"
    TOPIC_COLUMN_NAME = "topic"
    DEFINITION_COLUMN_NAME = "definition"
    REGIONAL_SETTINGS_DEFINITION_COLUMN_NAME = "regional_settings_definition"
    DATE_COLUMN_NAME = "date"
    TIMESTAMP_COLUMN_NAME = "timestamp"
    SENSE_LEMMA_COLUMN_NAME = "sense_lemma"
    SYNONYM_WORDS_COLUMN_NAME = "synonym_words"

    def __repr__(self):
        return str(self.value)

    def __call__(self, *args, **kwargs):
        return str(self.value)


