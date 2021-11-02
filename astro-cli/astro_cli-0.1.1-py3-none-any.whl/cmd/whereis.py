import json
import click
from tabulate import tabulate

from astro.cmd import global_options


@click.command()
@click.argument("body")
@global_options
@click.pass_obj
def whereis(astro, body, **kwargs):
    alt, az, distance = astro.whereis(body)
    position = {
        "alt": str(alt.degrees),
        "az": str(az.degrees),
        "distance": str(distance.km)
    }

    if kwargs.get("json"):
        click.echo(json.dumps(position))
    else:
        click.echo(tabulate([position], headers="keys"))
