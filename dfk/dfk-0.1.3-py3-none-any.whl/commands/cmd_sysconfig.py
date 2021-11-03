import click
from defektor_api import ApiException

import dfk.config
from dfk.cli import DfkCli


@click.group("sysconfig")
def cli():
    """💻 System configuration."""


@dfk.config.require_login
@cli.command()
def list():
    """Lists all system configurations."""

    try:
        list_system_config_results = DfkCli.api_instance.system_config_list()
        click.echo(list_system_config_results)
    except ApiException as api_exception:
        click.echo(f"ERROR: listing all campaigns.\n{api_exception}")
