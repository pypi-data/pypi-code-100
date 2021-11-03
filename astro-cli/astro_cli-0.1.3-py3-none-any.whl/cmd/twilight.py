import click


@click.command()
@click.option("--until", "-u", help="until datetime", default="tomorrow")
@click.pass_obj
def twilight(astro, until, **kwargs):
    events = astro.get_twilight_events(until=until)
    click.echo(astro.serialize(events))
