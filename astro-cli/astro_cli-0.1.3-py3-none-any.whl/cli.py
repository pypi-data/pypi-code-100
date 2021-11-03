import click

from astro.cmd import moon, twilight, whereis
from astro.lib import Astro


@click.group()
@click.option("--date", "-d", help="Observer datetime", default="now")
@click.option("--lat", help="Observer latitude")
@click.option("--lon", help="Observer longitude")
@click.option("--timezone", "--tz", help="Timezone")
@click.option(
    "--force-geoip",
    help="Bypass GeoIP cache (1 day), if lat/lon are't set",
    is_flag=True,
)
@click.option(
    "--format",
    "-f",
    help="Output format",
    type=click.Choice(["table", "json"]),
    default="table",
)
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
