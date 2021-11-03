import pkg_resources
import json


def print_config():
    stream = pkg_resources.resource_stream(__name__, 'data/config/config.json')
    config = json.load(stream)
    stream.close()
    for k, v in config.items():
        print(k, '=', v)
