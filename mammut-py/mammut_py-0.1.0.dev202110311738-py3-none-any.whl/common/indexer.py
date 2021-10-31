# coding=utf-8
from typing import Union, Any, Dict, Optional

from elasticsearch import Elasticsearch, TransportError
import logging
import pandas as pd

from mammut import CONCORDANCE_QUERY_SIZE, ES_HOSTS
from mammut.common import (
    FEATURES_CONFIGURATIONS,
    index_definition_timeout,
    index_lemma_timeout,
    index_creation_timeout,
    global_request_timeout,
)
import os
import elasticsearch.helpers
import hashlib

from mammut.common.constants import DictionaryTable, ElasticsearchParams
from mammut.common.corpus.constants import CorpusTable

log = logging.getLogger(__name__)


class IndexInventory:
    INDEX_NAME = "datasets_inventory"
    INDEX_COLUMN = "index"
    DATASET_COLUMN = "dataset"
    HASH_COLUMN = "hash"

    def __init__(self):
        self.elasticsearch = Elasticsearch(ES_HOSTS)
        self._index_exist = False

    def _create_index_if_no_exist(self):
        if not self._index_exist:
            exist = self.elasticsearch.indices.exists(IndexInventory.INDEX_NAME)
            if not exist:
                self.elasticsearch.indices.create(IndexInventory.INDEX_NAME)
            self._index_exist = True

    def id_generator(self, index: str, dataset_name: str):
        return f"{index}_{dataset_name}"

    def set_index_data(
        self, index: str, dataset_name: str, data: Union[pd.DataFrame, Dict[str, Any]]
    ) -> Union[bool, int, str]:
        self._create_index_if_no_exist()
        data_hash = self.get_data_hash(data)
        response = self.elasticsearch.index(
            index=IndexInventory.INDEX_NAME,
            doc_type="doc",
            body={
                IndexInventory.INDEX_COLUMN: index,
                IndexInventory.DATASET_COLUMN: dataset_name,
                IndexInventory.HASH_COLUMN: data_hash,
            },
            id=self.id_generator(index, dataset_name,),
        )
        return response[ElasticsearchParams.RESULT_RESPONSE_KEY()]

    def get_data_hash(self, data):
        data_hash = None
        if isinstance(data, pd.DataFrame):
            data_hash = pd.util.hash_pandas_object(data)
            data_hash = hash(frozenset(data_hash.tolist()))
        elif isinstance(data, dict):
            data_hash = hash(frozenset(data.items()))
        else:
            data_hash = hash(data)
        return data_hash

    def get_index_data(self, index: str, dataset_name: str) -> Optional[str]:
        self._create_index_if_no_exist()
        data_hash = None
        exist = self.elasticsearch.exists(
            index=IndexInventory.INDEX_NAME,
            doc_type="doc",
            id=self.id_generator(index, dataset_name,),
        )
        if exist:
            response = self.elasticsearch.get(
                index=IndexInventory.INDEX_NAME,
                doc_type="doc",
                id=self.id_generator(index, dataset_name,),
            )
            if (
                response[ElasticsearchParams.FOUND_RESPONSE_KEY()]
                and ElasticsearchParams.SOURCE_RESPONSE_KEY() in response
                and IndexInventory.HASH_COLUMN
                in response[ElasticsearchParams.SOURCE_RESPONSE_KEY()]
            ):
                data_hash = response[ElasticsearchParams.SOURCE_RESPONSE_KEY()][
                    IndexInventory.HASH_COLUMN
                ]
        return data_hash

    def have_to_index_data(
        self, index: str, dataset_name: str, data: Union[pd.DataFrame, Dict[str, Any]]
    ) -> bool:
        expected_data_hash = self.get_data_hash(data)
        stored_data_hash = self.get_index_data(index, dataset_name)
        if stored_data_hash is not None and stored_data_hash == expected_data_hash:
            return False
        else:
            return True


CurrentIndexInventory = IndexInventory()


class CorpusIndexer:

    DEFAULT_COLUMN_TITTLES = [
        CorpusTable.ID_COLUMN_NAME(),
        CorpusTable.SUB_ID_COLUMN_NAME(),
        CorpusTable.SCENARIO_TYPE_COLUMN_NAME(),
        CorpusTable.EVENT_MESSAGE_COLUMN_NAME(),
        CorpusTable.HIDDEN_COLUMN_NAME(),
        CorpusTable.FIELD_COLUMN_NAME(),
        CorpusTable.LAMBDA_CONDITION_COLUMN_NAME(),
        CorpusTable.UI_EVENT_COLUMN_NAME(),
        CorpusTable.ACTION_COLUMN_NAME(),
        CorpusTable.SOURCE_COLUMN_NAME(),
        CorpusTable.REGIONAL_SETTINGS_COLUMN_NAME(),
        CorpusTable.COMPLEXITY_COLUMN_NAME(),
    ]

    def __init__(self):
        self.elasticsearch = Elasticsearch(ES_HOSTS)

    def id_generator(
        self, spreadsheet_id, corpus_name, event_scenario_id, event_sub_id
    ):
        return spreadsheet_id + corpus_name + event_scenario_id + event_sub_id

    def index_event(self, index, spreadsheet_id, corpus_name, event):
        response = self.elasticsearch.index(
            index=index,
            doc_type="doc",
            body=event,
            id=self.id_generator(
                spreadsheet_id,
                corpus_name,
                event[CorpusTable.ID_COLUMN_NAME()],
                event[CorpusTable.SUB_ID_COLUMN_NAME()],
            ),
        )
        return response[ElasticsearchParams.RESULT_RESPONSE_KEY()]

    def delete_event(self, index, event_id):
        response = self.elasticsearch.delete(index=index, doc_type="doc", id=event_id)
        return response[ElasticsearchParams.FOUND_RESPONSE_KEY()]

    def delete_index(self, index):
        self.elasticsearch.indices.delete(index=index, ignore=[400, 404])

    def index_corpus(self, corpus_data_frame, spreadsheet_id, corpus_name, index):
        dataset_name = f"{spreadsheet_id}-{corpus_name}"
        have_to_index = CurrentIndexInventory.have_to_index_data(
            index, dataset_name, corpus_data_frame
        )
        if have_to_index:
            events = []
            for i in range(0, len(corpus_data_frame.index)):
                event = {}
                for column in CorpusIndexer.DEFAULT_COLUMN_TITTLES:
                    if corpus_data_frame.__contains__(column):
                        event[column] = corpus_data_frame[column][i]
                    else:
                        event[column] = ""
                event["corpus-name"] = corpus_name
                events.append(event)
            for event in events:
                self.index_event(index, spreadsheet_id, corpus_name, event)
            CurrentIndexInventory.set_index_data(index, dataset_name, corpus_data_frame)


class NGramIndexer:
    DEFAULT_REGIONAL_SETTINGS_KEY = "regional_settings"

    DEFAULT_PROVE_DATA_LOCATION_KEY = "prove_data_location"
    DEFAULT_DATA_LOCATION_KEY = "data_location"
    DEFAULT_DEFAULTNGRAM_KEY = "DEFAULT_NGRAM"
    DEFAULT_USERNGRAM_KEY = "USER_NGRAM"

    DEFAULT_COLUMN_TITTLES = ["ngram", "year", "match_count", "volume_count"]

    def __init__(self):
        self.elasticsearch = Elasticsearch(ES_HOSTS)

    def id_generator(self, ngram, year, path):
        return hashlib.md5((path + ngram + year).encode()).hexdigest()

    def index_ngram(self, index, year, ngram, path, ngram_doc):
        response = self.elasticsearch.index(
            index=index,
            doc_type="doc",
            body=ngram_doc,
            id=self.id_generator(ngram, year, path),
        )

        return response[ElasticsearchParams.RESULT_RESPONSE_KEY()]

    def delete_ngram(self, index, ngram_id):
        response = self.elasticsearch.delete(index=index, doc_type="doc", id=ngram_id)
        return response[ElasticsearchParams.FOUND_RESPONSE_KEY()]

    def delete_index(self, index):
        self.elasticsearch.indices.delete(index=index, ignore=[400, 404])

    def load_file(self, path, regional_settings):
        file = open(path)
        ngram_file = {}
        for line in file.readlines():
            ngram_elem = line.split("\t")
            ngram_file[self.id_generator(ngram_elem[0], ngram_elem[1], path)] = {
                NGramIndexer.DEFAULT_COLUMN_TITTLES[0]: ngram_elem[0],
                NGramIndexer.DEFAULT_COLUMN_TITTLES[1]: int(ngram_elem[1]),
                NGramIndexer.DEFAULT_COLUMN_TITTLES[2]: int(ngram_elem[2]),
                NGramIndexer.DEFAULT_COLUMN_TITTLES[3]: int(
                    ngram_elem[3].split("\n")[0]
                ),
                NGramIndexer.DEFAULT_REGIONAL_SETTINGS_KEY: regional_settings,
            }
        return ngram_file

    def index_ngram_file(self, file, index, prove_data=False):
        path = ""
        regional_settings = file.split("-")[1]
        DATA_LOCATION_KEY = ""

        if prove_data:
            DATA_LOCATION_KEY = NGramIndexer.DEFAULT_PROVE_DATA_LOCATION_KEY
        else:
            DATA_LOCATION_KEY = NGramIndexer.DEFAULT_DATA_LOCATION_KEY

        if (
            os.system(
                "cd "
                + os.path.join(
                    os.path.expanduser("~"),
                    FEATURES_CONFIGURATIONS[NGramIndexer.DEFAULT_DEFAULTNGRAM_KEY][
                        DATA_LOCATION_KEY
                    ],
                )
            )
            == 0
        ):
            os.chdir(os.path.expanduser("~"))
            path = (
                "./"
                + FEATURES_CONFIGURATIONS[NGramIndexer.DEFAULT_DEFAULTNGRAM_KEY][
                    DATA_LOCATION_KEY
                ]
                + "/"
                + file
            )
        else:
            os.chdir(os.path.expanduser("~"))
            path = (
                "./"
                + FEATURES_CONFIGURATIONS[NGramIndexer.DEFAULT_USERNGRAM_KEY][
                    DATA_LOCATION_KEY
                ]
                + "/"
                + file
            )

        ngram_file = self.load_file(path, regional_settings)
        dataset_name = f"ngram-{file}"
        have_to_index = CurrentIndexInventory.have_to_index_data(
            index, dataset_name, ngram_file
        )
        if have_to_index:
            for ngram in ngram_file.values():
                self.index_ngram(
                    index,
                    str(ngram[NGramIndexer.DEFAULT_COLUMN_TITTLES[1]]),
                    ngram[NGramIndexer.DEFAULT_COLUMN_TITTLES[0]],
                    path,
                    ngram,
                )
            CurrentIndexInventory.set_index_data(index, dataset_name, ngram_file)

    def file_generator(self, file, index, prove_data=False):
        path = ""
        regional_settings = file.split("-")[1]

        DATA_LOCATION_KEY = ""

        if prove_data:
            DATA_LOCATION_KEY = NGramIndexer.DEFAULT_PROVE_DATA_LOCATION_KEY
        else:
            DATA_LOCATION_KEY = NGramIndexer.DEFAULT_DATA_LOCATION_KEY
        user_path = os.path.expanduser("~")
        folder_path = os.path.join(
            user_path,
            FEATURES_CONFIGURATIONS[NGramIndexer.DEFAULT_DEFAULTNGRAM_KEY][
                DATA_LOCATION_KEY
            ],
        )
        if not os.path.exists(folder_path):
            folder_path = os.path.join(
                user_path,
                FEATURES_CONFIGURATIONS[NGramIndexer.DEFAULT_USERNGRAM_KEY][
                    DATA_LOCATION_KEY
                ],
            )
        path = folder_path + "/" + file
        file = open(path)
        line = None

        while True:
            line = file.readline()
            if not line:
                break
            ngram_elem = line.split("\t")
            ngram_doc = {
                "_op_type": "index",
                "_index": index,
                "_type": "doc",
                "_id": self.id_generator(ngram_elem[0], ngram_elem[1], path),
                "_source": {
                    NGramIndexer.DEFAULT_COLUMN_TITTLES[0]: ngram_elem[0],
                    NGramIndexer.DEFAULT_COLUMN_TITTLES[1]: int(ngram_elem[1]),
                    NGramIndexer.DEFAULT_COLUMN_TITTLES[2]: int(ngram_elem[2]),
                    NGramIndexer.DEFAULT_COLUMN_TITTLES[3]: int(
                        ngram_elem[3].split("\n")[0]
                    ),
                    NGramIndexer.DEFAULT_REGIONAL_SETTINGS_KEY: regional_settings,
                },
            }

            yield ngram_doc

    def index_ngram_file_bulk(self, file, index, prove_data=False):
        itor = self.file_generator(file, index, prove_data=prove_data)
        return elasticsearch.helpers.bulk(self.elasticsearch, itor)

    def index_ngram_file_parallel_bulk(self, file, index, prove_data=False):
        itor = self.file_generator(file, index, prove_data=prove_data)
        p_itor = elasticsearch.helpers.parallel_bulk(self.elasticsearch, itor)
        for response in p_itor:
            pass


class DefinitionIndexer:
    CORPUS_NAME = "definitions"

    def __init__(self, package_name):
        self.package_name = package_name
        self.definition_index_name = (
            self.package_name + "-" + DefinitionIndexer.CORPUS_NAME
        )
        self.elasticsearch = Elasticsearch(
            ES_HOSTS, request_timeout=global_request_timeout
        )
        if not self.elasticsearch.indices.exists(self.package_name):
            self.elasticsearch.indices.create(
                self.package_name,
                request_timeout=global_request_timeout,
                timeout=index_creation_timeout,
            )
        if not self.elasticsearch.indices.exists(self.definition_index_name):
            self.elasticsearch.indices.create(
                self.definition_index_name,
                request_timeout=global_request_timeout,
                timeout=index_creation_timeout,
            )

    def _index_definition(self, definition, morpheme):
        doc_id = (
            morpheme
            + "-"
            + definition[0]
            + "-"
            + definition[4]
            + "-"
            + str(definition[8])
        )
        self.elasticsearch.index(
            index=self.definition_index_name,
            doc_type="doc",
            body={
                DictionaryTable.LEMMA_COLUMN_NAME(): definition[0],
                DictionaryTable.WORD_TYPE_COLUMN_NAME(): definition[1],
                DictionaryTable.REGIONAL_SETTINGS_LEMMA_COLUMN_NAME(): definition[2],
                DictionaryTable.AFI_COLUMN_NAME(): definition[3],
                DictionaryTable.POS_PARADIGM_COLUMN_NAME(): definition[4],
                DictionaryTable.MORPH_PARADIGM_COLUMN_NAME(): definition[5],
                DictionaryTable.MISS_PARADIGM_COLUMN_NAME(): definition[6],
                DictionaryTable.FET_PARADIGM_COLUMN_NAME(): definition[7],
                DictionaryTable.DEFINITION_INDEX_COLUMN_NAME(): definition[8],
                DictionaryTable.FEATURES_COLUMN_NAME(): definition[9],
                DictionaryTable.SOURCE_COLUMN_NAME(): definition[10],
                DictionaryTable.TOPIC_COLUMN_NAME(): definition[11],
                DictionaryTable.DEFINITION_COLUMN_NAME(): definition[12],
                DictionaryTable.REGIONAL_SETTINGS_DEFINITION_COLUMN_NAME(): definition[
                    13
                ],
                DictionaryTable.DATE_COLUMN_NAME(): definition[14],
                "morpheme": morpheme,
            },
            id=doc_id,
            timeout=index_definition_timeout,
        )

    def index_lemma(self, definition_to_index, morphemes):
        """
        Index an entry in the dictionary as a corpus entry.
        The indexed document here used has the same exact structure
        of the one used in CorpusIndexer.

        :param definition_to_index: index of the definition inside the
        list of definitions for the lemma
        :param morphemes: all the formal morphemes associated to the lemma
        """
        doc_body_id = str(definition_to_index[0]) + "-" + str(definition_to_index[4])
        doc_id = doc_body_id + "-" + str(definition_to_index[8])
        try:
            self.elasticsearch.index(
                index=self.package_name,
                doc_type="doc",
                body={
                    CorpusTable.ID_COLUMN_NAME(): doc_body_id,
                    CorpusTable.SUB_ID_COLUMN_NAME(): str(definition_to_index[8]),
                    CorpusTable.SCENARIO_TYPE_COLUMN_NAME(): definition_to_index[
                        4
                    ],  # DictionaryTable.POS_PARADIGM_COLUMN_NAME()
                    CorpusTable.EVENT_MESSAGE_COLUMN_NAME(): definition_to_index[
                        12
                    ],  # DictionaryTable.DEFINITION_COLUMN_NAME()
                    CorpusTable.HIDDEN_COLUMN_NAME(): "",
                    CorpusTable.FIELD_COLUMN_NAME(): definition_to_index[
                        2
                    ],  # DictionaryTable.LEMMA_COLUMN_NAME()
                    CorpusTable.LAMBDA_CONDITION_COLUMN_NAME(): "",
                    CorpusTable.UI_EVENT_COLUMN_NAME(): "",
                    CorpusTable.ACTION_COLUMN_NAME(): "",
                    CorpusTable.SOURCE_COLUMN_NAME(): definition_to_index[
                        10
                    ],  # DictionaryTable.SOURCE_COLUMN_NAME()
                    CorpusTable.REGIONAL_SETTINGS_COLUMN_NAME(): definition_to_index[
                        13
                    ],  # DictionaryTable.REGIONAL_SETTINGS_DEFINITION_COLUMN_NAME()
                    CorpusTable.COMPLEXITY_COLUMN_NAME(): "",
                },
                id=doc_id,
                timeout=index_lemma_timeout,
            )
            for morpheme in morphemes:
                self._index_definition(definition_to_index, morpheme.text)
        except Exception as ex:
            mess = "Indexing Error: {}".format(ex)
            log.error(mess, exc_info=ex)
            raise ex

    def index_dictionary(
        self, dictionary, standard, spreadsheet_id: str, sheet_title: str,
    ):
        dataset_name = f"{spreadsheet_id}-{sheet_title}"
        have_to_index = CurrentIndexInventory.have_to_index_data(
            self.package_name, dataset_name, dictionary
        )
        if have_to_index:
            for index, lemma in enumerate(
                dictionary[DictionaryTable.LEMMA_COLUMN_NAME()]
            ):
                data = [
                    dictionary[DictionaryTable.LEMMA_COLUMN_NAME()][index],
                    dictionary[DictionaryTable.WORD_TYPE_COLUMN_NAME()][index],
                    dictionary[DictionaryTable.REGIONAL_SETTINGS_LEMMA_COLUMN_NAME()][
                        index
                    ],
                    dictionary[DictionaryTable.AFI_COLUMN_NAME()][index],
                    dictionary[DictionaryTable.POS_PARADIGM_COLUMN_NAME()][index],
                    dictionary[DictionaryTable.MORPH_PARADIGM_COLUMN_NAME()][index],
                    dictionary[DictionaryTable.MISS_PARADIGM_COLUMN_NAME()][index],
                    dictionary[DictionaryTable.FET_PARADIGM_COLUMN_NAME()][index],
                    int(
                        dictionary[DictionaryTable.DEFINITION_INDEX_COLUMN_NAME()][
                            index
                        ]
                    ),
                    dictionary[DictionaryTable.FEATURES_COLUMN_NAME()][index],
                    dictionary[DictionaryTable.SOURCE_COLUMN_NAME()][index],
                    dictionary[DictionaryTable.TOPIC_COLUMN_NAME()][index],
                    dictionary[DictionaryTable.DEFINITION_COLUMN_NAME()][index],
                    dictionary[
                        DictionaryTable.REGIONAL_SETTINGS_DEFINITION_COLUMN_NAME()
                    ][index],
                    dictionary[DictionaryTable.DATE_COLUMN_NAME()][index],
                    dictionary[DictionaryTable.TIMESTAMP_COLUMN_NAME()][index],
                ]
                morphemes = standard.get_morphemes(
                    dictionary[DictionaryTable.POS_PARADIGM_COLUMN_NAME()][index],
                    dictionary[DictionaryTable.MORPH_PARADIGM_COLUMN_NAME()][
                        index
                    ].split(" ")[0],
                    dictionary[DictionaryTable.LEMMA_COLUMN_NAME()][index],
                    dictionary[
                        DictionaryTable.REGIONAL_SETTINGS_DEFINITION_COLUMN_NAME()
                    ][index],
                )
                self.index_lemma(data, morphemes)
            CurrentIndexInventory.set_index_data(
                self.package_name, dataset_name, dictionary
            )

    def get_receipt(self, lemma, definition):
        res = self.elasticsearch.search(
            index=self.definition_index_name,
            body={
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {
                                    DictionaryTable.DEFINITION_COLUMN_NAME(): definition
                                }
                            },
                            {"match": {DictionaryTable.LEMMA_COLUMN_NAME(): lemma}},
                        ]
                    }
                }
            },
        )
        if res["hits"]["total"] > 0:
            return (
                "definition: "
                + definition
                + "\ncorrectly saved in spreadsheet with id: "
                + self.package_name
                + "\nfor lemma: "
                + lemma
            )
        else:
            return "Definition not found!!!"

    def get_defined_lemmas(self, date: str):
        try:
            docs = self.elasticsearch.search(
                index=self.definition_index_name,
                doc_type="doc",
                body={
                    "query": {"match": {DictionaryTable.DATE_COLUMN_NAME(): date}},
                    "size": CONCORDANCE_QUERY_SIZE,
                },
            )
            s = set()
            l_hits = docs["hits"]["hits"]
            for lemma in l_hits:
                s.add(lemma["_source"]["lemma"])
            return list(s)
        except TransportError as error:
            if error.error != "index_not_found_exception":
                print(str(error))
            return []
