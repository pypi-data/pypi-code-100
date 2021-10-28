try:
    from importlib import metadata
except ImportError:  # for Python<3.8
    import importlib_metadata as metadata  # type: ignore

try:
    __version__ = metadata.version("mesaplot")
except metadata.PackageNotFoundError:
    # package is not installed
    pass