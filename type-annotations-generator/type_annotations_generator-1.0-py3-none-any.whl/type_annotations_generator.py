"type-annotations-generator provides a function for generating type annotations for a object"
from typing import List, Any


def _get_multiples_types(content_types: List[str], pep_604: bool = False) -> str:
    if len(content_types) == 1:
        return content_types[0]
    else:
        type_str = ""
        if not pep_604:
            type_str += "Union["
        for i in content_types:
            if pep_604:
                type_str += i + " | "
            else:
                type_str += i + ", "
        if pep_604:
            return type_str[:-3]
        else:
            return type_str[:-2] + "]"


def generate_annotations(obj: Any, pep_585: bool = False, pep_604: bool = False) -> str:
    "Generate the type annotations for the object"
    if isinstance(obj, list):
        if pep_585:
            type_name = "list"
        else:
            type_name = "List"
        if len(obj) == 0:
            return type_name
        content_types = []
        for i in obj:
            elem_type = generate_annotations(i, pep_585=pep_585, pep_604=pep_604)
            if elem_type not in content_types:
                content_types.append(elem_type)
        return type_name + "[" + _get_multiples_types(content_types, pep_604=pep_604) + "]"
    elif isinstance(obj, dict):
        if pep_585:
            type_name = "dict"
        else:
            type_name = "Dict"
        if len(obj) == 0:
            return type_name
        key_types = []
        value_types = []
        for key, value in obj.items():
            key_type = generate_annotations(key, pep_585=pep_585, pep_604=pep_604)
            if key_type not in key_types:
                key_types.append(key_type)
            value_type = generate_annotations(value, pep_585=pep_585, pep_604=pep_604)
            if value_type not in value_types:
                value_types.append(value_type)
        return type_name + "[" + _get_multiples_types(key_types, pep_604=pep_604) + ", " + _get_multiples_types(value_types, pep_604=pep_604) + "]"
    else:
        return type(obj).__name__
