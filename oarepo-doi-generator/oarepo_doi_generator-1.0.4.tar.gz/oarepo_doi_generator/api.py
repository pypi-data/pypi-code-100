import json

from flask import current_app
from invenio_db import db
from invenio_pidstore.models import PersistentIdentifier, PIDStatus
from jsonref import requests
from flask_login import current_user
from .new_datasets_mapping import schema_mapping
import datetime

def doi_request(record, publisher):
    date = datetime.datetime.now()
    date = str(date)
    if "oarepo:doirequest" not in record:
        record['oarepo:doirequest'] = {"publisher": publisher, "requestedBy": current_user.id, "requestedDate": date}

    record.commit()
    db.session.commit()
    return record

def doi_approved(record, pid_type, test_mode = False):

    if "oarepo:doirequest" in record:
        publisher = record["oarepo:doirequest"]["publisher"]
        data = schema_mapping(record, pid_type, publisher, test_mode=test_mode)
        doi_registration(data=data, test_mode=test_mode)
        doi = data['data']['attributes']['doi']
        if "persistentIdentifiers" not in record:
            record['persistentIdentifiers'] = [{
                    "identifier": doi,
                    "scheme": "DOI",
                    "status": "registered"
                }]
        else:
            record['persistentIdentifiers'].append(
                {
                    "identifier": doi,
                    "scheme": "DOI",
                    "status": "registered"
                }
                )
        record.pop("oarepo:doirequest")
        PersistentIdentifier.create('DOI', doi, object_type='rec',
                                    object_uuid=record.id,
                                    status=PIDStatus.REGISTERED)


    return record


def doi_registration(data, test_mode = False):
    username = current_app.config.get("DOI_DATACITE_USERNAME")
    password = current_app.config.get("DOI_DATACITE_PASSWORD")

    if test_mode:
        url = 'https://api.test.datacite.org/dois'
    else:
        url = 'https://api.datacite.org/dois'


    request = requests.post(url=url, json=data, headers = {'Content-type': 'application/vnd.api+json'}, auth=(username, password))
    if request.status_code != 201:
        raise requests.ConnectionError("Expected status code 201, but got {}".format(request.status_code))





