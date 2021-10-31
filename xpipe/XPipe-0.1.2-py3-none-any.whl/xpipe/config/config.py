from . import objects as objects
import yaml
from .tags import Tags
import yaml

def load_config(config_file : str, template=None):
    """Loads a configuration file and return a Config Object which can instantiate the wanted objects.

    Args:
        config_file (str): The path of the yaml config file
    
    Returns:
        Config: A Config object
    """
    Tags.save_tags(yaml) # Set tags constructors and representers
    with open(config_file, "r") as stream:
        yaml_dict = yaml.safe_load(stream)
    return objects.Config("__root__", yaml_dict)

def load_yaml(config_file : str):
    """Loads a configuration file and return a Config Object which can instantiate the wanted objects.

    Args:
        config_file (str): The path of the yaml config file
    
    Returns:
        Config: A Config object
    """
    Tags.save_tags(yaml) # Set tags constructors and representers
    with open(config_file, "r") as stream:
        yaml_dict = yaml.safe_load(stream)
    return yaml_dict

def load_config_from_str(conf: str):
    """Loads a configuration from a string and return a Config Object which can instantiate the wanted objects.

    Args:
        conf (str): A configuration
    
    Returns:
        Config: A Config object
    """
    Tags.save_tags(yaml) # Set tags constructors and representers
    yaml_dict = yaml.safe_load(conf)
    return objects.Config("__root__", yaml_dict)

def to_yaml(conf):
    """Converts a Config object to a yaml string

    Args:
        conf (Config): A configuration

    Returns:
        str: The corresponding yaml string
    """
    return conf._xpipe_to_yaml()

def to_dict(conf):
    """Converts a Config object to a dictionary.

    Args:
        conf (Config): A Config object

    Returns:
        dict: A multi-level dictionary containing a representation ogf the configuration.
    """
    return conf._xpipe_to_dict()