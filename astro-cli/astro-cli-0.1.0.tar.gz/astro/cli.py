import click

from astro.cmd import global_options, moon, twilight, whereis
from astro.lib import Astro


@click.group()
@global_options
@click.pass_context
def cli(ctx, **kwargs):
    ctx.obj = Astro.from_args(**kwargs)
    click.echo(f"Location: {ctx.obj.location}", err=True)
    click.echo(err=True)


cli.add_command(moon.moon)
cli.add_command(twilight.twilight)
cli.add_command(whereis.whereis)


if __name__ == "__main__":
    cli()
