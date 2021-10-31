from mammut.common.lexicon.functional import FunctionalLemmaDescriptor


class NonFunctionalLemmaDescriptor:
    LEMMA_COLUMN_NAME = "lemma"
    HIDE_COLUMN_NAME = "hide"
    REGIONAL_SETTINGS_LEMMA_COLUMN_NAME = "regional-settings-lemma"
    POS_PARADIGM_COLUMN_NAME = "pos-paradigm"
    DEFAULT_START_CELL = "A1"
    DEFAULT_END_CELL = "AF"

    def __init__(self, dataframe_row, standard):
        self.lemma = dataframe_row[FunctionalLemmaDescriptor.LEMMA_COLUMN_NAME].lower()
        self.regional_settings_lemma = dataframe_row[
            FunctionalLemmaDescriptor.REGIONAL_SETTINGS_LEMMA_COLUMN_NAME
        ]
        self.pos_paradigm = dataframe_row[
            FunctionalLemmaDescriptor.POS_PARADIGM_COLUMN_NAME
        ]
