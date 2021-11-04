import click

from .commands import start_dash, start_project


@click.group()
def cli():
    pass


cli.add_command(start_project)
cli.add_command(start_dash)

if __name__ == "__main__":
    cli()  # pragma: no cover
