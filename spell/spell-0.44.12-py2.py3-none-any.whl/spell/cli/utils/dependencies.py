import os

from spell.shared.dependencies import (
    CondaDependencies,
    in_virtualenv,
    NoEnvFound,
    PipDependencies,
    format_pip_versions as _format_pip_versions,
)
from spell.cli.exceptions import ExitException


def dependencies_from_env():
    if os.environ.get("CONDA_DEFAULT_ENV"):
        return CondaDependencies.from_env()
    elif in_virtualenv():
        return PipDependencies.from_env()
    raise NoEnvFound


# Recast the value error as an ExitException
def format_pip_versions(pip):
    try:
        return _format_pip_versions(pip)
    except ValueError as e:
        raise ExitException(str(e))
