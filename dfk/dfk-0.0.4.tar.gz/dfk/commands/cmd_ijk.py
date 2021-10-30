import click
from defektor_api.exceptions import ApiException

import dfk.config
from dfk.cli import DfkCli


@click.group("ijk")
def cli():
    """💉 Fault Injektors."""


@dfk.config.require_login
@cli.command()
def list():
    """List installed Injektors."""

    try:
        list_ijk_result = DfkCli.api_instance.ijk_list()
        click.echo(list_ijk_result)
    except ApiException as api_exception:
        click.echo(f"ERROR: retrieving the list of Injektors.\n{api_exception}")
