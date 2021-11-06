

r = None


"""
Method to clean data following schema.org format
"""
import requests

import json

class Schema_org:


    def __init__(self):


        self.schemas = {}

        self._download_data()


    def get_datatype(self, schema_id):
        """Returns data type for the given key
        """

        datatype = self.get_schema(schema_id).get('schema:rangeIncludes', None)

        if not isinstance(datatype, list):
            datatype = [datatype]

        datatypes = []

        for i in datatype:
            if i:
                d = i.get('@id', None)
                datatypes.append(d)


        return datatypes


    def get_schema(self, schema_id):

        schema = self.schemas.get(schema_id, {})

        return schema


    def get_schemas(self):

        schemas = self.schemas.keys()

        return schemas


    def _download_data(self):
        """Download schema_org data
        """

        global r

        if r:
            self.schemas = r
            return


        url = 'https://schema.org/version/latest/schemaorg-current-https.jsonld'
        r = requests.get(url)


        data = r.json()

        for i in data.get('@graph', []):
            schema_id = i.get('@id', None)
            self.schemas[schema_id] = i 
            
        r = self.schemas
 