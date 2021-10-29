
import importlib_metadata

from .mongo import JoMongodbDatabase as Database

try:
    __version__ = importlib_metadata.version("vnpy_jomongodb")
except importlib_metadata.PackageNotFoundError:
    __version__ = "dev"