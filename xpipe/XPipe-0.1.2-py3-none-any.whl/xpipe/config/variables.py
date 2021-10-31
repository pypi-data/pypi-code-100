from .node import Node
from .tags import Tags

import os
import string
import yaml

__all__ = ["Variable", "EnvVariable", "Include", "FormatStrVariable", "SingleObjectTag"]


class Variable(Node):

    def __init__(self, name, value):
        super(Variable, self).__init__(name, value)

    def _xpipe_construct(self, name, value):
        self.name = name
        self.value = value

    def set_name(self, name):
        self.name = name
    
    def __call__(self):
        return self.value

    def _xpipe_to_yaml(self, n_indents=0):
        return self.value
    
    def _xpipe_to_dict(self):
        return self.value

    def __eq__(self, o) -> bool:
        if not isinstance(o, Variable): 
            raise Exception(f"Cannot compare {self.__class__} and {o.__class__}")
        return self.value == o.value
    
    def __str__(self) -> str:
        return self.__repr__()
        
    def __repr__(self) -> str:
        return f"{self.name} = Variable({self.value})"


@Tags.register
class EnvVariable(Variable): 
    yaml_tag = u"!env"
    """This class defines a yaml tag.
    It will load an environment variable.
    """

    def __init__(self, value):
        if not isinstance(value, str):
            raise ValueError("Environment variable name must be a string.")
        if value[0] == "$":
            value = value[1:]
        self.var_name = value
        if value in os.environ:
            value = os.environ[value]
        else:
            raise EnvironmentError(f"Environment variable '{value}' is not defined.")
        self.value = value
        super().__init__("", value)
    
    @classmethod
    def from_yaml(cls, loader, node):
        return EnvVariable(node.value)

    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_scalar(data)

    def __repr__(self) -> str:
        return f"EnvVariable(var={self.var_name}, value={self.value})"
    

@Tags.register
class Include(Variable):
    yaml_tag = u"!include"
    builder_class_name = "IncludedConfig"
    
    """
    This class defines a yaml tag.
    It will include another yaml into the current configuration.
    """
    
    def __init__(self, path):
        self.original_path = path
        try:
            path = string.Template(path).substitute(os.environ)
        except KeyError as e:
            raise EnvironmentError(f"Environment variable '{str(e)}' is not defined in include statement.")
        self.path = path
    
    def load(self):
        with open(self.path, "r") as f:
            return yaml.safe_load(f)
    
    @classmethod
    def from_yaml(cls, loader, node):
        return Include(node.value)

    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_scalar(data)

    def __eq__(self, o) -> bool:
        if not isinstance(o, Include): 
            raise Exception(f"Cannot compare {self.__class__} and {o.__class__}")
        return self.original_path == o.original_path

    def __repr__(self) -> str:
        return f"Include(path={self.path})"


@Tags.register
class FormatStrVariable(Variable):
    yaml_tag = u"!f"
    """This class defines a yaml tag. 
    The class will automatically replace substrings $ENV_VAR or ${ENV_VAR} with the corresponding environment variables.
    """

    def __init__(self, value):
        self.original_str = value
        try:
            value = string.Template(value).substitute(os.environ)
        except KeyError as e:
            raise EnvironmentError(f"Environment variable '{str(e)}' is not defined in formatted string.")
        self.str = value
        super().__init__("", value)
    
    @classmethod
    def from_yaml(cls, loader, node):
        return FormatStrVariable(node.value)

    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_scalar(data)

    def __eq__(self, o) -> bool:
        if not isinstance(o, FormatStrVariable): 
            raise Exception(f"Cannot compare {self.__class__} and {o.__class__}")
        return self.original_str == o.original_str

    def __repr__(self) -> str:
        return f"FormatStrVariable(original={self.original_str}, output={self.value})"
    

@Tags.register
class SingleObjectTag(Variable):
    yaml_tag = u"!obj"
    """
    This class defines a yaml tag.
    It will include another yaml into the current configuration.
    """
    
    def __init__(self, class_name):
        self.class_name = class_name
    
    @classmethod
    def from_yaml(cls, loader, node):
        return SingleObjectTag(node.value)

    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_scalar(data)

    def __hash__(self) -> int:
        return hash(id(self))

    def __repr__(self) -> str:
        return f"SingleObjectTag(class_name={self.class_name})"


@Tags.register
class ClassTag(Variable):
    yaml_tag = u"!class"
    """This class defines a yaml tag
    It store a class (not an instance)"""

    def __init__(self, class_name):
        self.class_name = class_name
    
    @classmethod
    def from_yaml(cls, loader, node):
        return ClassTag(node.value)

    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_scalar(data)

    def __eq__(self, o) -> bool:
        if not isinstance(o, ClassTag): 
            raise Exception(f"Cannot compare {self.__class__} and {o.__class__}")
        return self.class_name == o.class_name

    def __repr__(self) -> str:
        return f"ClassTag(class_name={self.class_name})"