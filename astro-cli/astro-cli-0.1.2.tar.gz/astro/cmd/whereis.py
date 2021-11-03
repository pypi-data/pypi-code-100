import click


@click.command()
@click.argument("body")
@click.pass_obj
def whereis(astro, body, **kwargs):
    alt, az, distance = astro.whereis(body)

    position = {
        "alt": str(alt.degrees),
        "az": str(az.degrees),
        "distance": str(distance.km)
    }

    click.echo(astro.serialize([position]))
