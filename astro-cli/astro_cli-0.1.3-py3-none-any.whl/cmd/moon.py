import click


@click.group()
def moon():
    pass


@moon.command()
@click.option("--until", "-u", help="until datetime", default="next month")
@click.pass_obj
def phases(astro, until, **kwargs):
    phases = astro.get_moon_phases(until=until)
    click.echo(astro.serialize(phases))


@moon.command()
@click.option("--until", "-u", help="until datetime", default="next year")
@click.pass_obj
def eclipses(astro, until, **kwargs):
    eclipses = astro.get_moon_eclipses(until=until)
    click.echo(astro.serialize(eclipses))
