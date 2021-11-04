import os
import pathlib
from functools import partial

import typer
import uvicorn

from workplanner import logger

path_to_db = os.getenv(
    "WORKPLANNER_DATABASE_PATH", pathlib.Path.home() / "workplanner.db"
)


def webserver(
    dbpath: str = path_to_db,
    host: str = "127.0.0.1",
    port: int = 14444,
    debug: bool = False,
    loglevel: str = "INFO",
):
    os.environ["WORKPLANNER_DATABASE_PATH"] = dbpath

    from workplanner.views import app as webapp

    typer.echo("\n===== WorkPlanner =====")
    typer.echo(f"WORKPLANNER_DATABASE_PATH={dbpath}")
    typer.echo(f"INFO:     http://{host}:{port}/docs")
    typer.echo(f"INFO:     http://{host}:{port}/redoc\n")

    if debug:
        loglevel = "DEBUG"

    if loglevel.upper() == "TRACE":
        logger.setLevel("DEBUG")
    else:
        logger.setLevel(loglevel.upper())

    partial(webapp, debug=debug)
    uvicorn.run(
        webapp, host=host, port=port, log_level=loglevel.lower(), use_colors=True
    )


if __name__ == "__main__":
    typer.run(webserver)
