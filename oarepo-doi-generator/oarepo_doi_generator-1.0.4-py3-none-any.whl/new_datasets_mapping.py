from deepmerge import always_merger
from flask import current_app
from datetime import datetime


def try_name(nlist, record, default=None):
    for name in nlist:
        try:
            return record[name]
        except:
            continue
    else:
        return default


def generate_doi(prefix, pid_type, pid_value):
    return prefix + '/' + pid_type + '.' + pid_value


def schema_mapping(record, pid_type, publisher, test_mode=False):
    prefix = current_app.config.get("DOI_DATACITE_PREFIX")
    new_doi = generate_doi(prefix, pid_type, record['InvenioID'])
    url = record.canonical_url
    for_test_array = url.split('/')

    test_url_prefix = current_app.config.get("DOI_DATACITE_TEST_URL")
    test_url = test_url_prefix + for_test_array[-3] + '/' + for_test_array[-2] + '/' + for_test_array[-1]

    id_data = {}

    always_merger.merge(id_data, {"type": 'dois'})

    attributes = {"event": "publish", "doi": new_doi}

    # creators
    creators = try_name(nlist=['creators'], record=record)
    if creators is None:
        always_merger.merge(attributes, {"creators": [{"name": "Various authors"}]})
    else:
        creators_data = []
        for creator in creators:
            affiliation = []
            if 'affiliation' in creator:
                for aff in creator['affiliation']:
                    if 'en' in aff['title']:
                        affiliation.append(aff['title']['en'])
                    else:
                        affiliation.append(aff['title']['cs'])
            if len(affiliation) > 0:
                creator_data = {"name": creator['fullName'], "affiliation": affiliation}
            else:
                creator_data = {"name": creator['fullName']}
            creators_data.append(creator_data)
        always_merger.merge(attributes, {'creators': creators_data})

    # title
    titles = try_name(nlist=['titles'], record=record)
    if titles == None:
        always_merger.merge(attributes, {"titles": [{"title": {"_": "Unknown"}}]})
    else:
        for title in titles:
            if title['titleType'] == 'mainTitle':
                always_merger.merge(attributes, {"titles": [{'title': title['title']}]})
                break

    # publication year
    if 'dateAvailable' in record:  # should always be in record...
        date = record['dateAvailable']
        date_array = date.split('-')
        always_merger.merge(attributes, {"publicationYear": int(date_array[0])})
    else:
        currentYear = datetime.now().year
        always_merger.merge(attributes, {"publicationYear": currentYear})

    # types
    document_type = "Dataset"  # defaul value
    always_merger.merge(attributes, {"types": {"resourceTypeGeneral": document_type}})

    # url
    if test_mode:
        always_merger.merge(attributes, {"url": test_url})
    else:
        always_merger.merge(attributes, {"url": record.canonical_url})

    # schemaVersion
    always_merger.merge(attributes, {"schemaVersion": "http://datacite.org/schema/kernel-4"})

    # publisher

    always_merger.merge(attributes, {"publisher": publisher})

    attributes = {"attributes": attributes}

    always_merger.merge(id_data, attributes)
    data = {"data": id_data}
    print(data)

    return data






