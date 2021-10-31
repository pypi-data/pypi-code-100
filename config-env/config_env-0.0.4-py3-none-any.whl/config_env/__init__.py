import os
import collections.abc
from dotenv import load_dotenv
load_dotenv()

class ConfigEnv:
    def __init__(self) -> None:
        self.python_env = os.getenv("PYTHON_ENV")
        self.__run()

    def __cleanNullTerms(self, d: dict) -> dict:
        clean = {}
        for k, v in d.items():
            if isinstance(v, dict):
                nested = self.__cleanNullTerms(v)
                if len(nested.keys()) > 0:
                    clean[k] = nested
            elif v is not None:
                clean[k] = v
        return clean

    def __update_dictionary(self, d, u):
        for k, v in u.items():
            if isinstance(v, collections.abc.Mapping):
                d[k] = self.__update_dictionary(d.get(k, {}), v)
            else:
                d[k] = v
        return d

    def __evaluate_environment_variables(self, config: dict) -> dict:
        for key, value in config.items():
            if isinstance(value, dict):
                self.__evaluate_environment_variables(value)
            else:
                config.update({key: os.getenv(value)})
        return config

    def __run(self):
        self.config = {}
        dir = f"{os.getcwd()}/config"
        files = os.listdir(dir)
        filenames = []
        for file in files:
            path = dir + "/" +file
            if os.stat(path).st_size != 0:
                filename = file.split(".")[0].replace("-", "_") + "_config"
                filenames.append(filename)
                exec(f'{filename} = {eval(open(path).read())}')

        if self.python_env == None or "DEFAULT":
            if "default.json" in files:
                exec('self.config.update(default_config)')
            else:
                raise ValueError(f"Missing config file default.json")

        if self.python_env not in [None, "DEFAULT"]:
            if f"{self.python_env.lower().replace('-','_')}.json" in files:
                env_name = f"{self.python_env.lower()}_config"
                self.config = self.__update_dictionary(self.config, eval(env_name))
            else:
                raise ValueError(f"Missing config file {self.python_env.lower()}.json")

        if "custom_environment_variables.json" in files:
            custom_config = self.__evaluate_environment_variables(
                eval("custom_environment_variables_config")
            )
            custom_config_cleaned = self.__cleanNullTerms(custom_config)
            self.config = self.__update_dictionary(self.config, custom_config_cleaned)
        return self.config
    
    def get(self, values):
        values_list = values.split(".")
        if len(values_list) == 1 and not values_list[0]: 
            return self.config
        else:
            command = "self.config"
            for value in values_list:
                command+=f".get('{value}')"
            try:
                return eval(command)
            except:
                return None
