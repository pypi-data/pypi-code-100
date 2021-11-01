import json, os
from elasticsearch import RequestsHttpConnection
from elasticsearch.helpers import bulk
from elasticsearch_dsl import connections, Search, Document, UpdateByQuery
import boto3, json
from collections import Counter
from requests_aws4auth import AWS4Auth

class Manager(object):
    
    def __init__(self, hosts, access_key=None, secret_key=None, region='eu-west-3', service='es', use_ssl=True, verify_certs=True, timeout=60):
        
        if access_key is None or secret_key is None:
            credentials = boto3.Session().get_credentials()
            access_key = credentials.access_key
            secret_key = credentials.secret_key

        awsauth = AWS4Auth(access_key, secret_key, region, service)
        
        self.connect = connections.create_connection(
                        hosts=hosts,
                        timeout=timeout,
                        http_auth = awsauth,
                        use_ssl = use_ssl,
                        verify_certs = use_ssl,
                        connection_class = RequestsHttpConnection
                    )


        
    def _check_field_cross_index(self, field_values, index, field):
        """
        """
        query_2 = {"query": {"terms": {field: field_values}}}
        res2 = self.get_from_index(index, query_2)
        return res2[1]



    def check_field_cross_index(self, from_index, to_index, field):
        """

        """
        query_1 = {"query": {"match_all": {}}}
        res1 = self.get_from_index(from_index, query_1)
        # print(type(list(res1[0])))
        field_values = [hit.to_dict().get(field, 'fake') for hit in res1[0]]
        print(len(field_values))
        return self._check_field_cross_index(field_values, to_index, field)
        # values = [self._check_field_cross_index(hit, to_index, field)   for hit in res1[0]]
        # return Counter(values)

            
    def get_index_as_partial_dict(self, index, cols):
        l = []
        search_dict = {
        "_source": cols,
        "query": {
          "match_all": {  
          }
        }
        }

        s = Search().from_dict(search_dict).index(index).scan()
        for hit in tqdm(s):
            d = hit.to_dict()
            d["_id"] = hit.meta.id
            l.append(d)
        return l
        

    def gendata(index, docs):
    for doc in docs:
        yield {
            "_op_type": "update",
            "_index": index,
            "_id": doc["_id"],
            "doc": {doc['column']: doc["value"]}
        }
        print("end gen")


    def get_from_index(self, index, body: [str, dict]):
        """
        """
        if isinstance(body, str):
            body = json.loads(body)


        results = Search().from_dict(body).index(index)
        results.execute()
        # print("#######ES query gives {} articles".format(results.count()))
        return (results.scan(), results.count())

        # for hit in results.scan():
        #     print(hit.to_dict()['DOI'])
        #     break
        # print("#######ES query gives {} articles".format(results.count()))

        
    def create_index(self, index_name: str, settings: None, erase_if_exists: bool=False):
        
        if settings is None:
             settings = {
                "settings":{
                    "number_of_shards":5,
                    "number_of_replicas":1,
                    "analysis":{
                        "filter":{"backslash":{"pattern":"\\[a-z]","type":"pattern_replace","replacement":""},
                        "english_snowball":{"type":"snowball","language":"English"},
                        "english_stop":{"type":"stop","stopwords":"_english_"}},
                        "analyzer":{
                        "classic_analyzer":{
                            "filter":["lowercase","backslash"],
                            "char_filter":["html_strip"],
                            "type":"custom",
                            "tokenizer":"standard"},
                        "stopword_analyzer":{
                            "filter":["lowercase","backslash","english_stop","english_snowball"],
                            "char_filter":["html_strip"],
                            "type":"custom",
                            "tokenizer":"standard"}
                        }
                    }
                    },
                    "mappings":{
                    "properties":{
                        "DOI":{"type":"keyword"},
                        "prefix_doi": {"type": "keyword"},
                        "URL":{"type":"keyword"},
                        "abstract":{"type":"text","analyzer":"classic_analyzer","search_analyzer":"stopword_analyzer","search_quote_analyzer":"classic_analyzer"},
                        "abstract_clean":{"type":"keyword"},
                        "authors":{"type":"keyword"},
                        "fullText":{"type":"text","analyzer":"classic_analyzer","search_analyzer":"stopword_analyzer","search_quote_analyzer":"classic_analyzer"},
                        "fullText_clean":{"type":"text"},
                        "keywords":{"type":"keyword"},
                        "language":{"type":"keyword"},
                        "openaire_id":{"type":"keyword"},
                        "provider":{"type":"keyword"},
                        "provider_id":{"type":"keyword"},
                        "publication_date":{"type":"date","ignore_malformed":True,"format":"yyyy-mm-dd"},
                        "title":{"type":"text"},
                        "citation": {"type": "text"},
                        # "ISBN": {"type": "keyword"},

                        },
                    }
            }
        
        if self.connect.indices.exists(index_name):
            print(index_name + " index already exists")
            if(erase_if_exists):
                print(index_name + " deleted and recreated")
                self.connect.indices.delete(index=index_name)
        try:
            self.connect.indices.create(index=index_name,body=settings,ignore=400)
        except Exception as e:
            print(e)
        
        
    def save_to_index(self, generator):
        print('Bulk starts')
        res = bulk(self.connect, generator, raise_on_error=False, raise_on_exception=False)
        print(res)
        
        

