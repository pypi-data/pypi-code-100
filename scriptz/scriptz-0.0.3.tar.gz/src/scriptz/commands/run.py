import typer
from typer import Option, Argument
import os
import subprocess
from pathlib import Path
from typing import List

from scriptz import cli, logger, Manager


@cli.command()
def run(
    paths: List[Path] = Argument(None),
    start: Path = Option(None),
    continue_on_error: bool = Option(False),
):
    """ Run scripts specified. """

    manager = Manager()
    paths = paths or [Path.cwd()]

    start = start and start.absolute()

    for script in manager.iterate_scripts(paths):
        if start and (script.path < start):
            logger.info(f"- Skipping: {script}")

        else:
            logger.info(f"+ Running: {script} ....................+")

            args = [script.handler.command] + script.handler.options
            args.append(script.path)

            env = manager.config.get_environ(script.path)

            process = subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                env=dict(os.environ, **env),
            )

            with process.stdout:
                log_subprocess_output(process.stdout)

            exit_code = process.wait()  # 0 means success
            if exit_code:
                logger.error(f"Error Code = {exit_code}")
                if not continue_on_error:
                    logger.error(f"Exiting.")
                    raise typer.Exit(exit_code)


def log_subprocess_output(pipe):
    for line in iter(pipe.readline, b""):
        logger.info(line.decode().strip())
