from mammut import BASE_MODEL_VISON_DIR
from mammut.common.basic_tokenizer import BasicTokenizer
from mammut.common.corpus.constants import CorpusTable
from mammut.common.corpus.corpus_base import Corpus, CorpusScenarioEntry
from mammut.common.corpus.crawler_corpus import CrawlerCorpus
from mammut.common.google_api import GoogleStorageDrive
from mammut.common.lexicon.dictionary import Dictionary
from mammut.common.storage.storage_manager import StorageManager


class ImagesCorpus(Corpus):
    DEFAULT_SHEET_TITTLE = "images_corpus"
    DEFAULT_BEGIN_RANGE = "A2"
    DEFAULT_IMAGE_ID = 1

    DEFAULT_SCENARIO_TYPE_VALUE = "Monologue"
    DEFAULT_EVENT_MESSAGE_ORIGINAL_VALUE = ""
    DEFAULT_EVENT_MESSAGE_VALUE = '[variable_image|"%s"]'
    DEFAULT_HIDDEN_VALUE = ""
    DEFAULT_FIELD_VALUE = ""
    DEFAULT_SOURCE_VALUE = "Mammut"
    DEFAULT_COMPLEXITY_VALUE = ""
    storage_manager = StorageManager()
    # configurations keys
    FOLDER_ID = "folder_id"  # del drive
    DESTINATION_DIRECTORY = "destination_directory"

    def __init__(
        self,
        spreadsheet_id: str,
        id,
        corpus_sheet_title: str,
        corpus_extension_sheet_title: str,
        tokenizer: BasicTokenizer,
        dictionary: Dictionary,
        regional_settings: str,
        update_status_text_box,
        annotable: bool,
        configuration_json,
    ):
        self.sheet_title = corpus_sheet_title
        self.spreadsheet_id = spreadsheet_id
        self.destination_folder = (
            BASE_MODEL_VISON_DIR + "/train/vision/" + spreadsheet_id + "/"
        )
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
            configuration_json,
        )

    def create_dump_sheet(self, spreadsheet_id):
        temporal_sheet_title = self.storage_manager.create_temporal_new_sheet(
            spreadsheet_id, self.sheet_title
        )
        self.storage_manager.add_rows_to_spreadsheet(
            spreadsheet_id,
            temporal_sheet_title,
            CrawlerCorpus.DEFAULT_COLUMN_TITTLES,
            CrawlerCorpus.DEFAULT_START_ROW_TITTLE,
            CrawlerCorpus.DEFAULT_START_COLUMN_TITTLE,
        )
        return temporal_sheet_title

    def get_images_data(self):
        folders_tuple = GoogleStorageDrive.get_folders_in_folder(
            self.configuration[ImagesCorpus.FOLDER_ID]
        )
        all_images = list()
        for folder in folders_tuple:
            all_images += self.download_images(folder[0], folder[1])
        return all_images

    def download_images(self, folder_name, folder_id):
        images = GoogleStorageDrive.get_all_files_in_folder(folder_id)
        images_titles = [i[0] for i in images]
        GoogleStorageDrive.download_files(
            folder_id,
            self.destination_folder + "/" + folder_name,
            images_titles,
        )
        return images_titles

    def dump_corpus(self, images):
        data = []
        for index, image in enumerate(images):
            image_name = ".".join(image.split(".")[:-1])
            data.append(
                [
                    ImagesCorpus.DEFAULT_IMAGE_ID,
                    index,
                    ImagesCorpus.DEFAULT_SCENARIO_TYPE_VALUE,
                    ImagesCorpus.DEFAULT_EVENT_MESSAGE_ORIGINAL_VALUE,
                    ImagesCorpus.DEFAULT_EVENT_MESSAGE_VALUE % image_name,
                    ImagesCorpus.DEFAULT_HIDDEN_VALUE,
                    ImagesCorpus.DEFAULT_FIELD_VALUE,
                    ImagesCorpus.DEFAULT_SOURCE_VALUE,
                    self.regional_settings,
                    ImagesCorpus.DEFAULT_COMPLEXITY_VALUE,
                ]
            )
        self.write_data(self.DEFAULT_CORPUS_RANGE, data)

    def write_data(self, range, rows):
        sheet_name, range_cell = range.split("!")
        self.storage_manager.add_rows_to_spreadsheet(
            self.spreadsheet_id,
            sheet_name,
            rows,
            range_cell[1 : len(range_cell)],
            range_cell[0],
        )

    def load_data(self):
        images_titles = self.get_images_data()
        # TODO:el nombre que se guarda en el coprus del exel debe contenr el nombre del folder donde se guarda?
        self.dump_corpus(images_titles)

    def retrain_model(self):
        return

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
