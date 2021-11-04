
import uuid
import json
import datetime


"""
Module to handle json objects
"""


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    else:
        return str(obj)

def json_deserial(json_dict):
    """JSON deserializer for objects not serializable by default json code"""
    for (key, value) in json_dict.items():
        try:
            json_dict[key] = datetime.datetime.fromisoformat(json_dict[key])
        except:
            pass
    return json_dict


def dumps(value):
    # Same as json.dumps but converts dates


    return json.dumps(value, indent=4, sort_keys=True, default=json_serial)

def loads(value):
    # Same as json.loads but handles dates

    loaded_dict = json.loads(value, object_hook=json_deserial)

    return loaded_dict


def dump(value, file):
    # Writes json to file
    json.dump(value, file, default = json_serial, ensure_ascii=False, indent=4)

    return

def load(file):
    # Load json from file
    data = json.load(file, object_hook=json_deserial)
    return data



def flatten(y):
    # Converts json record in list of RDF
    out = []

    def flatten(x, parent_object_type = None, parent_object_id = None, parent_key = None):
        
        if type(x) is dict:
            
            # Check if value is an entity
            if x.get('@type', None):
                child_object_type = x.get('@type', None)
            else:
                child_object_type = ('schema:unknown')

            if x.get('@id', None):
                child_object_id = x.get('@id', None)
            else:
                child_object_id = str(uuid.uuid4())


            child_object = {
                '@type': child_object_type,
                '@id': child_object_id
            }

            for k in x.keys():
                if k not in ['@type', '@id']:
                    flatten(x.get(k, None), child_object_type, child_object_id, k)
        
            # Assign kid as value to parent
            if parent_object_type and parent_object_id:
                record = {
                    '@type': parent_object_type,
                    '@id': parent_object_id,
                    'key': parent_key,
                    'value': child_object
                    }
                out.append(record)
            

        elif type(x) is list:
            for a in x:
                flatten(a, parent_object_type, parent_object_id, parent_key)
        else:
            record = {
                '@type': parent_object_type,
                '@id': parent_object_id,
                'key': parent_key,
                'value': x
                }
            if parent_key and not parent_key.startswith('@'):
                out.append(record)

    flatten(y)
    return out


def compact(record):
    # Remove empty lists and value, converts lists of 1 to unit

    def _simpl(record):

        if isinstance(record, dict):
            new_record = {}
            for key in record:
                value = _simpl(record[key])
                if value: 
                    new_record[key] = value

        elif isinstance(record, list):
            new_record = []

            for i in record:
                new_record.append(_simpl(i))
            
            if len(new_record) == 1:
                new_record = new_record[0]

        else:
            new_record = record

        return new_record

    return _simpl(record)