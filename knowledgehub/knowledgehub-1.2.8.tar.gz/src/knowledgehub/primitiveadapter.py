import json
import traceback

import requests
import urllib3
from . import constants


def getSubjects(subjects: str):
    return int(subjects.split('/')[0])


class PrimitiveAdapter:
    endpoint = None
    api = None

    def __init__(self, api, endpoint, mode):
        urllib3.disable_warnings()
        self.api = api
        self.mode = mode
        self.endpoint = endpoint

    def get_token(self):
        return self.api.get_token()

    def index(self, conceptCode):
        json_data = {
            "searchConcept": None,
            "filter": {
                "criteria": [
                    [
                        {
                            "field": {
                                "dataClassKey": "COMPOUND",
                                "name": "name"
                            },
                            "primitiveType": "String",
                            "comparisonOperator": "EQUALS",
                            "caseSensitive": False,
                            "values": [
                                {
                                    "value": "terbinafine"
                                }
                            ]
                        }
                    ]
                ]
            },
            "selectedFields": [
                {
                    "dataClassKey": "FINDING",
                    "names": [
                        "id",
                        "compoundIdentifier",
                        "name",
                        "inchi",
                        "inchiKey",
                        "smiles",
                        "confidentiality",
                        "organisation",
                        "createdDate",
                        "modifiedDate"
                    ]
                }
            ],
            "sortFields": [
                {
                    "field": {
                        "dataClassKey": "COMPOUND",
                        "name": "id"
                    },
                    "order": "ASC"
                }
            ],
            "Offset": 0,
            "Limit": 100
        }

        r = requests.post(self.endpoint + 'query', verify=False, headers={"Authorization": f"Bearer {self.get_token()}"}, json=json_data, timeout=None)

        if r.status_code == 200:
            return json.loads(r.text)
        else:
            print(f"Cannot search in {self.endpoint}: {r.status_code}")
            return None

    #
    # retrieve all unique compounds using the data endpoint
    #
    def getAllCompounds(self, maximum: int = None):
        result = []

        r = requests.get(self.endpoint + 'count', verify=False, params={'dataClassKey': 'COMPOUND'}, headers={"Authorization": f"Bearer {self.get_token()}"})
        limit = maximum if maximum is not None else int(r.text)
        size = min(limit, 1000)
        if r.status_code == 200:
            for offset in range(0, limit, size):
                print(f'retrieving {offset} of {limit} compounds')
                r = requests.get(self.endpoint + 'data', params={'dataClassKey': 'COMPOUND', 'limit': size, 'offset': offset}, verify=False, headers={"Authorization": f"Bearer {self.get_token()}"}, timeout=None)

                if r.status_code == 200:
                    for compound in json.loads(r.text):
                        if compound not in result:
                            result.append(compound)
                else:
                    print(f"Cannot retrieve compoundIds from {self.endpoint}: {r.status_code}")

        return result

    #
    # retrieve all adverse events using the data endpoint
    # Mon 5 april: added the reconnect to handle expiration of a token with long running tasks.
    #
    def getAllFindings(self, maximum: int = None):
        result = []
        tries = 0
        if maximum is None:
            for tries in range(0, 5):
                r = requests.get(self.endpoint + 'count', verify=False, params={'dataClassKey': 'FINDING'}, headers={"Authorization": f"Bearer {self.get_token()}"}, timeout=None)
                if r.status_code == 200:
                    maximum = int(r.text)
                elif r.status_code == 401:
                    self.api.reconnect()
                else:
                    print(f"Cannot retrieve findings from {self.endpoint}: {r.status_code}")

        if maximum is not None:
            size = min(maximum, 1000)
            for offset in range(0, maximum, size):
                for tries in range(0, 5):
                    print(f'retrieving records {offset}-{offset+size}...')
                    r = requests.get(self.endpoint + 'data', params={'dataClassKey': 'FINDING', 'limit': size, 'offset': offset}, verify=False, headers={"Authorization": f"Bearer {self.get_token()}"})
                    if r.status_code == 200:
                        for finding in json.loads(r.text):
                            result.append(finding)
                    elif r.status_code == 401:
                        self.api.reconnect()
                    else:
                        print(f"Cannot retrieve findings from {self.endpoint}: {r.status_code}")
                    break

        return result

    # 
    #  retrieve the compound identifiers from the COMPOUND index using the names 
    #  as values. Repeat the query as long as we get limit records
    #
    def getCompoundIdsByNames(self, names):
        result = [];

        query = {
            "offset": 0,
            "limit": 100,
            "searchConcept": None,
            "filter": {
                "criteria": [
                    [
                        {
                            "field": {
                                "dataClassKey": "COMPOUND",
                                "name": "name"
                            },
                            "primitiveType": "String",
                            "comparisonOperator": "IN",
                            "caseSensitive": False,
                            "values": [{'value': name} for name in names]
                        }
                    ]
                ]
            },
            "selectedFields": [
                {
                    "dataClassKey": "COMPOUND",
                    "names": [
                        "id"
                    ]
                }
            ]
        }

        while True:
            r = requests.post(self.endpoint + 'query', verify=False, headers={"Authorization": f"Bearer {self.get_token()}"}, json=query, timeout=None)

            if r.status_code == 200:
                response = json.loads(r.text)
                data = response['resultData']['data']
                for compound in data:
                    compound_id = compound['COMPOUND']['id']
                    if compound_id not in result:
                        result.append(compound_id)
                nr_records = len(data)
            elif r.status_code == 401:
                self.api.reconnect()
                continue
            else:
                print(f"Cannot retrieve compoundIds from {self.endpoint}: {r.status_code}")
                nr_records = 0

            if nr_records < query['limit']:
                break
            else:
                query['offset'] += query['limit']

        return result

    def getCompoundsByInchiKeys(self, inchiKeys):

        if inchiKeys is not None:
            inchiKeys = inchiKeys if isinstance(inchiKeys, list) else [inchiKeys]

            result = []

            query = {
                "offset": 0,
                "limit": 100,
                "searchConcept": None,
                "filter": {
                    "criteria": [
                        [
                            {
                                "field": {
                                    "dataClassKey": "COMPOUND",
                                    "name": "inchiKey"
                                },
                                "primitiveType": "String",
                                "comparisonOperator": "IN",
                                "caseSensitive": False,
                                # "values": [{'value': inchiKey} for inchiKey in inchiKeys]
                                "values": None
                            }
                        ]
                    ]
                },
                "selectedFields": [
                    {
                        "dataClassKey": "COMPOUND",
                        "names": [
                            "id",
                            'name',
                            "inchiKey",
                            "smiles"
                        ]
                    }
                ]
            }

            for i in range(0, len(inchiKeys), 500):
                print(f'start:{i}')
                query['filter']['criteria'][0][0]['values'] = [{'value': inchiKey} for inchiKey in inchiKeys[i:i+500]]
                while True:
                    r = requests.post(self.endpoint + 'query', verify=False, headers={"Authorization": f"Bearer {self.get_token()}"}, json=query, timeout=None)

                    if r.status_code == 200:
                        response = json.loads(r.text)
                        data = response['resultData']['data']
                        for compound in data:
                            result.append(compound['COMPOUND'])
                        nr_records = len(data)
                    elif r.status_code == 401:
                        self.api.reconnect()
                        continue
                    else:
                        print(f"Cannot retrieve compounds from {self.endpoint}: {r.status_code}")
                        nr_records = 0

                    if nr_records < query['limit']:
                        break
                    else:
                        query['offset'] += query['limit']

            return result

        else:
            return None

    def getStudiesByCompoundNames(self, compound_names, maximum: int = None):
        result = []
        limit = maximum if maximum is not None else 1000

        if len(compound_names) > 0:

            query = {"searchConcept": {
                "concepts": None,
                "targetConceptGroups": None
            }, "filter": {
                "criteria": [
                    [
                        {
                            "field": {
                                "dataClassKey": "COMPOUND",
                                "name": "name"
                            },
                            "primitiveType": "String",
                            "comparisonOperator": "IN",
                            "values": [{'value': compound_name} for compound_name in compound_names],
                            "caseSensitive": False
                        }
                    ]
                ]
            }, "selectedFields": [
                {
                    "dataClassKey": "STUDY",
                    "names": [
                        "id",
                        "studyIdentifier",
                    ]
                },
                {
                    "dataClassKey": "FINDING",
                    "names": [
                        "id",
                        "specimenOrgan",
                        "specimenOrganCode",
                        "specimenOrganVocabulary",
                        "finding",
                        "findingCode",
                        "findingVocabulary",
                        "frequency",
                        "severity"
                    ]
                },
                {
                    "dataClassKey": "COMPOUND",
                    "names": [
                        "name",
                        "compoundIdentifier",
                        'smiles',
                    ]
                }
            ], 'offset': 0, 'limit': limit}

            while True:
                r = requests.post(self.endpoint + 'query', verify=False, headers={"Authorization": f"Bearer {self.get_token()}"}, json=query, timeout=None)

                if r.status_code == 200:
                    response = json.loads(r.text)
                    if query['offset'] == 0:
                        total = response['resultData']['total']

                    record_count = len(response['resultData']['data'])
                    for record in response['resultData']['data']:
                        record['source'] = response['origin']
                        if self.mode == constants.USE_SEVERITY:
                            record['FINDING']['count'] = int(record['FINDING']['severity'])
                        elif self.mode == constants.USE_FREQUENCY:
                            frequency, total = record['FINDING']['frequency'].split('/', 1)
                            record['FINDING']['count'] = int(frequency)
                        elif self.mode == constants.INITIALIZE_1:
                            record['FINDING']['count'] = 1
                        result.append(record)
                        if maximum is not None and len(result) >= maximum:
                            break
                elif r.status_code == 401:
                    self.api.reconnect()
                    continue
                else:
                    record_count = 0

                if record_count < query['limit'] or (maximum is not None and len(result) >= maximum):
                    break

                query['offset'] += query['limit']
            return result
        else:
            print(f"No compound names specified for searching {self.endpoint}")
            return None

    #
    # This method retrieves compounds from the database by its identifier
    # 
    def getStudiesByCompoundIds(self, compound_ids, maximum: int = None):
        limit = maximum if maximum is not None else 1000
        result = []

        if len(compound_ids) > 0:
            query = {"searchConcept": {
                "concepts": None,
                "targetConceptGroups": None
            }, "filter": {
                "criteria": [
                    [
                        {
                            "field": {
                                "dataClassKey": "COMPOUND",
                                "name": "compoundIdentifier"
                            },
                            "primitiveType": "String",
                            "comparisonOperator": "IN",
                            "caseSensitive": "True",
                            "values": [{'value': compound_id} for compound_id in compound_ids]
                        }
                    ]
                ]
            }, "selectedFields": [
                {
                    "dataClassKey": "FINDING",
                    "names": [
                        "specimenOrgan",
                        "specimenOrganVocabulary",
                        "specimenOrganVocabulary",
                        "finding",
                        "findingCode",
                        "findingVocabulary",
                        "frequency",
                        "severity"
                    ]
                },
                {
                    "dataClassKey": "COMPOUND",
                    "names": [
                        "name",
                        "compoundIdentifier",
                    ]
                }
            ], 'offset': 0, 'limit': limit}

            while True:
                r = requests.post(self.endpoint + 'query', verify=False, headers={"Authorization": f"Bearer {self.get_token()}"}, json=query, timeout=None)

                if r.status_code == 200:
                    response = json.loads(r.text)
                    if query['offset'] == 0:
                        total = response['resultData']['total']

                    for record in response['resultData']['data']:
                        record['source'] = response['origin']
                        if self.mode == constants.USE_SEVERITY:
                            record['FINDING']['count'] = int(record['FINDING']['severity'])
                        elif self.mode == constants.INITIALIZE_1:
                            record['FINDING']['count'] = 1
                        result.append(record)

                        if maximum is not None and len(result) >= maximum:
                            break

                elif r.status_code == 401:
                    self.api.reconnect()
                    continue
                else:
                    record_count = 0

                if record_count < query['limit']:
                    break

                query['offset'] += query['limit']
            return result
        else:
            print(f"Cannot search in {self.endpoint}")
            return None


    def getStudiesBySMILESandSOC(self, SMILES, SOC, maximum: int = None):
        limit = maximum if maximum is not None else 1000
        result = []

        if SMILES is not None:
            query = {"searchConcept": {
                "concepts": None,
                "targetConceptGroups": None
            }, "filter": {
                "criteria": [
                    [
                        {
                            "field": {
                                "dataClassKey": "COMPOUND",
                                "name": "smiles"
                            },
                            "primitiveType": "String",
                            "comparisonOperator": "EQUALS",
                            "caseSensitive": True,
                            "values": [
                                {
                                    "value": SMILES
                                }
                            ]
                        },
                        {
                            "field": {
                                "dataClassKey": "FINDING",
                                "name": "specimenOrganCode"
                            },
                            "primitiveType": "String",
                            "comparisonOperator": "EQUALS",
                            "caseSensitive": True,
                            "values": [
                                {
                                    "value": SOC
                                }
                            ]
                        }
                    ]
                ]
            }, "selectedFields": [
                {
                    "dataClassKey": "FINDING",
                    "names": [
                        "specimenOrgan",
                        "specimenOrganCode",
                        "specimenOrganVocabulary",
                        "finding",
                        "findingCode",
                        "findingVocabulary",
                        "frequency",
                        "severity"
                    ]
                },
                {
                    "dataClassKey": "COMPOUND",
                    "names": [
                        "name",
                        "compoundIdentifier",
                        "smiles",
                    ]
                }
            ], 'offset': 0, 'limit': limit}

            while True:
                r = requests.post(self.endpoint + 'query', verify=False, headers={"Authorization": f"Bearer {self.get_token()}"}, json=query, timeout=None)
                if r.status_code == 200:
                    response = json.loads(r.text)
                    if query['offset'] == 0:
                        total = response['resultData']['total']

                    record_count = len(response['resultData']['data'])
                    for record in response['resultData']['data']:
                        record['source'] = response['origin']
                        if self.mode == constants.USE_SEVERITY:
                            record['FINDING']['count'] = int(record['FINDING']['severity'])
                        elif self.mode == constants.INITIALIZE_1:
                            record['FINDING']['count'] = 1
                        result.append(record)
                        if maximum is not None and len(result) >= maximum:
                            break

                elif r.status_code == 401:
                    self.api.reconnect()
                    continue
                else:
                    record_count = 0

                if record_count < query['limit']:
                    break

                query['offset'] += query['limit']
            return result
        else:
            print(f"Cannot search in {self.endpoint}")
            return None

    def getStudiesBySMILES(self, SMILES, maximum: int = None):
        limit = maximum if maximum is not None else 1000
        result = []

        if SMILES is not None:
            SMILES = SMILES if isinstance(SMILES, list) else [SMILES]

            query = {"searchConcept": {
                "concepts": None,
                "targetConceptGroups": None
            }, "filter": {
                "criteria": [
                    [
                        {
                            "field": {
                                "dataClassKey": "COMPOUND",
                                "name": "smiles"
                            },
                            "primitiveType": "String",
                            "comparisonOperator": "IN",
                            "caseSensitive": True,
                            "values": [{'value': smile} for smile in SMILES]
                        }
                    ]
                ]
            }, "selectedFields": [
                {
                    "dataClassKey": "STUDY",
                    "names": [
                        "id",
                        "studyIdentifier",
                        "species",
                    ]
                },
                {
                    "dataClassKey": "FINDING",
                    "names": [
                        "specimenOrgan",
                        "specimenOrganCode",
                        "specimenOrganVocabulary",
                        "finding",
                        "findingCode",
                        "findingVocabulary",
                        "frequency",
                        "severity"
                    ]
                },
                {
                    "dataClassKey": "COMPOUND",
                    "names": [
                        "name",
                        "compoundIdentifier",
                        "smiles",
                    ]
                }
                ], 'offset': 0, 'limit': limit}

            while True:
                r = requests.post(self.endpoint + 'query', verify=False, headers={"Authorization": f"Bearer {self.get_token()}"}, json=query, timeout=None)

                if r.status_code == 200:
                    response = json.loads(r.text)
                    if query['offset'] == 0:
                        total = response['resultData']['total']

                    record_count = len(response['resultData']['data'])
                    for record in response['resultData']['data']:
                        record['source'] = response['origin']
                        if self.mode == constants.USE_SEVERITY:
                            record['FINDING']['count'] = getSubjects(record['FINDING']['frequency'])
                        elif self.mode == constants.INITIALIZE_1:
                            record['FINDING']['count'] = 1
                        result.append(record)
                        if maximum is not None and len(result) >= maximum:
                            break
                elif r.status_code == 401:
                    self.api.reconnect()
                    continue
                else:
                    record_count = 0

                if record_count < query['limit']:
                    break

                query['offset'] += query['limit']

            return result

        else:
            print(f"Cannot search in {self.endpoint}")
            return None

    def getStudiesCountBySMILES(self, SMILES):
        if SMILES is not None:
            SMILES = SMILES if isinstance(SMILES, list) else [SMILES]

            query = {"searchConcept": {
                "concepts": None,
                "targetConceptGroups": None
            }, "filter": {
                "criteria": [
                    [
                        {
                            "field": {
                                "dataClassKey": "COMPOUND",
                                "name": "smiles"
                            },
                            "primitiveType": "String",
                            "comparisonOperator": "IN",
                            "caseSensitive": True,
                            "values": [{'value': smile} for smile in SMILES]
                        }
                    ]
                ]
            },
            "selectedFields": [
                {
                    "dataClassKey": "STUDY",
                    "names": [
                        "id",
                        "studyIdentifier",
                    ]
                },
                {
                    "dataClassKey": "FINDING",
                    "names": [
                        "specimenOrgan",
                        "specimenOrganCode",
                        "specimenOrganVocabulary",
                        "finding",
                        "findingCode",
                        "findingVocabulary",
                        "frequency",
                        "severity"
                    ]
                },
                {
                    "dataClassKey": "COMPOUND",
                    "names": [
                        "name",
                        "compoundIdentifier",
                        "smiles",
                    ]
                }
               ],
            'offset': 0, 'limit': 0}

            tries = 0
            while tries < 5:
                r = requests.post(self.endpoint + 'query', verify=False, headers={"Authorization": f"Bearer {self.get_token()}"}, json=query, timeout=None)
                tries += 1
                if r.status_code == 200:
                    response = json.loads(r.text)
                    total = response['resultData']['total']
                    return total
                elif r.status_code == 401:
                    self.api.reconnect()
                    continue
        else:
            print(f"Cannot search in {self.endpoint}")
            return None

    def getStudiesCountByInchiKeys(self, inchiKeys):
        if inchiKeys is not None:
            SMILES = inchiKeys if isinstance(inchiKeys, list) else [inchiKeys]

            query = {"searchConcept": {
                "concepts": None,
                "targetConceptGroups": None
            }, "filter": {
                "criteria": [
                    [
                        {
                            "field": {
                                "dataClassKey": "COMPOUND",
                                "name": "inchiKey"
                            },
                            "primitiveType": "String",
                            "comparisonOperator": "IN",
                            "caseSensitive": True,
                            "values": [{'value': inchiKey} for inchiKey in inchiKeys]
                        }
                    ]
                ]
            },
            "selectedFields": [
                {
                    "dataClassKey": "STUDY",
                    "names": [
                        "id",
                        "studyIdentifier",
                    ]
                },
                {
                    "dataClassKey": "FINDING",
                    "names": [
                        "specimenOrgan",
                        "specimenOrganCode",
                        "specimenOrganVocabulary",
                        "finding",
                        "findingCode",
                        "findingVocabulary",
                        "frequency",
                        "severity"
                    ]
                },
                {
                    "dataClassKey": "COMPOUND",
                    "names": [
                        "name",
                        "compoundIdentifier",
                        "inchiKey",
                    ]
                }
               ],
            'offset': 0, 'limit': 0}

            tries = 0
            while tries < 5:
                r = requests.post(self.endpoint + 'query', verify=False, headers={"Authorization": f"Bearer {self.get_token()}"}, json=query, timeout=None)
                tries += 1
                if r.status_code == 200:
                    response = json.loads(r.text)
                    total = response['resultData']['total']
                    return total
                elif r.status_code == 401:
                    self.api.reconnect()
                    continue
        else:
            print(f"Cannot search in {self.endpoint}")
            return None


    
    #
    # retrieve all the additional properties using the data endpoint
    #
    def getAllAdditionalProperties(self, endpoint, idx, propertyName):
        result = []
                   
        query = {
            "propertyName": propertyName,
            "resultType": "TREE",
            "offset": 0,
            "limit": 1000
        }
        
        r = requests.post(self.endpoint + endpoint + idx + '/additionalproperties', verify=False, headers={"Authorization": f"Bearer {self.get_token()}"}, json=query)
        if r.status_code == 200:
            n_rows = json.loads(r.text)['total']
            
        for offset in range(0, n_rows, 1000):
            query['offset'] = offset
            r = requests.post(self.endpoint + endpoint + idx + '/additionalproperties', verify=False, headers={"Authorization": f"Bearer {self.get_token()}"}, json=query)
            if r.status_code == 200:
                for data in json.loads(r.text)['data']:
                    result.append(data)
            else:
                print(f"Cannot retrieve compoundIds from {self.endpoint + endpoint + idx + '/additionalproperties'}: {r.status_code}")

        return result
