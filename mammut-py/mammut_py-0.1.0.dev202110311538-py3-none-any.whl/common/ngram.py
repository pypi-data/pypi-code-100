# coding=utf-8
from elasticsearch import Elasticsearch, TransportError
from mammut import ES_HOSTS, CONCORDANCE_QUERY_SIZE


class NGram:
    def __init__(self):
        self.elasticsearch = Elasticsearch(ES_HOSTS)

    def get_ngram(self, index, ngram):
        try:
            docs = self.elasticsearch.search(
                index=index,
                doc_type="doc",
                body={
                    "query": {"match": {"ngram": ngram}},
                    "size": CONCORDANCE_QUERY_SIZE,
                },
            )
            s = list()
            l_hits: list() = docs["hits"]["hits"]
            for ngrams in l_hits:
                s.append(ngrams["_source"])
            return list(s)
        except TransportError as error:
            if error.error != "index_not_found_exception":
                print(str(error))
            return []

    def get_ngram_regional_settings(self, index, ngram, regional_settings):
        try:
            docs = self.elasticsearch.search(
                index=index,
                doc_type="doc",
                body={
                    "query": {
                        "bool": {
                            "must": [
                                {"match": {"ngram": ngram}},
                                {"match": {"regional_settings": regional_settings}},
                            ]
                        }
                    },
                    "size": CONCORDANCE_QUERY_SIZE,
                },
            )
            s = list()
            l_hits: list() = docs["hits"]["hits"]
            for ngrams in l_hits:
                s.append(ngrams["_source"])
            return list(s)

        except TransportError as error:
            if error.error != "index_not_found_exception":
                print(str(error))
            return []
