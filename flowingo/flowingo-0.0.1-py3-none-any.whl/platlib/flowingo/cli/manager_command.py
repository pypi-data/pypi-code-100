import socket
from typing import Optional

import click

from flowingo.configuration import conf
from flowingo.manager.app import app


@click.command()
@click.option('-d', '--demonize', is_flag=True, default=False, show_default=True, help='Demonize manager')
@click.option('--pipelines', type=click.Path(exists=True, file_okay=False, readable=True), help='Pipelines folder')
@click.option('--tasks', type=click.Path(exists=True, file_okay=False, readable=True), help='Tasks folder')
def manager(demonize: bool, pipelines: Optional[str], tasks: Optional[str]):
    """Starts flowingo manager worker"""
    if pipelines:
        conf.pipelines_folder = pipelines
    if tasks:
        conf.tasks_folder = tasks
    conf.manager_demonize = demonize

    worker = app.Worker(
        hostname=f'manager@{socket.gethostname()}',
        # loglevel='INFO',
        loglevel='DEBUG',
        queues='manager',
        concurrency=1,
        pool='solo',
        send_task_events=True,  # TODO: fix enable events
    )
    worker.start()
