import hashlib

from mammut.common.basic_tokenizer import BasicTokenizer
from mammut.common.corpus.constants import CorpusTable
from mammut.common.corpus.corpus_base import ScenarioType
from mammut.common.corpus.natural_corpus import NaturalCorpus
from mammut.common.lexicon.dictionary import Dictionary


class DictionaryCorpus(NaturalCorpus):
    DEFAULT_SHEET_NAME = "dictionary_corpus"

    def __init__(
        self,
        spreadsheet_id: str,
        id,
        corpus_sheet_title: str,
        corpus_extension_sheet_title: str,
        tokenizer: BasicTokenizer,
        dictionary: Dictionary,
        regional_settings: str,
        annotable: bool,
        hash_lemma_dict: dict,
        corpus_dataframe,
    ):
        NaturalCorpus.__init__(
            self,
            spreadsheet_id,
            id,
            corpus_sheet_title,
            corpus_extension_sheet_title,
            tokenizer,
            dictionary,
            regional_settings,
            annotable,
            corpus_dataframe,
        )
        self.hash_lemma_dict = hash_lemma_dict

    @staticmethod
    def lemma_entry_to_events_rows(hashed_lemma, lemma_entry):
        events_list = list()
        for pos in lemma_entry.postags_entries:
            for definition_set in pos.definitions_set_entries:
                for definition_entry in definition_set.definitions_entries:
                    event_message = list()
                    event_message.append(hashed_lemma)  # id
                    event_message.append(
                        definition_set.definition_index
                    )  # sub_id
                    event_message.append(
                        ScenarioType.Monologue.value
                    )  # scenario_type
                    event_message.append(
                        definition_entry.definition
                    )  # event_message
                    event_message.append("")  # hidden
                    event_message.append("")  # field
                    event_message.append("dictionary")  # source
                    event_message.append(
                        definition_entry.regional_settings_definition
                    )  # regional seting
                    event_message.append("")  # complexity
                    events_list.append(event_message)
        return events_list

    @classmethod
    def transform_dictinary_to_sheet_rows(cls, dictionary):
        df_columuns = [
            CorpusTable.ID_COLUMN_NAME(),
            CorpusTable.SUB_ID_COLUMN_NAME(),
            CorpusTable.SCENARIO_TYPE_COLUMN_NAME(),
            CorpusTable.EVENT_MESSAGE_COLUMN_NAME(),
            CorpusTable.HIDDEN_COLUMN_NAME(),
            CorpusTable.FIELD_COLUMN_NAME(),
            CorpusTable.SOURCE_COLUMN_NAME(),
            CorpusTable.REGIONAL_SETTINGS_COLUMN_NAME(),
            CorpusTable.COMPLEXITY_COLUMN_NAME(),
        ]
        hash_lemma_dict = dict()
        sheet_rows = list()
        sheet_rows.append(df_columuns)
        for scenario_index, lemma_entry in enumerate(
            dictionary.lemmas_entries
        ):
            hashed_lemma = int(
                hashlib.sha256(lemma_entry.lemma.encode("utf-8")).hexdigest(),
                16,
            ) % (10 ** 8)
            hash_lemma_dict[hashed_lemma] = lemma_entry.lemma
            lemma_rows = cls.lemma_entry_to_events_rows(
                hashed_lemma, lemma_entry
            )
            sheet_rows = sheet_rows + lemma_rows
        return sheet_rows, hash_lemma_dict
