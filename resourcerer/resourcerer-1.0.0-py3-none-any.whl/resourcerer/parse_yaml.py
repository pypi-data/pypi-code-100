import yaml


def get_yaml_obj(path=None):
    if path:
        resources_yaml_path = path
    else:
        resources_yaml_path = "resources.yaml"
    with open(resources_yaml_path, "r") as f:
        resources = yaml.full_load(f)
    return resources
