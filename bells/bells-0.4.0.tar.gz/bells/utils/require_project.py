"Decorator for commands which only work inside projects"
from functools import wraps

import click

from .config import pass_config
from .get_root import get_root


def require_project(command):
    """Decorator for commands which only work inside projects.

    Usage:
        @click.command()
        ...  # other click args
        @utils.require_project
        def your_cmd(config, ...): # first parameter is going to be config
            pass
    """
    @pass_config
    @wraps(command)
    def new_command(*args, **kwargs):
        "Command Wrapper"
        root = get_root()
        if not root:
            click.echo("No root directory of project found", err=True)
            return 1
        command(*args, **kwargs)
        return 0
    return new_command
