from pkg_resources import resource_stream

from ruamel.yaml import YAML


def get_yaml(stream_args):
    with resource_stream(*stream_args) as stream:
        yaml = YAML()
        return yaml.load(stream)


def get_config():
    stream_args = ["roseta", "data/config.yml"]
    config_data = get_yaml(stream_args)
    return config_data


def get_all_city():
    stream_args = ["roseta", "data/city.yml"]
    city_data = get_yaml(stream_args)
    city_list = []
    for data_item1 in city_data["行政区"].keys():
        if data_item1 in ["直辖市", "特别行政区"]:
            for data_item2 in city_data["行政区"][data_item1]:
                city_list.append(data_item1 + "/" + data_item2)
        else:
            for data_item2 in city_data["行政区"][data_item1].keys():
                for data_item3 in city_data["行政区"][data_item1][data_item2].keys():
                    for data_item4 in city_data["行政区"][data_item1][data_item2][data_item3]:
                        city_list.append(data_item1 + "/" + data_item2 + "/" + data_item3 + "/" + data_item4)
    return city_list
