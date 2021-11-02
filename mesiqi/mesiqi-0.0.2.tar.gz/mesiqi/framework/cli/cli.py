import os
import webbrowser
from copy import deepcopy
from pathlib import Path
from typing import Any, Sequence

import click

from mesiqi import __version__ as version
from mesiqi.core.jobs import run_all_job_in_directory, run_job

here = os.getcwd()

LOGO = rf"""
mesiqi. v{version}
"""


@click.group(name="mesiqi")
@click.version_option(version, "--version", "-V", help="Show version and exit")
def cli():
    """mesiqi is a CLI for running data ingestion and governance jobs. For more
    information, type ``mesiqi info``.
    """
    pass


@cli.command()
def info():
    """Get more information about mesiqi."""
    click.secho(LOGO, fg="green")
    click.echo("Tools for building data microservices.")


@cli.command(short_help="See the API docs and introductory tutorial.")
def docs():
    """Display the API docs and introductory tutorial in the browser,
    using the packaged HTML doc files."""
    html_path = str((Path(__file__).parent.parent / "html" / "index.html").resolve())
    index_path = f"file://{html_path}"
    click.echo(f"Opening {index_path}")
    webbrowser.open(index_path)


@cli.command()
@click.option("--profile-dir", envvar="mesiqi_PROFILE_DIR", default=None, required=False)
@click.option("--job-dir", envvar="mesiqi_JOB_DIR", default="jobs", required=False)
@click.option("--job", default=None, help="Job to be run", required=False)
def run(profile_dir, job_dir, job):
    dir = here
    if job_dir:
        dir = os.path.join(here, job_dir)

    if job:  # run single job
        source = os.path.join(dir, job)
        click.echo(f"run job: {source}")
        run_job(source)
    else:  # run all jobs in jobs directory
        click.echo(f"run all jobs in directory: {dir}")
        run_all_job_in_directory(dir)


def main():
    cli()


if __name__ == "__main__":
    main()
