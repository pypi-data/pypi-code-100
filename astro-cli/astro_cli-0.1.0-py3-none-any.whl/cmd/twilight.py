import json
import click
from tabulate import tabulate

from astro.cmd import global_options


@click.command()
@click.option("--until", "-u", help="until datetime", default="tomorrow")
@global_options
@click.pass_obj
def twilight(astro, until, **kwargs):
    events = astro.get_twilight_events(until=until)

    if kwargs.get("json"):
        click.echo(json.dumps(events))
    else:
        click.echo(tabulate(events, headers="keys"))
