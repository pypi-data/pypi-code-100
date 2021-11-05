from logging import getLogger
from pathlib import Path

import toml
from pkg_resources import DistributionNotFound, get_distribution

log = getLogger(__name__)

# Root path to the Skaha Project
BASE_PATH: Path = Path(__file__).absolute().parent.parent

try:
    __version__ = get_distribution("skaha").version
except DistributionNotFound as e:
    log.warning(e)
    pyproject = toml.load(BASE_PATH / "pyproject.toml")
    __version__ = pyproject["tool"]["poetry"]["version"]
except Exception as e:
    log.warning(e)
    log.warning("unable to determine skaha client version")
    __version__ = "unknown"
