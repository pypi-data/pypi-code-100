import click

from jetpack import _runtime as runtime
from jetpack import cron
from jetpack._job.job import Job
from jetpack.cmd import util
from jetpack.config import symbols
from jetpack.config.symbols import Symbol

_using_new_cli = False


def is_using_new_cli() -> bool:
    """
    for legacy uses, we keep old cli. This function disables that logic to ensure
    we don't run the cli command twice.
    """
    return _using_new_cli


@click.group()
def cli() -> None:
    global _using_new_cli
    _using_new_cli = True


@click.command(help="Runs jetpack job")
@click.option("--entrypoint", required=True)
@click.option("--exec-id", required=True)
@click.option("--job-name", required=True)
@click.option("--encoded-args", default="")
def job(entrypoint: str, exec_id: str, job_name: str, encoded_args: str) -> None:
    util.load_user_entrypoint(entrypoint)
    func = symbols.get_symbol_table()[Symbol(job_name)]
    Job(func).exec(exec_id, encoded_args)


@click.command(help="Registers jetpack functions with runtime")
@click.option("--entrypoint", required=True)
def register(entrypoint: str) -> None:
    util.load_user_entrypoint(entrypoint)
    runtime.set_cron_jobs(cron.get_jobs())


cli.add_command(job)
cli.add_command(register)
