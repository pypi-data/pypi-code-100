
from collections import namedtuple
from io import DEFAULT_BUFFER_SIZE
import os
import json 

Field = namedtuple("Field", ["name", "categories", "default_category"])

class Configuration:

    default_configuration = {
	"states": {
		  "READY": {
			   "READING": "Start reading",
		  },
		  "READING": {
			     "DONE": "Finish reading",
			     "READY": "Bring back to to-read state"
		  },
          "DONE": {}
	},
	"default_state": "READY",
	"storage_location": os.path.join(os.environ["HOME"], "Documents"),
	"fields": {
		  "Computer Science": {
			    "default": "Algorithms",
			    "categories": ["Algorithms", "Theory"]
		  }
	},
	"default_field": "Computer Science",
    "metadata_location": os.path.join(os.environ["HOME"], ".papertrack", "metadata.json")
}

    def __init__(self, configuration_dictionary = {}):
        self.configuration_dictionary = configuration_dictionary

    def get_document_states(self):
        if "states" in self.configuration_dictionary:
            return list(self.configuration_dictionary["states"])
        else: 
            return ["READY", "READING", "DONE"]
        
    def get_document_state_transitions(self, state):
        state_definition = self.configuration_dictionary.get("states", self.default_configuration["states"])
        try:
            return list(state_definition[state].items())
        except KeyError:
            raise ValueError("Undefined state requested transitions")
        
    def get_default_document_state(self):
        default_state = self.configuration_dictionary.get("default_state", self.default_configuration["default_state"])
        if default_state not in self.get_document_states():
            raise ValueError("Default state not defined in states")
        return default_state
    
    def get_storage_location(self):
        return self.configuration_dictionary.get("storage_location", self.default_configuration["storage_location"])
    
    def get_fields(self) -> list[Field]:
        fields =  self.configuration_dictionary.get("fields", self.default_configuration["fields"])
        return list(Field(
            name = k, 
            default_category=v.get("default", v.get("categories", ["Default"])[0]),
            categories=v.get("categories", ["Default"])
        ) for k,v in fields.items())

    def get_default_field(self) -> Field:
        default_field_name = self.configuration_dictionary.get("default_field", self.default_configuration["default_field"])
        for field in self.get_fields():
            if field.name == default_field_name:
                return field 
        raise ValueError("Default field in configuration is not contained in fields definition")
    
    def get_metadata_db_location(self) -> str:
        return self.configuration_dictionary.get("metadata_location", self.default_configuration["metadata_location"])
        


def get_configuration(collector_name: str = None) -> Configuration:
    config_dict = {} 
    configuration_directory = os.environ.get("PAPERTRACK_CONFIG_DIR", os.path.join(os.environ["HOME"], ".papertrack"))
    try:
        with open(os.path.join(configuration_directory, "config.json")) as f:
            config_dict = json.loads(f.read())
        if collector_name is not None:
            with open(os.path.join(configuration_directory, f"{collector_name}_config.json")) as f:
                for k,v in json.loads(f.read()).items():
                    config_dict[k] = v
    except:
        pass 
    return Configuration(config_dict)
    