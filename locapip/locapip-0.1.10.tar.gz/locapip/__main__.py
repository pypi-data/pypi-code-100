import logging
from pathlib import Path

import click

import locapip


@click.command()
@click.option('--port', type=int, default=6547)
@click.option('--proto', type=click.Path(file_okay=False, dir_okay=True, path_type=Path), multiple=True)
def main(port: int, proto):
    if proto is not None:
        for path in proto:
            locapip.server_packages.add(path)

    logging.basicConfig(level=logging.INFO)
    locapip.serve(port)


if __name__ == "__main__":
    main()
