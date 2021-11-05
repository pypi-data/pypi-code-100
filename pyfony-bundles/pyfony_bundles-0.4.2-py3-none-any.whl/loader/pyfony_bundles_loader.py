from typing import List
from injecta.module import attribute_loader
from pyfonybundles.Bundle import Bundle
from pyfonybundles.loader import entry_points_reader, pyproject_reader


def get_entry_points():
    entry_points = entry_points_reader.get_by_key("pyfony.bundle")

    for entry_point in entry_points:
        _check_name(entry_point.name, entry_point.value)

    return entry_points


def load_bundles() -> List[Bundle]:
    bundles = []
    bundle_fqns = set()

    for entry_point in get_entry_points():
        bundle_class = entry_point.load()
        bundle_fqn = bundle_class.__module__ + "." + bundle_class.__name__

        if bundle_fqn in bundle_fqns:
            raise Exception(f"Multiple installations of bundle {bundle_fqn} found in your environment")

        bundles.append(bundle_class())
        bundle_fqns.add(bundle_fqn)

    return bundles


def load_bundles_with_current() -> List[Bundle]:
    bundles = load_bundles()

    raw_config = pyproject_reader.read(pyproject_reader.get_path())

    if not _entry_point_defined(raw_config):
        raise Exception('Missing entry point [tool.poetry.plugins."pyfony.bundle"] in pyproject.toml')

    bundle = _load_directly(raw_config)()
    bundles.append(bundle)

    return bundles


def _entry_point_defined(raw_config):
    return (
        "tool" in raw_config
        and "poetry" in raw_config["tool"]
        and "plugins" in raw_config["tool"]["poetry"]
        and "pyfony.bundle" in raw_config["tool"]["poetry"]["plugins"]
    )


def _load_directly(raw_config):
    entry_points = raw_config["tool"]["poetry"]["plugins"]["pyfony.bundle"]

    for name, val in entry_points.items():
        _check_name(name, val)

    return attribute_loader.load_from_string(entry_points["create"])


def _check_name(name: str, value):
    if name != "create":
        raise Exception(f'Unexpected entry point name "{name}" for {value}')
