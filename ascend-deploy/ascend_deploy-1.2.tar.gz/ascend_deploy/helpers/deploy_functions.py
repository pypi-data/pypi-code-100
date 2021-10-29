import configparser
import json
import logging
import os
import re
from pathlib import Path

from ascend.sdk.client import Client


def build_logging(level_string):
    """"
    Setting up a logger at this level, as we can request to run it with more details and the likes, plus gives us information on imported packages 
    ## NOTE Not so sure if ascend's SDK has any logging but this just looks nicer
    """
    logging.basicConfig(
        format="[%(asctime)s] [%(levelname)s] [%(message)s]", level=level_string.upper()
    )


def read_file_as_string(file_location) -> str:
    """
    Reads in a python file as a string
    """
    if not os.path.isfile(file_location):
        raise Exception(f"File {file_location} does not exist")

    with open(file_location, "r") as file:
        file_string = file.read()

    return file_string


def apply_config_to_string(
    file_string: str, environment: str, config_location: str,
) -> str:
    """
    Given a string and an environment, apply the rules given by the triggers in the config
    file to the string
    """
    # Loading in the config
    with open(Path(config_location)) as file:
        config = json.load(file)

    # Selecting the environment config. For each action in that config, apply the changes if
    # the trigger exists
    if environment not in config:
        raise Exception(f"Environment: {environment} is not valid")

    environment_config = config[environment]

    # Components are always seperated with a blank line. We use this to our advantage when editing
    # the python script
    components = file_string.split("\n\n")

    updated_components = []
    for component in components:

        # Running through actions in the environment config and applying them
        for action in environment_config:

            # If the trigger is in the component, and the component is in the action, apply the
            # replace
            if action["trigger"] in component and any(
                c in component for c in action["components"]
            ):
                for replace_string in action["replace_from"]:
                    component = re.sub(replace_string, action["replace_to"], component)

        # Adding component to updated_components
        updated_components.append(component)

    # Joining components back together
    file_string = "\n\n".join(updated_components)
    return file_string


def client_setup(_instance) -> Client:
    """
    Sets up all the required settings for an Ascend client object
    """
    # ----------------------------------------------------------------------------#
    # Reading in credentials from config

    # Loading in the config
    #configuration_file_location = Path("./config.json")
    #with open(configuration_file_location) as file:
    #    config = json.load(file)

    #credentials = config["credentials"]

    # -------------------------------------------------------------------------------#
    # When creating a client, Ascend assumes that the credentials are located inside
    # the file ~\ascend\credentials. If the credentials do not exist, this function
    # creates them

    # Getting the Ascend credentials from the ascend configuration, as documented on https://developer.ascend.io/docs/python-sdk
    ascend_configurations_path = f"{Path.home()}/.ascend/credentials"

    if os.path.isfile(ascend_configurations_path) is False:

        ascend_config = configparser.ConfigParser()
        ascend_config[credentials["environment"]] = {
            "ascend_access_key_id": "Your Ascend.io Access Key ID",
            "ascend_secret_access_key": "Your Ascend.io Access Secret Access Key",
        }
        with open(ascend_configurations_path, "w") as configfile:
            ascend_config.write(configfile)

        raise Exception(
            f"Ascend configuration not found! Please update the file at {ascend_configurations_path} with your credentials, then run this script again!"
        )
    else:
        ascend_config = configparser.ConfigParser()
        ascend_config.read(os.path.expanduser(ascend_configurations_path))

    access_id = ascend_config.get(_instance, "ascend_access_key_id")
    secret_key = ascend_config.get(_instance, "ascend_secret_access_key")

    # -------------------------------------------------------------------------------#
    # Calling the Client object without passing credentials forces it to search for
    # the credentials. This was already setup in the previous steps
    # client = Client(hostname=credentials[_instance])
    client = Client(hostname='{}.ascend.io'.format(_instance), access_key=access_id, secret_key=secret_key)

    return client
