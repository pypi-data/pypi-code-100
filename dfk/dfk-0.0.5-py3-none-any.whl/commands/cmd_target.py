import click
from defektor_api import ApiException

import dfk.config
from dfk.cli import DfkCli


@click.group("target")
def cli():
    """🎯 Faulty targets."""


@dfk.config.require_login
@cli.command()
@click.argument("type", required=True)
def get(type):
    """Print target details."""

    try:
        get_target_result = DfkCli.api_instance.target_get(target=type)
        click.echo(get_target_result)
    except ApiException as api_exception:
        click.echo(f"ERROR: getting target for type {type}.\n{api_exception}")


@dfk.config.require_login
@cli.command()
def list():
    """Lists all target types."""

    try:
        list_targets_result = DfkCli.api_instance.target_list()
        click.echo(list_targets_result)
    except ApiException as api_exception:
        click.echo(f"ERROR: listing all targets.\n{api_exception}")
