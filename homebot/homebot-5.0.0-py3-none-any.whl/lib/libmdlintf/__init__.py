"""Module interface library."""

from homebot.core.mdlintf import ModuleInterface
from homebot.core.mdlintf import get_module as _get_module
from homebot.core.mdlintf import register_module as _register_module

def get_module(module_name: str):
	return _get_module(module_name)

def register_module(mdlintf: ModuleInterface):
	return _register_module(mdlintf)
