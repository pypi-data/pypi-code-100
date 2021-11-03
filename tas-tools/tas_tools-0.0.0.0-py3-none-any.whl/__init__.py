"""tas_tools python module documentation"""

# Promote our version to our top level package.
try:
    from .version import __version__
except ImportError:
    __version__ = '0.0.0.0'