"Simple command to record to a file outside a project"
import click

from ..recording import interactive_recorder

@click.command()
@click.argument(
    "path",
    type=click.Path(exists=False, file_okay=True, dir_okay=False)
)
def rec_file(path):
    "Record a file at PATH outside a project"
    interactive_recorder(path + ".wav")
