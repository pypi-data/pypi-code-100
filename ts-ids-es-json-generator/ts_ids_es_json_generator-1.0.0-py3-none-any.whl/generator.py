import argparse
import json
from pathlib import Path
from typing import Union

import jsonref
from pydash import (
    get,
    reduce_right
)
from pydash.objects import merge


def create_dict_from_keys(dot_connected_keys: str, item: dict) -> dict:
    """Recursively create a dict based on the provided keys

    Args:
        dot_connected_keys (str): dot-connected key string
        item (dict): the value of the last key

    Returns:
        dict: a nested object with each key nested inside one another

    Example:
        input: ("a.b.c", {})
        output: {
            "a": {
                "properties": {
                    "b": {
                        "properties": {
                            "c": {
                                "type": "nested"
                            }
                        }
                    }
                }
            }
        }

        See more in the unit tests
    """
    key_dict = {}
    keys = dot_connected_keys.split(".")

    last_key = keys.pop(-1)
    key_dict[last_key] = {"type": "nested"}
    if item:
        key_dict[last_key]["properties"] = generate_es_mapping(item)

    return_dict = reduce_right(
        keys,
        lambda d, k: {k: {"properties": d}},
        key_dict
    )

    return return_dict


def find_array_object(schema: dict, parent_key: str = "") -> dict:
    """Creates a specially designed dict containing all nested fields based on the provided schema

    Args:
        schema (dict): the main schema body in "properties" field in a standard JSON schema file, with all JSON pointers dereferenced
        parent_key (str, optional): parent key for key concatenation. This is a special annotation for array of object field inside an object. Defaults to "".

    Returns:
        dict: specially designed dict which contains all fields that should be defined "nested" in elasticsearch.json

    Example:
        See unit tests
    """
    array_object = {}

    for key, item in schema.items():
        concat_key = key
        if parent_key:
            concat_key = f"{parent_key}.{key}"

        if get(item, "type") == "array" and get(item, "items.type") == "object":
            array_object[concat_key] = {}
            array_object[concat_key].update(
                find_array_object(get(item, "items.properties"))
            )

        # need to keep looking for array of objects inside object
        elif get(item, "type") == "object":
            tmp_dict = find_array_object(get(item, "properties"), concat_key)
            if tmp_dict:
                array_object.update(tmp_dict)

    return array_object


def generate_es_mapping(array_object_dict: dict) -> dict:
    """Generate elasticsearch mapping based on the dict created by "find_array_object" function

    Args:
        array_object_dict (dict): dict created by "find_array_object" function

    Returns:
        dict: elasticsearch mapping dict

    Example:
        See unit tests
    """
    mapping = {}
    for key, item in array_object_dict.items():
        mapping = merge(mapping, create_dict_from_keys(key, item))

    return mapping


def create_elasticsearch(schema_json: Union[dict, str]) -> dict:
    """Create an ElasticSearch mapping from a JSON Schema with nested properties

    Args:
        schema_json (dict|str) -- The schema as a dict or JSON string. JSON pointers in the schema will be dereferenced using `jsonref`.

    Returns:
        es_mapping (dict) -- the default Tetra ElasticSearch mapping including all nested properties, and `datacubes` in nonSearchableFields if present.
    """
    if isinstance(schema_json, str):
        schema_json = jsonref.loads(schema_json)
    elif isinstance(schema_json, dict):
        # Ensure JSON pointers are dereferenced
        schema_json = jsonref.loads(jsonref.dumps(schema_json))
    else:
        raise TypeError(
            "The elasticsearch mapping generator expects a dict or JSON string as input")

    try:
        schema_json_properties = schema_json["properties"]
    except KeyError as e:
        raise KeyError(
            "There is no 'properties' member in this schema.") from e

    non_searchable_fields = []
    if "datacubes" in schema_json_properties:
        schema_json_properties.pop("datacubes")
        non_searchable_fields.append("datacubes")

    array_object_dict = find_array_object(schema_json_properties)

    return {
        "mapping": {
            "properties": generate_es_mapping(array_object_dict),
            "dynamic_templates": []
        },
        "nonSearchableFields": non_searchable_fields
    }


def create_elasticsearch_in_dir(ids_dir: Path) -> None:
    """Create an ElasticSearch mapping from a JSON Schema in the given folder

    This function produces an `elasticsearch.json` file in `ids_dir` containing the generated ElasticSearch mapping JSON

    Args:
        ids_dir (Path) -- The path to a folder containing the JSON Schema `schema.json`

    Returns:
        None
    """
    schema_json_str = (ids_dir / "schema.json").read_text("UTF-8")

    print("Generating elasticsearch.json")
    es_json = create_elasticsearch(schema_json_str)

    print("Saving elasticsearch.json to disk")

    with open(ids_dir / "elasticsearch.json", "w") as fout:
        json.dump(es_json, fout, indent=2)

    print("Finished successfully")
