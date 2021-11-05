"Init command"
import logging
import os
import pathlib
import sys

import click
from .. import utils

@click.command()
@click.argument("path", type=click.Path(writable=True, path_type=pathlib.Path),
                required=False, default=".")
@utils.pass_config
def init(config, path):
    """Initializes a new bells project"""
    if config.root:
        logging.error("Trying to create project inside another project, exiting.")
        click.echo(
            f"Project exists at {config.root}. Nested projects are not supported",
            err=True
        )
        sys.exit(1)

    if (path/".bells").is_dir() and (path/".bells"/"config.ini").is_file():
        logging.error("Project exists. Exiting")
        click.echo(
            f"Project exists at {path.absolute()}"
        )


    logging.info("Creating the directory")
    os.makedirs(path/".bells", exist_ok=True)

    logging.info("Creating .bells/config.ini")
    with open(path/".bells"/"config.ini", "w", encoding="utf-8") as config_file:
        config_file.write("")

    logging.info("Creating other directories")
    os.mkdir(path/"structural")
    os.mkdir(path/"chronological")

    click.echo(f"Created new bells project at {path.absolute()}")
