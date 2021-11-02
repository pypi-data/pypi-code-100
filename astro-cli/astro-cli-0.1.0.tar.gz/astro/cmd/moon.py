import json
import click
from tabulate import tabulate

from astro.cmd import global_options


@click.group()
def moon():
    pass


@moon.command()
@click.option("--until", "-u", help="until datetime", default="next month")
@global_options
@click.pass_obj
def phases(astro, until, **kwargs):
    phases = astro.get_moon_phases(until=until)

    if kwargs.get("json"):
        click.echo(json.dumps(phases))
    else:
        click.echo(tabulate(phases, headers="keys"))


@moon.command()
@click.option("--until", "-u", help="until datetime", default="next year")
@global_options
@click.pass_obj
def eclipses(astro, until, **kwargs):
    eclipses = astro.get_moon_eclipses(until=until)

    if kwargs.get("json"):
        click.echo(json.dumps(eclipses))
    else:
        click.echo(tabulate(eclipses, headers="keys"))
