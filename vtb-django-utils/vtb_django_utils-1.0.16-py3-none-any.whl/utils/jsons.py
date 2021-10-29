import json
from hashlib import md5


def get_json_hash(json_obj):
    return md5(json.dumps(json_obj, sort_keys=True).encode()).hexdigest()
