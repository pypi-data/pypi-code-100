import click
from defektor_api import ApiException

import dfk.config
from dfk.cli import DfkCli


@click.group("campaign")
def cli():
    """🎯 Faulty campaigns."""


@dfk.config.require_login
@cli.command()
@click.argument("campaign", required=True)
def get(id):
    """Print campaign details."""

    try:
        get_campaign_result = DfkCli.api_instance.campaign_get(campaign_id=id)
        click.echo(get_campaign_result)

    except ApiException as api_exception:
        click.echo(f"ERROR: getting campaign for type {type}.\n{api_exception}")


@dfk.config.require_login
@cli.command()
def list():
    """Lists all campaign types."""

    try:
        list_campaigns_result = DfkCli.api_instance.campaign_list()
        click.echo(list_campaigns_result)
    except ApiException as api_exception:
        click.echo(f"ERROR: listing all campaigns.\n{api_exception}")
