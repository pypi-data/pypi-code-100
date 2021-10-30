
class PySCFGError(Exception):
    pass


__all__ = ["core", "stores", "SimpleConfigs", "PySCFGError"]

# import SimpleConfigs into root namespace for simplicity
from .core import SimpleConfigs

# import modules into this namespace to make them available after installing by setup.py
# TODO: is there a proper way to do this?
from . import *
