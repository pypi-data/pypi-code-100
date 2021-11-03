import click

from dfk.config import write_config


@click.command("login")
@click.argument("address", required=True)
def cli(address):
    """🔑 defektor login."""

    write_config(str(address))
