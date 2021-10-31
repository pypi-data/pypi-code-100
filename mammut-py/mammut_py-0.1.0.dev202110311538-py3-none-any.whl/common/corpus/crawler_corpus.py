from mammut.common.basic_tokenizer import BasicTokenizer
from mammut.common.corpus.constants import CorpusTable, CrawlerCorpusTable
from mammut.common.corpus.corpus_base import Corpus, CorpusScenarioEntry
from mammut.common.lexicon.dictionary import Dictionary
from mammut.common.storage.storage_manager import StorageManager
from mammut.data.mammut_crawler import CrawlingProperties, MammutCrawler


class CrawlerCorpus(Corpus):
    storage_manager = StorageManager()

    def __init__(
            self,
            spreadsheet_id: str,
            id,
            corpus_sheet_title: str,
            corpus_extension_sheet_title: str,
            tokenizer: BasicTokenizer,
            dictionary: Dictionary,
            regional_settings: str,
            json_parameters,
            update_status_text_box,
            annotable: bool,
    ):
        self.sheet_title = corpus_sheet_title
        self.spreadsheet_id = spreadsheet_id
        self.update_status_text_box = update_status_text_box
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
            json_parameters,
        )
        self.corpus_sheet_title = corpus_sheet_title

    def create_dump_sheet(self, spreadsheet_id):
        temporal_sheet_title = self.storage_manager.create_temporal_new_sheet(
            spreadsheet_id, self.sheet_title
        )
        self.storage_manager.add_rows_to_spreadsheet(
            spreadsheet_id,
            temporal_sheet_title,
            CrawlerCorpusTable.DEFAULT_COLUMN_TITTLES,
            CrawlerCorpusTable.DEFAULT_START_ROW_TITTLE,
            CrawlerCorpusTable.DEFAULT_START_COLUMN_TITTLE,
        )
        return temporal_sheet_title

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

    def load_data(self):
        data = []
        i = 0
        crawling_properties = CrawlingProperties(
            self.configuration[CrawlerCorpusTable.URL_KEY],
            self.configuration[CrawlerCorpusTable.NODES_PATTERN_KEY],
            self.configuration[CrawlerCorpusTable.NODE_ELEMENT_KEY],
            self.configuration[CrawlerCorpusTable.PAGE_HREF_KEY],
            pagination_nodes_pattern=self.configuration[
                CrawlerCorpusTable.PAGINATION_NODE_PATTERN_KEY
            ],
            pagination_element_xpath=self.configuration[
                CrawlerCorpusTable.PAGINATION_NODE_ELEMENT_KEY
            ],
            pages_limit=self.configuration[
                CrawlerCorpusTable.DEFAULT_PAGES_LIMIT_KEY
            ],
        )
        crawling_data = MammutCrawler(
            crawling_properties,
            update_status_text_box=self.update_status_text_box,
        ).execute()
        for dict in crawling_data:
            i += 1
            data.append(
                [
                    i,
                    i,
                    CrawlerCorpusTable.DEFAULT_SCENARIO_TYPE_VALUE,
                    dict["element"],
                    CrawlerCorpusTable.DEFAULT_EVENT_MESSAGE_VALUE,
                    CrawlerCorpusTable.DEFAULT_HIDDEN_VALUE,
                    CrawlerCorpusTable.DEFAULT_FIELD_VALUE,
                    CrawlerCorpusTable.DEFAULT_SOURCE_VALUE,
                    self.regional_settings,
                    CrawlerCorpusTable.DEFAULT_COMPLEXITY_VALUE,
                ]
            )
        self.write_data(self.DEFAULT_CORPUS_RANGE, data)

    def write_data(self, range, rows):
        sheet_name, range_cell = range.split("!")
        self.storage_manager.add_rows_to_spreadsheet(
            self.spreadsheet_id,
            sheet_name,
            rows,
            range_cell[1: len(range_cell)],
            range_cell[0],
        )
