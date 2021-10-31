from mammut.common.basic_tokenizer import BasicTokenizer
from mammut.common.corpus.constants import CorpusTable
from mammut.common.corpus.corpus_base import Corpus, CorpusScenarioEntry
from mammut.common.lexicon.dictionary import Dictionary


class NaturalCorpus(Corpus):
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
        corpus_dataframe=None,
    ):
        Corpus.__init__(
            self,
            spreadsheet_id,
            id,
            corpus_sheet_title,
            corpus_extension_sheet_title,
            tokenizer,
            dictionary,
            regional_settings,
            annotable,
            corpus_dataframe=corpus_dataframe,
        )

    def get_corpus_scenario_entry_from_row(self, g):
        return CorpusScenarioEntry(
            g[0],
            g[1].iloc[0][CorpusTable.SCENARIO_TYPE_COLUMN_NAME()],
            g[1],
            self.tokenizer,
            self.dictionary,
            self.regional_settings,
            self,
        )
