import click
from iictl.commands import cli

@cli.group()
@click.pass_context
def config(ctx):
    pass
