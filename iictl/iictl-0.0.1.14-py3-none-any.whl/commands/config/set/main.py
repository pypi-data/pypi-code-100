import click
from iictl.commands.config.main import config

@config.group()
@click.pass_context
def set(ctx):
    pass
