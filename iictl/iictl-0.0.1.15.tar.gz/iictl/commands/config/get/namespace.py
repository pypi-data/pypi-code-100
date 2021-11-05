import click
from iictl.commands.config.get.main import get

@get.command(help='Get current namespace')
@click.pass_context
def namespace(ctx):
    click.echo(ctx.obj['namespace'])

