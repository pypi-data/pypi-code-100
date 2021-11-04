
exclude_field_names = ['IsDeleted', 'RecordTypeId', 'SystemModstamp', 'LastActivityDate', 'LastViewedDate',
                       'LastReferencedDate']


class Field(object):
    def __init__(self, name, label):
        self.name = name
        self.label = label


def get_object_fields(sf, object_name):
    fields = []
    d = getattr(sf, object_name).describe()
    for f in d['fields']:
        if f['name'] in exclude_field_names:
            continue
        fields.append(Field(f['name'], f['label']))
    return fields


def get_object_field_names(sf, object_name):
    field_names = []
    d = getattr(sf, object_name).describe()
    for f in d['fields']:
        if f['name'] in exclude_field_names:
            continue
        field_names.append(f['name'])
    return field_names


def get_salesforce_object_records_from_query_str(sf, query_str, field_names):
    records = []
    datas = sf.query_all(query_str)
    for data in datas['records']:
        record = {}
        for f_name in field_names:
            record[f_name] = data[f_name]
        records.append(record)

    return records;


def get_salesforce_object_records(sf, object_name, addition_query_str=None):
    fields = get_object_fields(sf, object_name)
    field_names = []
    for f in fields:
        field_names.append(f.name)
    records = []
    query_str = "SELECT {} FROM {}".format(','.join(field_names), object_name)
    if addition_query_str:
        query_str = query_str + ' ' + addition_query_str
    return get_salesforce_object_records_from_query_str(sf, query_str, field_names)