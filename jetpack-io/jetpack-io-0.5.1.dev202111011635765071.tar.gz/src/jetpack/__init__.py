# __version__ is placeholder
# It gets set in the build/publish process (publish_with_credentials.sh)
__version__ = "0.5.1-dev202111011635765071"

from jetpack._job.interface import job
from jetpack._remote.interface import remote
from jetpack.cli import handle as init
from jetpack.cmd import root
from jetpack.redis import redis


def run() -> None:
    root.cli()
