''' Get contacts from Hubspot via API '''

import requests
import json
import pandas as pd

def get_contacts(hapikey, offset):

properties = ["firstname","lastname","email","company","jobtitle","phone","address","city","state","zip","country","twitter","facebook","linkedin"]

params = {
    'hapikey': hapikey,
    'property': properties,
    'count': 100,
    'vidOffset': offset
}

r = requests.get("https://api.hubapi.com/contacts/v1/lists/all/contacts/all", params=params)

if r.status_code == 200:
    return r.json()
else:
    return None

def export_contacts_to_dataframe(contacts):
    ''' Export contacts to Pandas DataFrame '''
    df = pd.DataFrame(columns=[properties])
    for i, contact in enumerate(contacts):
        #add each property to a columns
        for p in properties:
            if p in contact['properties'].keys():
                df.loc[i, p] = contact['properties'][p]['value']
            else:
                df.loc[i, p] = ''
    return df
