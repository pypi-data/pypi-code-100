from .node import Node
import importlib
from .utils import is_object, is_objects_list, is_var, is_list, is_config
from . import variables as variables
from collections.abc import Mapping

__all__ = ["Config", "SingleObject", "ObjectsList", "Parameters"]

class Config(Node, Mapping):

    def __init__(self, name, config_dict):
        self._xpipe_config_dict = config_dict
        self._xpipe_properties = {}
        Node.__init__(self, name, config_dict)

    def _xpipe_check_valid(self, name, config_dict):
        if name != "__root__":
            super(Config, self)._xpipe_check_valid(name, config_dict)
        return True

    def _xpipe_construct(self, name, sub_config):
        for name, sub_config in sub_config.items():
            # self.set_node(name, sub_config)
            node = construct(name, sub_config)
            self._xpipe_properties[name] = node

    def _xpipe_to_yaml(self, n_indents=0):
        r = []
        for key, value in self.items():
            el = "  " * n_indents
            el += f"{key}: "
            if isinstance(value, Config) or isinstance(value, ObjectsList) or isinstance(el, List):
                el += "\n"
            el += f"{value._xpipe_to_yaml(n_indents=n_indents + 1)}"
            r += [el]
        joiner = "\n\n" if self._xpipe_name == "__root__" else "\n"
        return joiner.join(r)

    def _xpipe_to_dict(self):
        return { k: v._xpipe_to_dict() for k, v in self.items() }
    
    def __getattribute__(self, prop: str):
        properties = super(Node, self).__getattribute__("_xpipe_properties")
        if prop in properties:
            return properties[prop]
        else:
            try: 
                return super(Node, self).__getattribute__(prop)
            except:
                raise AttributeError(f"'{self._xpipe_name}' ({self.__class__.__name__}) does not have an attribute '{prop}'")

    def __getitem__(self, prop):
        if prop in self._xpipe_properties:
            return self._xpipe_properties[prop]
        else:
            raise AttributeError(f"'{self._name}' ({self.__class__.__name__}) does not have an attribute '{prop}'")

    def __contains__(self, prop):
        return prop in self._xpipe_properties
    
    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Config): 
            raise Exception(f"Cannot compare {self.__class__} and {o.__class__}")
        return self._xpipe_properties == o._xpipe_properties

    def __len__(self):
        return len(self._xpipe_properties)

    def __iter__(self):
        for prop in self._xpipe_properties.keys():
            yield prop
    
    def __repr__(self) -> str:
        return f"Config(len={len(self)})"

class IncludedConfig(Config):

    def __init__(self, name, config_dict):
        conf = config_dict.load()
        self._xpipe_path = config_dict.path
        super(IncludedConfig, self).__init__(name, conf)
    
    def __repr__(self) -> str:
        return f"IncludedConfig(len={len(self)}, path={self._xpipe_path})"

class Parameters(Config):
    """Create parameters of an object from a dict 'param_dict' of format 
    { 
    object_param_name: {class_name: obj_param_dict},
    variable_param_name: value,
    objects_list_param_name: [class_name: obj_param_dict, ...]
    }

    Args:
        param_dict (dict): Dictionary of the parameters
    """

    def __init__(self, class_name, param_dict):
        super(Parameters, self).__init__(class_name, param_dict)
        
    def _xpipe_construct(self, class_name, params_dict):
        super(Parameters, self)._xpipe_construct(class_name, params_dict)

    def _xpipe_check_valid(self, class_name, param_dict):
        return True

    def __repr__(self) -> str:
        return f"Parameters({len(self)})"

    def unwarp(self):
        return {param_name: (param_value() if not isinstance(param_value, Config) else param_value) for param_name, param_value in self._xpipe_properties.items()}

class IncludedParameters(Parameters):

    def __init__(self, class_name, param_dict):
        super(IncludedParameters, self).__init__(class_name, param_dict)

    def _xpipe_construct(self, class_name, params_dict):
        conf = params_dict.load()
        self._xpipe_path = params_dict.path
        return super(IncludedParameters, self)._xpipe_construct(class_name, conf)


class List(Node):

    def __init__(self, name, config_dict):
        self._xpipe_elements = []
        super(List, self).__init__(name, config_dict)
    
    def _xpipe_construct(self, name, config_dict):
        for element in config_dict:
            constructed_el = construct(name, element)
            self._xpipe_elements += [constructed_el]

    def _xpipe_check_valid(self, name, config_dict):
        return True

    def _xpipe_to_dict(self):
        return [el._xpipe_to_dict() for el in self._xpipe_elements]

    def _xpipe_to_yaml(self, n_indents=0):
        r = "\n"
        
        for el in self._xpipe_elements:
            indents = "  " * (n_indents + 1)
            yaml_el = el._xpipe_to_yaml(n_indents = n_indents + 2)
            if isinstance(el, Config) or isinstance(el, ObjectsList) or isinstance(el, List):
                yaml_el = f"\n{yaml_el}"
            r += f"{indents}- {yaml_el}\n"
        return r

    def __getitem__(self, index):
        from .variables import Variable
        element = self._xpipe_elements[index]
        if isinstance(element, Variable):
            return element()
        else:
            return element

    def __len__(self):
        return len(self._xpipe_elements)

    def __call__(self):
        return [el for el in self]

    def __repr__(self) -> str:
        return f"[{', '.join(map(lambda x: str(x), self))}]"
    

class SingleObject(Node):
    """Allow the instantiation of an object defined in a yaml configuration file.

    Args:
        name (str): Name of the object
        config_dict (dict): A dictionary defining the object (class name and parameters).
    """

    def __init__(self, name, config_dict):
        super(SingleObject, self).__init__(name, config_dict)

    def _xpipe_check_valid(self, name, config_dict):
        return True

    def _xpipe_construct(self, name, config_dict):
        self._name = name
        object, self._params = list(config_dict.items())[0]
        self._class_name = object.class_name
        split_index = len(self._class_name) - self._class_name[::-1].index(".") # Get index of the last point
        self._module, self._class_name = self._class_name[:split_index-1], self._class_name[split_index:]
        if not isinstance(self._params, variables.Include):
            self._params = Parameters(self._class_name, self._params)
        else:
            self._params = IncludedParameters(self._class_name, self._params)

    def _xpipe_to_yaml(self, n_indents=0):
        indents = "  " * (n_indents)
        r = f"{indents}{variables.SingleObjectTag.yaml_tag} {self._module}.{self._class_name}:\n"
        r += self._params._xpipe_to_yaml(n_indents=n_indents + 1)
        return r

    def _xpipe_to_dict(self):
        return {
            f"obj:{self._module}.{self._class_name}": self._params._xpipe_to_dict()
        }
        
    def __call__(self, **args):
        module = importlib.import_module(self._module)
        class_object = getattr(module, self._class_name)
        params = self._params.unwarp()
        return class_object(**params, **args)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, SingleObject): 
            raise Exception(f"Cannot compare {self.__class__} and {o.__class__}")
        return self._class_name == o._class_name and self._params == o._params

    def __repr__(self) -> str:
        return f"SingleObject(name={self._class_name})"


class ObjectsList(Node):
    """Create a list of SingleObject from a yaml configuration file.

    Args:
        name (str): Name of the list of objects
        config_dict (list<dict>): A list of dictionaries which defines the objects list.
    """
    
    def __init__(self, name, config_dict):
        super(ObjectsList, self).__init__(name, config_dict)

    def _xpipe_check_valid(self, name, config_dict): 
        super(ObjectsList, self)._xpipe_check_valid(name, config_dict)

    def _xpipe_construct(self, name, config_dict):
        self._name = name
        self._objects = [SingleObject(name, obj_dict) for obj_dict in config_dict]
        
    def _xpipe_to_yaml(self, n_indents=0):
        r = []
        for object in self._objects:
            el = "  " * (n_indents + 1)
            el += f"- {object._xpipe_to_yaml(n_indents=n_indents + 1)}"
            r += [el]
        return "\n".join(r)
    
    def _xpipe_to_dict(self):
        return [ obj._xpipe_to_dict() for obj in self._objects ]

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, ObjectsList): 
            raise Exception(f"Cannot compare {self.__class__} and {o.__class__}")
        return self._objects == o._objects

    def __getitem__(self, i):
        return self._objects[i]

    def __call__(self, **args):
        return [obj(**args) for obj in self._objects]


def get_node_type(conf):
    """Detect the object that can build the tree

    Args:
        conf (dict): The configuration dictionary

    Returns:
        Node | Variable: The object type
    """
    if isinstance(conf, variables.Variable):
        # Return the builder class defined by the variable or None if none is needed
        builder_name = getattr(conf.__class__, "builder_class_name", None)
        return globals()[builder_name] if builder_name is not None else None

    builder_checkers = [
        (SingleObject, is_object),
        (ObjectsList, is_objects_list),
        (List, is_list), 
        (variables.Variable, is_var), 
        (Config, is_config)
    ]
    for node_type, can_build in builder_checkers:
        if can_build(conf):
            return node_type
    raise Exception(f"Configuration cannot be parsed: {conf}")


def construct(name, config_dict):
    """Build a tree from a dictionary

    Args:
        name (str): Name of the node
        config_dict (dict): The dictionary

    Returns:
        Node | Variable: The build tree element
    """
    NodeType = get_node_type(config_dict)

    if NodeType is not None: 
        node = NodeType(name, config_dict)
    else: 
        # Node is already built by a yaml tag
        node = config_dict
        node.set_name(name)
    return node