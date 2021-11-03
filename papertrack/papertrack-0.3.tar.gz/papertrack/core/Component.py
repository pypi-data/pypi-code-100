

import collections
from typing import Collection
from functools import partial
import os 

_DOWNLOADERS = [] 
_COLLECTORS = []
_VIEWERS = [] 

def register_downloader(cls):
    _DOWNLOADERS.append(cls)
    return cls


def register_collector(cls):
    _COLLECTORS.append(cls)
    return cls


def register_viewer(cls):
    _VIEWERS.append(cls)
    return cls

def simple_ask_fn(name, param_type, description, choices: list) -> str:
    value = None
    while value is None:
        if choices and len(choices) > 0:
            print("%s (%s)" % (name, description))
            for i,c in enumerate(choices):
                print(" > %d %s" % (i+1, c))
            try:
                value = int(input("Selection >"))
                value = choices[value - 1]
            except:
                value = None
        else:
            print("%s (%s)" % (name, description),)
            if param_type == "list":
                resulting_list = [] 
                item = None
                while item != "q":
                    item = input("Enter value for the list (enter 'q' and press ENTER to finish) >")
                    if item != "q":
                        resulting_list.append(item)
                value = resulting_list
            else:
                value = input("> ")
    return value


def _convert_type(value, type):
    if type in ["str", "string"]:
        return str(value)
    elif type in ["int", "integer", "number"]:
        return int(value)
    elif type in ["bool", "boolean"]:
        return bool(value)
    elif type == "list":
        return value
    else:
        raise TypeError("Wrong type")

def get_component_class(name, type):
    components = None
    if type == "downloader":
        components = _DOWNLOADERS
    elif type == "collector":
        components = _COLLECTORS
    elif type == "viewer":
        components = _VIEWERS
    else:
        raise TypeError("Wrong type of component. Contact developer to resolve this.")
    result = None
    for component in components:
        if component.name == name:
            result = component
    if not result:
        raise ValueError("Component with name %s not found" % name)
    return result

def _get_component_instance(name, ask_param_fn, type, **params):
    result = get_component_class(name, type)
    config = {}
    for param, definition in result.params.items():
        if "default" not in definition and param not in params:
            print("%s has no default, asking..." % param)
            value = ask_param_fn(
                param, 
                definition.get("type", "string"), 
                definition.get("description", ""), 
                definition.get("choices", [])
            )
            config[param] = _convert_type(value, definition.get("type", "string"))
        elif "default" in definition and param not in params:
            if os.environ.get("PAPERTRACK_ASK_ON_DEFAULT", "0") == "1":
                print("%s has default, asking..." % param)
                value = ask_param_fn(
                    param, 
                    definition.get("type", "string"), 
                    definition.get("description", ""), 
                    definition.get("choices", [])
                )
                config[param] = _convert_type(value, definition.get("type", "string"))
            else:
                print("%s has default=%s" % (param, definition["default"]))
                config[param] = _convert_type(definition["default"], definition["type"])
        else:
            print("%s = %s" % (param, params[param]))
            config[param] = _convert_type(params[param], definition.get("type", "str"))
    return result(**config)
    
get_downloader_instance = partial(_get_component_instance,  type="downloader")
get_collector_instance = partial(_get_component_instance,  type="collector")
get_viewer_instance = partial(_get_component_instance,  type="viewer")

def get_all_components(type):
    if type == "downloader":
        return _DOWNLOADERS
    elif type == "collector":
        return _COLLECTORS
    elif type == "viewer":
        return _VIEWERS
    else:
        raise TypeError("Wrong type")
