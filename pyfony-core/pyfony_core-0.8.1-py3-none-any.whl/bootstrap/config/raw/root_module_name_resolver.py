import os


def resolve(raw_config):
    if "root_module_name" in raw_config:
        return raw_config["root_module_name"]

    return _resolve_root_module_name()


def _resolve_root_module_name():
    root_modules = os.listdir(f"{os.getcwd()}/src")

    if len(root_modules) != 1:
        raise Exception(f"Cannot resolve root module from 'src' folder, it must contain exactly 1 root module, found: {root_modules}")

    return root_modules[0]
