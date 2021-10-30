import ipaddress
import json
from json import JSONDecodeError
from pathlib import Path

import click
import defektor_api
from defektor_api import Configuration
from jsonschema import validate, ValidationError
from python_jsonschema_objects import ObjectBuilder

from dfk.cli import DfkCli

CONFIG_DATA = None
CONFIG_PATH = Path.home().joinpath(".config").joinpath("dfk").joinpath("config")

config_schema = {
    "title": "Config",
    "type": "object",
    "properties": {
        "address": {"type": "string"}
    },
    "required": ["address"]
}


def get_config():
    try:
        with open(str(CONFIG_PATH)) as config_file:
            config_data = json.loads(config_file.read().replace('\n', ''))

        validate(config_data, config_schema)

        CONFIG_DATA = config_data
    except (JSONDecodeError, ValidationError) as schema_format_exception:
        click.echo(f"ERROR: error in configuration file.\n{schema_format_exception}")
        exit(1)
    except IOError as file_read_exception:
        click.echo(f"ERROR: reading configuration file.\n{file_read_exception}")
        exit(1)
    except ValueError as address_format_exception:
        click.echo(f"ERROR: address not valid in configuration file.\n{address_format_exception}")
        exit(1)

    config: Configuration = Configuration()
    if CONFIG_DATA['address']:
        config.host = CONFIG_DATA['address']

    return config


def write_config(address: str):
    objectBuilder = ObjectBuilder(config_schema)
    ns = objectBuilder.build_classes()
    Config = ns.Config

    dfkConfig = Config(address=address)
    jsonConfig = dfkConfig.serialize()

    with open(str(CONFIG_PATH), "w") as file:
        file.write(jsonConfig)

    click.echo(f"{jsonConfig} written into {CONFIG_PATH}")


def require_login(func):
    if not Path.exists(CONFIG_PATH):
        click.echo("ERROR: Please login!\n$ dfk login")
        exit(1)

    api_client = defektor_api.ApiClient(get_config())
    DfkCli.api_instance = defektor_api.DefaultApi(api_client)
