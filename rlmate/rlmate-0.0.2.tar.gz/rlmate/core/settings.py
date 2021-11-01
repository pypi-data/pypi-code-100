import git
import os
from pathlib import Path


def get_repo_path():
    repo = git.Repo(".", search_parent_directories=True)
    return repo.working_tree_dir


# Dictionary of settings with default value:
d = {"path_to_experiments": "./", "threads": 1}


def add_to_dictionary(dictionary, line, delimiter, line_number):
    if line.startswith("bot_id") or line.startswith("chat_id"):
        return True
    try:
        key, value = line.split(delimiter)
    except:
        print("line " + str(line_number) + ": " + line + " does not fit convention")
        return False
    try:
        t = type(d[key])
    except:
        print("line " + str(line_number) + ": " + key + " setting does not exist")
        return False
    try:
        dictionary[key] = t(value)
    except:
        print(
            "line "
            + str(line_number)
            + ": "
            + value
            + " could not be casted to needed type ("
            + t
            + ")"
        )
        return False

    return True


def load():
    """checks whether the repo has a .hermes_settings file
    loads the given settings if there os one is
    uses the default settings else"""
    path = get_repo_path()

    settings_file = path + "/.hermes_settings"
    if os.path.exists(settings_file):
        with open(settings_file, "r") as f:
            for i, line in enumerate(f):
                line = line.replace(" ", "")
                line = line.replace("\n", "")
                add_to_dictionary(d, line, ":", i)

    relative_path = d["path_to_experiments"]
    absolute_path = Path(get_repo_path())
    d["path_to_experiments"] = str(Path.joinpath(absolute_path, relative_path))
    print(d["path_to_experiments"])
    return d


def create_settings_file():
    """checks whether the repo has a .hermes_settings file
    gives an error if there is one
    else creates an hermes_settings file with the default values"""
    path = get_repo_path()

    settings_file = path + "/.hermes_settings"

    if os.path.exists(settings_file):
        print("Error: file does already exist")
    else:
        with open(settings_file, "w") as f:
            for i, k in enumerate(d):
                s = str(k) + ":" + str(d[k])
                if i != len(d):
                    s += "\n"
                f.write(s)
