"""Main executable file. Refer to cli module"""
import click

from flowingo.cli.db_command import db
from flowingo.cli.manager_command import manager
from flowingo.cli.pipeline_command import pipeline
from flowingo.cli.webserver_command import webserver


@click.group()
@click.version_option(prog_name='flowingo')
def main() -> None:
    """Main executable function"""
    pass


# Add main group commands
main.add_command(db)
main.add_command(manager)
main.add_command(pipeline)
main.add_command(webserver)


if __name__ == '__main__':  # pragma: nocover
    main()
