from typing import Any, Type
import builtins
import json
import yaml
import copy
import sys


class ArgumentParser:
    """A simple argument parser.
    It allows you to specify the type of each expected argument.

        The key-shorts and their values have to be given together.
    For example: if an integer \"offset\" with short being \"o\" has to take the value 100, in the command-line you would type \"-o100\".
    """

    def __init__(self, description: str = "", epilog: str = "", add_help: bool = True):
        """
        Initialisation of the class.

        Parameters
        ----------
        description: string
            description of the program purpose (default is "")
        epilog: string
            last text displayed by help (default is "")
        add_help: bool
            flag to allow help to be provided (default is True)
        """
        self.arguments: dict = {}
        self.__results: dict = {}
        self.description = description
        self.epilog = epilog
        self.add_help = add_help

    def from_json(self, path: str):
        """Use the content of the json file at path to fill list of arguments to parse.

        Parameters
        ----------
        path: string
            Path (absolute or relative) to the json file.
        """
        with open(path, "r") as f:
            data = json.load(f)

        for key, value in data.items():
            short = value["short"]
            type = getattr(builtins, value["type"]) if "type" in value.keys() else str
            required = value["required"] if "required" in value.keys() else True
            description = value["description"] if "description" in value.keys() else ""
            choices = value["choices"] if "choices" in value.keys() else []

            self.add(key, short, type, required, description, choices)

    def from_yaml(self, path: str):
        """Use the content of the yaml file at path to fill list of arguments to parse.

        Parameters
        ----------
        path: string
            Path (absolute or relative) to the json file.
        """
        with open(path, "r") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

        for key, value in data.items():
            short = value["short"]
            type = getattr(builtins, value["type"]) if "type" in value.keys() else str
            required = value["required"] if "required" in value.keys() else True
            description = value["description"] if "description" in value.keys() else ""
            choices = value["choices"] if "choices" in value.keys() else []

            self.add(key, short, type, required, description, choices)

    def add(
        self,
        key: str,
        short: str,
        type: type = str,
        required: bool = True,
        description: str = "",
        choices: list = [],
    ) -> None:
        """Add an argument to parse.

        Parameters
        ----------
        key: string
            key of the new argument. It has to be new.
        short: string
            short representation of the key, without dash.
        type: type
            type of the argument. (default is str)
        required: boolean
            flag that specify if a key is mandatory. (default is True)
        description: str
            description of the argument. (default is "")
        choices: list
            allowed values for the argument. (default is [])
        """
        assert key not in self.arguments.keys(), "Key already used."
        assert isinstance(key, str), "Key must be a string."
        assert isinstance(short, str), "Short must be a string."
        assert isinstance(type, Type), "Type must be a class type."
        assert isinstance(required, bool), "Required must be a boolean."
        assert isinstance(description, str), "Description must be a string."
        assert isinstance(choices, list), "Choices must be a list."
        assert len(short) == 1, "Short must be a single character."

        self.arguments[key] = {
            "short": f"-{short}",
            "required": required,
            "type": type,
            "description": description,
            "choices": [str(c) for c in choices],
        }

    def compile(self, args: list[str]) -> dict:
        """Parse the input arguments with the keys previously specified.

        Parameters
        ----------
        args: list of string
            Arguments to parse

        Returns
        -------
        dict
            dictionnary of compiled arguments keys and values
        """
        if len(args) == 0 and len(self.arguments) != 0 and self.add_help:
            print("To get help, use -h or --help command line options.")
            exit()

        if len(args) == 1 and args[0] in ["--help", "-h"] and self.add_help:
            self.show_help()
            exit()

        keys = [key for key, _ in self.arguments.items()]
        shorts = [value["short"] for _, value in self.arguments.items()]

        for arg in args:
            if arg[:2] in shorts:
                key = keys[shorts.index(arg[:2])]
                choices = self.arguments[key]["choices"]
                if choices:
                    if arg[2:] in choices:
                        self.__results[key] = arg[2:]
                    else:
                        print(f"Provided {key} not in {choices}")
                        exit()
                else:
                    self.__results[key] = arg[2:]

        for key in keys:
            if self.arguments[key]["required"] and key not in self.__results.keys():
                print(
                    f"{__class__.__name__} error: '{key}' command line argument is required. Add it using '{self.arguments[key]['short']}value'"
                )
                exit()

        return {key: self.__getitem__(key) for key in self.arguments}

    def show_help(self):
        """Displays help for the argument to pass on the command-line."""
        n_arg = len(self.arguments)

        if n_arg != 0:
            length_str = max([len(arg) for arg in self.arguments.keys()])
            script_name = sys.argv[0]

            arg_strs: list[str] = []
            for key, value in self.arguments.items():
                if value["required"]:
                    arg_strs.append(f"{value['short']}{key}")

            for key, value in self.arguments.items():
                if not value["required"]:
                    arg_strs.append(f"[{value['short']}{key}]")

            print(f"usage: {script_name} {' '.join(arg_strs)}\n")
            if self.description:
                print(f"{self.description}\n")

            print(f"positional arguments:")
            for key, value in self.arguments.items():
                if value["required"]:
                    print(f"{value['short']}: {key:{length_str+10}s} {value['type']}")
                    print(f"\t{value['description']}")
                    if value["choices"]:
                        print(f"\tPossible values are {value['choices']}.")

            print("")
            print(f"optional arguments:")
            for key, value in self.arguments.items():
                if not value["required"]:
                    print(f"{value['short']}: {key:{length_str+10}s} {value['type']}")
                    print(f"\t{value['description']}")
                    if value["choices"]:
                        print(f"\tPossible values are {value['choices']}")

            print("-h, --help\n\tshow this help message and exit")

            if self.epilog:
                print(f"\n{self.epilog}")

    def to_json(self, filename: str):
        """Export the arguments dictionnary to a json file.

        Parameters
        ----------
        filename: string
            name of the json file to send dictionnary values to.
        """
        args = copy.deepcopy(self.arguments)

        for key in args.keys():
            args[key]["type"] = args[key]["type"].__name__
            args[key]["short"] = args[key]["short"][1]

        with open(filename, "w") as f:
            json.dump(args, f)

    def to_yaml(self, filename: str):
        """Export the arguments dictionnary to a yaml file.

        Parameters
        ----------
        filename: string
            name of the json file to send dictionnary values to.
        """
        args = copy.deepcopy(self.arguments)

        for key in args.keys():
            args[key]["type"] = args[key]["type"].__name__
            args[key]["short"] = args[key]["short"][1]

        with open(filename, "w") as f:
            yaml.dump(args, f)

    def __getitem__(self, key: str) -> Any:
        """Returns the value (with the right type) associated with a given key. If the key correspond to an optional argument that has not been given, the method returns None.

        Parameters
        ----------
        key: string
            key to retrieve the value for.

        Returns
        -------
        Any
            The value related to the given key, with the right type.

        """
        assert key in self.arguments, f'Key "{key}" not found.'

        value_type = self.arguments[key]["type"]

        if key not in self.__results:
            return value_type()

        try:
            if value_type == bool:
                return value_type(eval(self.__results[key]))
            return value_type(self.__results[key])
        except ValueError as e:
            print(
                f"{__class__.__name__} error with '{key}': {e}. Using default constructor value."
            )
            return value_type()
