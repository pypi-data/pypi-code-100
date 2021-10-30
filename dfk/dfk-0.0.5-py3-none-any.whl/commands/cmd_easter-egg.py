import click


@click.group("easter-egg")
def cli():
    # TODO: Implement this later.
    """🐰🥚 The easter-egg command."""


@cli.command()
def run():
    """Runs a easter surprise."""
    raise NotImplementedError("You must implement the run() method yourself!")
