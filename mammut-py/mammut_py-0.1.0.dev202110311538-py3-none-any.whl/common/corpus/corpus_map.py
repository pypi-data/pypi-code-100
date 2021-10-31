import itertools

import pandas as pd

from mammut.common.basic_tokenizer import BasicTokenizer
from mammut.common.corpus.synthetic_corpus import SyntheticCorpus
from mammut.common.corpus.images_corpus import ImagesCorpus
from mammut.common.corpus.crawler_corpus import CrawlerCorpus
from mammut.common.corpus.dictionary_corpus import DictionaryCorpus
from mammut.common.corpus.natural_corpus import NaturalCorpus
from mammut.common.corpus.issue_corpus import IssueCorpus
from mammut.common.corpus.mammut_corpus import MammutCorpus
from mammut.common.lexicon.dictionary import Dictionary
from mammut.common.lexicon.linguistic_standard import LinguisticStandard
from mammut.common.storage.storage_manager import StorageManager
from mammut.common.catalog.catalog_manager import Catalog
from typing import List
from mammut.common.corpus.hugging_face_corpus import *
import json as json_module


class CorpusMap:
    """The Corpus Map is a map of all the corpus
    that can be used to train a bot.

    # TODO: Document class methods.
    """

    DEFAULT_SHEET_TITTLE = "corpus_map"
    DEFAULT_START_COLUMN = "A"
    DEFAULT_START_ROW = "2"
    DEFAULT_END_RANGE = "N"
    DEFAULT_ID_KEY = "id"
    DEFAULT_MAIN_SHEET_KEY = "main_sheet"
    DEFAULT_EXTENSION_SHEET_KEY = "extension_sheet"
    DEFAULT_VARIABLES_SHEET_KEY = "variables_sheet"
    DEFAULT_TYPE_KEY = "corpus_type"
    DEFAULT_REGIONAL_SETTINGS_KEY = "regional_settings"
    DEFAULT_ANNOTABLE_KEY = "annotable"
    DEFAULT_ONTOLOGY_INSTANCES_KEY = "ontology_instances"
    DEFAULT_ONTOLOGY_DEFAULTS_KEY = "ontology_defaults"
    DEFAULT_ONTOLOGY_VERTICES_KEY = "ontology_vertices"
    DEFAULT_ONTOLOGY_EDGES_KEY = "ontology_edges"
    DEFAULT_ONTOLOGY_PROPERTIES_KEY = "ontology_properties"
    DEFAULT_CONFIGURATION_JSON_KEY = "configuration_json"
    DEFAULT_HIDDEN_KEY = "hidden"
    DEFAULT_MAMMUT_TYPE = "M"
    DEFAULT_CRAWLER_TYPE = "C"
    DEFAULT_NATURAL_TYPE = "N"
    DEFAULT_IMAGES_TYPE = "IM"
    DEFAULT_ISSUES_TYPE = "I"
    DEFAULT_DICTIONARY_TYPE = "D"
    DEFAULT_SYNTHETIC_TYPE = "S"
    DEFAULT_HUGGINGFACE_FIXED_TYPE = "HF_FIXED"
    DEFAULT_HUGGINGFACE_FIXED_TEST_TYPE = "HF_FIXED_TEST"
    DEFAULT_NONE_KEY = "None"
    storage_manager = StorageManager()

    def __init__(
        self,
        spreadsheet_id: str,
        tokenizer: BasicTokenizer,
        dictionary: Dictionary,
        standard: LinguisticStandard,
        catalog: Catalog,
        update_status_text_box=None,
    ):

        self.map = self.storage_manager.get_spreadsheet_as_dataframe(
            spreadsheet_id,
            CorpusMap.DEFAULT_SHEET_TITTLE,
            CorpusMap.DEFAULT_START_COLUMN,
            CorpusMap.DEFAULT_START_ROW,
            CorpusMap.DEFAULT_END_RANGE,
        )
        if CorpusMap.DEFAULT_HIDDEN_KEY in self.map:
            self.map = self.map.loc[
                (self.map[CorpusMap.DEFAULT_HIDDEN_KEY] == "")
            ]
        self.mammut_corpus_list = []
        self.crawler_corpus_list = []
        self.natural_corpus_list = []
        self.images_corpus_list = []
        self.dictionary_corpus_list = []
        self.issues_corpus_list = []
        self.synthetic_corpus_list = []
        self.hugging_face_corpus_list: List[HuggingFaceDatasetCorpus] = []
        self.hugging_face_corpus_test_list: List[HuggingFaceDatasetCorpus] = []
        self._corpus_table_by_id: Dict = {}
        self.spreadsheet_id = spreadsheet_id
        self.tokenizer = tokenizer
        self.dictionary = dictionary
        self.standard = standard
        self.catalog = catalog
        self.update_status_text_box = update_status_text_box
        self.switch_load = {
            CorpusMap.DEFAULT_MAMMUT_TYPE: self.create_mammut_corpus,
            CorpusMap.DEFAULT_CRAWLER_TYPE: self.create_crawler_corpus,
            CorpusMap.DEFAULT_NATURAL_TYPE: self.create_natural_corpus,
            CorpusMap.DEFAULT_IMAGES_TYPE: self.create_images_corpus,
            CorpusMap.DEFAULT_ISSUES_TYPE: self.create_issue_corpus,
            CorpusMap.DEFAULT_SYNTHETIC_TYPE: self.create_synthetic_corpus,
            CorpusMap.DEFAULT_HUGGINGFACE_FIXED_TYPE: self.create_hugging_face_fixed_corpus,
            CorpusMap.DEFAULT_HUGGINGFACE_FIXED_TEST_TYPE: self.create_hugging_face_fixed_corpus_test,
        }
        self.switch_get = {
            CorpusMap.DEFAULT_MAMMUT_TYPE: self.mammut_corpus_list,
            CorpusMap.DEFAULT_CRAWLER_TYPE: self.crawler_corpus_list,
            CorpusMap.DEFAULT_NATURAL_TYPE: self.natural_corpus_list,
            CorpusMap.DEFAULT_IMAGES_TYPE: self.images_corpus_list,
            CorpusMap.DEFAULT_DICTIONARY_TYPE: self.dictionary_corpus_list,
            CorpusMap.DEFAULT_ISSUES_TYPE: self.issues_corpus_list,
            CorpusMap.DEFAULT_SYNTHETIC_TYPE: self.synthetic_corpus_list,
            CorpusMap.DEFAULT_HUGGINGFACE_FIXED_TYPE: self.hugging_face_corpus_list,
            CorpusMap.DEFAULT_HUGGINGFACE_FIXED_TEST_TYPE: self.hugging_face_corpus_test_list,
        }
        self.load()
        self.load_dictionary_corpus()

    def _update_corpus_table_by_id(self, corpus_id: int, corpus_reference):
        """Adds the corpus to the corpus table with corpus ID keys.

        The ID of the corpus is being received because there's no a common
        generalization of corpus data attributes.

        Args:
            corpus_id: The corpus ID for the corpus_reference.
            corpus_reference: the corpus object reference to be stored as value
                in the table.
        """
        self._corpus_table_by_id[int(corpus_id)] = corpus_reference

    def load(self):
        i = 0
        for type in self.map[CorpusMap.DEFAULT_TYPE_KEY]:
            annotable = not (
                str.strip(self.map[CorpusMap.DEFAULT_ANNOTABLE_KEY][i]) == ""
            )
            self.switch_load[type](
                self.map[CorpusMap.DEFAULT_ID_KEY][i],
                self.map[CorpusMap.DEFAULT_MAIN_SHEET_KEY][i],
                self.map[CorpusMap.DEFAULT_EXTENSION_SHEET_KEY][i],
                self.map[CorpusMap.DEFAULT_VARIABLES_SHEET_KEY][i],
                self.map[CorpusMap.DEFAULT_REGIONAL_SETTINGS_KEY][i],
                self.map[CorpusMap.DEFAULT_CONFIGURATION_JSON_KEY][i],
                annotable,
                self.map[CorpusMap.DEFAULT_ONTOLOGY_INSTANCES_KEY][i],
                self.map[CorpusMap.DEFAULT_ONTOLOGY_DEFAULTS_KEY][i],
                self.map[CorpusMap.DEFAULT_ONTOLOGY_VERTICES_KEY][i],
                self.map[CorpusMap.DEFAULT_ONTOLOGY_EDGES_KEY][i],
                self.map[CorpusMap.DEFAULT_ONTOLOGY_PROPERTIES_KEY][i],
            )
            i += 1

    def load_dictionary_corpus(self):
        lemmas_entries_by_regional_settings_lemma = itertools.groupby(
            self.dictionary.lemmas_entries, lambda e: e.regional_settings_lemma
        )
        for (
            regional_settings_lemma,
            lemmas_entries,
        ) in lemmas_entries_by_regional_settings_lemma:
            (
                sheet_rows,
                hash_lemma_dict,
            ) = DictionaryCorpus.transform_dictinary_to_sheet_rows(
                self.dictionary
            )
            corpus_dataframe = pd.DataFrame(
                sheet_rows[1:], columns=sheet_rows[0]
            )
            corpus_dataframe["sub_id"] = corpus_dataframe["sub_id"].apply(str)
            corpus_dataframe["id"] = corpus_dataframe["id"].apply(str)
            corpus_id = 1
            for corpus_type in self.switch_get:
                corpus_id = corpus_id + len(self.switch_get[corpus_type])
            annotable = True
            self.dictionary_corpus_list.append(
                DictionaryCorpus(
                    self.spreadsheet_id,
                    corpus_id,
                    f"{DictionaryCorpus.DEFAULT_SHEET_NAME}-{regional_settings_lemma}",
                    "",
                    self.tokenizer,
                    self.dictionary,
                    regional_settings_lemma,
                    annotable,
                    hash_lemma_dict,
                    corpus_dataframe=corpus_dataframe,
                )
            )
            self._update_corpus_table_by_id(
                corpus_id, self.dictionary_corpus_list[-1]
            )

    def create_synthetic_corpus(
        self,
        id,
        main_sheet,
        extension_sheet,
        variables_sheet,
        language_settings,
        json,
        annotable,
        ontology_instances,
        ontology_defaults,
        ontology_vertices,
        ontology_edges,
        ontology_properties,
    ):
        self.synthetic_corpus_list.append(
            SyntheticCorpus(
                self.spreadsheet_id,
                id,
                self.dictionary,
                self.standard,
                language_settings,
                json,
            )
        )
        self._update_corpus_table_by_id(id, self.synthetic_corpus_list[-1])

    def create_hugging_face_fixed_corpus(
        self,
        id,
        main_sheet,
        extension_sheet,
        variables_sheet,
        language_settings,
        json,
        annotable,
        ontology_instances,
        ontology_defaults,
        ontology_vertices,
        ontology_edges,
        ontology_properties,
    ):
        json_parsed = json_module.loads(json)
        self.hugging_face_corpus_list.append(
            HuggingFaceFixedCorpus(self.spreadsheet_id, id, json_parsed,)
        )
        self._update_corpus_table_by_id(id, self.hugging_face_corpus_list[-1])

    def create_hugging_face_fixed_corpus_test(
        self,
        id,
        main_sheet,
        extension_sheet,
        variables_sheet,
        language_settings,
        json,
        annotable,
        ontology_instances,
        ontology_defaults,
        ontology_vertices,
        ontology_edges,
        ontology_properties,
    ):
        json_parsed = json_module.loads(json)
        self.hugging_face_corpus_list.append(
            HuggingFaceFixedCorpusTest(self.spreadsheet_id, id, json_parsed,)
        )
        self._update_corpus_table_by_id(id, self.hugging_face_corpus_list[-1])

    def create_mammut_corpus(
        self,
        id,
        main_sheet,
        extension_sheet,
        variables_sheet,
        language_settings,
        json,
        annotable,
        ontology_instances,
        ontology_defaults,
        ontology_vertices,
        ontology_edges,
        ontology_properties,
    ):
        if extension_sheet == CorpusMap.DEFAULT_NONE_KEY:
            extension_sheet = ""

        # TODO: Implementar la carga del nuevo Knowledge
        self.mammut_corpus_list.append(
            MammutCorpus(
                self.spreadsheet_id,
                id,
                main_sheet,
                extension_sheet,
                variables_sheet,
                self.tokenizer,
                self.dictionary,
                language_settings,
                annotable,
            )
        )
        self._update_corpus_table_by_id(id, self.mammut_corpus_list[-1])

    def create_crawler_corpus(
        self,
        id,
        main_sheet,
        extension_sheet,
        variables_sheet,
        language_settings,
        json,
        annotable,
        ontology_instances,
        ontology_defaults,
        ontology_vertices,
        ontology_edges,
        ontology_properties,
    ):
        if extension_sheet == CorpusMap.DEFAULT_NONE_KEY:
            extension_sheet = ""

        self.crawler_corpus_list.append(
            CrawlerCorpus(
                self.spreadsheet_id,
                id,
                main_sheet,
                extension_sheet,
                self.tokenizer,
                self.dictionary,
                language_settings,
                json,
                self.update_status_text_box,
                annotable,
            )
        )

        self._update_corpus_table_by_id(id, self.crawler_corpus_list[-1])

    def create_natural_corpus(
        self,
        id,
        main_sheet,
        extension_sheet,
        variables_sheet,
        language_settings,
        json,
        annotable,
        ontology_instances,
        ontology_defaults,
        ontology_vertices,
        ontology_edges,
        ontology_properties,
    ):
        if extension_sheet == CorpusMap.DEFAULT_NONE_KEY:
            extension_sheet = ""

        self.natural_corpus_list.append(
            NaturalCorpus(
                self.spreadsheet_id,
                id,
                main_sheet,
                extension_sheet,
                self.tokenizer,
                self.dictionary,
                language_settings,
                annotable,
            )
        )

        self._update_corpus_table_by_id(id, self.natural_corpus_list[-1])

    def create_images_corpus(
        self,
        id,
        main_sheet,
        extension_sheet,
        variables_sheet,
        language_settings,
        json,
        annotable,
        ontology_instances,
        ontology_defaults,
        ontology_vertices,
        ontology_edges,
        ontology_properties,
    ):
        if extension_sheet == CorpusMap.DEFAULT_NONE_KEY:
            extension_sheet = ""

        self.images_corpus_list.append(
            ImagesCorpus(
                self.spreadsheet_id,
                id,
                main_sheet,
                extension_sheet,
                self.tokenizer,
                self.dictionary,
                language_settings,
                self.update_status_text_box,
                annotable,
                json,
            )
        )

        self._update_corpus_table_by_id(id, self.images_corpus_list[-1])

    def create_issue_corpus(
        self,
        id,
        main_sheet,
        extension_sheet,
        variables_sheet,
        language_settings,
        json,
        annotable,
        ontology_instances,
        ontology_defaults,
        ontology_vertices,
        ontology_edges,
        ontology_properties,
    ):
        if extension_sheet == CorpusMap.DEFAULT_NONE_KEY:
            extension_sheet = ""
        knowledge = None
        self.issues_corpus_list.append(
            IssueCorpus(
                self.spreadsheet_id,
                id,
                main_sheet,
                extension_sheet,
                variables_sheet,
                self.tokenizer,
                self.dictionary,
                language_settings,
                annotable,
            )
        )

        self._update_corpus_table_by_id(id, self.issues_corpus_list[-1])

    def get_corpus(self, type, sheet_tittle):
        corpus_list = self.switch_get[type]
        for corpus in corpus_list:
            if corpus.sheet_title == sheet_tittle:
                return corpus
        raise NameError()

    def get_corpus_by_type(self, corpus_type, sheet_tittle):
        corpus_list = []
        for i in self.switch_get:
            if len(self.switch_get[i]) > 0:
                if type(self.switch_get[i][0]) == corpus_type:
                    corpus_list = self.switch_get[i]
        for corpus in corpus_list:
            if corpus.sheet_title == sheet_tittle:
                return corpus

    def get_all_corpus(self):
        return (
            self.mammut_corpus_list
            + self.natural_corpus_list
            + self.crawler_corpus_list
            + self.images_corpus_list
            + self.dictionary_corpus_list
            + self.issues_corpus_list
            + self.synthetic_corpus_list
            + self.hugging_face_corpus_list
        )

    def get_corpus_by_id(self, corpus_id: int):
        """Returns a corpus stored in the corpus map by id.

        Raises:
            KeyError if the corpus_id key isn't found in the corpus table

        Return:
            The corpus reference object.
        """
        return self._corpus_table_by_id[corpus_id]
