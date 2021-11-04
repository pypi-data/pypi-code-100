import json
import requests
import urllib3


class ChemistryService:
    endpoint = None
    api = None

    def __init__(self, api, base):
        urllib3.disable_warnings()
        self.api = api
        self.service = base + "/chemistryservice.kh.svc/v1/"

    def get_token(self):
        return self.api.get_token()

    #
    #  retrieve the compound NSI from the COMPOUND index using the names
    #  as values. Repeat the query as long as we get limit records
    #
    def getCompoundByName(self, name):
        retries = 0
        result = []
        while retries < 5:
            retries += 1
            r = requests.get(f'{self.service}name_to_structure', verify=False, params={'name': name}, headers={"Authorization": f"Bearer {self.get_token()}"})
            if r.status_code == 200:
                if 'result' in r.json():
                    return r.json()['result']
            elif r.status_code == 401:
                self.api.reconnect()
                continue
            else:
                print(f"Cannot retrieve compoundIds from {self.service}: {r.status_code}")
                return None

    def getSMILESByName(self, name):
        return [self.getCompoundByName(name)]

    def getStandardizedSMILES(self, smiles):
        response = self.paStandardize(smiles, 'clinical')
        if response is not None and type(response) == tuple:
            inchikey, smiles = response
            return smiles
        else:
            return response

    #
    # Single endpoint to standardise molecules and to retrieve structures from names for the Primitive Adapters.
    # Compound should be either a name (such as paracetamol) when pa_type is 'clinical', or a SMILES string when pa_type is 'clinical'
    # Returns a SMILES
    #
    def paStandardize(self, compound, pa_type):
        retries = 0
        while retries < 5:
            retries += 1
            r = requests.post(f'{self.service}pa_standardize', verify=False, data={'compound': compound, 'pa_type':pa_type}, headers={"Authorization": f"Bearer {self.get_token()}"})
            if r.status_code == 200:
                if 'Empty response' in r.json():
                    if r.json()['Empty response'] == 'Request is valid. But no result found for query.':
                        return None
                    else:
                        return r.json()['Empty response']
                if 'result' in r.json():
                    return (r.json()['result'][0]['inchikey'], r.json()['result'][0]['smiles'])
            elif r.status_code == 401:
                self.api.reconnect()
                continue
            else:
                print(f"Cannot retrieve compoundIds from endpoint {self.service}: {r.status_code}")
                return None
