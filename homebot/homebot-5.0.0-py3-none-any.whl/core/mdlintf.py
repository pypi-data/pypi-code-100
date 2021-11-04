#
# Module Interface core
#

# TODO: Remove with Python 3.10
from __future__ import annotations

from homebot.core.binder import Binder, BinderInterface
from homebot.core.error_handler import format_exception
from homebot.core.logging import LOGE
from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules
from telegram.bot import Bot
from telegram.ext import Handler
from typing import Callable

def import_modules(modules_path: Path):
	"""Import all the modules and let them execute register_module()."""
	for module_name in [name for _, name, _ in iter_modules([str(modules_path)])]:
		try:
			import_module(f'homebot.modules.{module_name}')
		except Exception as e:
			LOGE(f"Error importing module {module_name}:\n"
			     f"{format_exception(e)}")

class _IOCTLReturn:
	(
		_OK,
		_MODULE_NOT_FOUND,
		_NO_IOCTL,
		_NOT_SUPPORTED,
		_MODULE_SPECIFIC_ERROR,
	) = range(5)

	STRINGS = {
		_OK: "IOCTL handled successfully",
		_MODULE_NOT_FOUND: "Requested module isn't registered",
		_NO_IOCTL: "The module doesn't support IOCTL",
		_NOT_SUPPORTED: "IOCTL value not supported",
		_MODULE_SPECIFIC_ERROR: "Module-specific error",
	}

	def __init__(self, status: int):
		self.status = status

	def __int__(self):
		return self.status

	def __str__(self) -> str:
		return self.STRINGS[self.status]

class IOCTLReturn(_IOCTLReturn):
	OK = _IOCTLReturn(_IOCTLReturn._OK)
	MODULE_NOT_FOUND = _IOCTLReturn(_IOCTLReturn._MODULE_NOT_FOUND)
	NO_IOCTL = _IOCTLReturn(_IOCTLReturn._NO_IOCTL)
	NOT_SUPPORTED = _IOCTLReturn(_IOCTLReturn._NOT_SUPPORTED)
	MODULE_SPECIFIC_ERROR = _IOCTLReturn(_IOCTLReturn._MODULE_SPECIFIC_ERROR)

def mdlintf_ioctl(module_name: str, ioctl: int, data: dict) -> IOCTLReturn:
	"""
	Perform a IOCTL call.

	If everything went ok, this function will return OK
	and result data will be in data dictionary,
	else refer to the returned value and module specific constants
	"""
	module = mdlbinder.get_interface(module_name)
	if module is None:
		return IOCTLReturn.MODULE_NOT_FOUND

	return module.ioctl(ioctl, data)

class ModuleInterface(BinderInterface):
	"""
	Module Binder interface.

	Attributes:
	- add_user: Function called when a bot enable the module
	- remove_user: Function called when a bot disable the module
	- handlers: python-telegram-bot handlers
	- ioctl: Function to handle IOCTL
	"""
	add_user: Callable[[ModuleInterface, Bot], None] = lambda self, bot: None
	remove_user: Callable[[ModuleInterface, Bot], None] = lambda self, bot: None
	handlers: list[Handler] = []
	ioctl: Callable[[ModuleInterface, int, dict], IOCTLReturn] = lambda self, ioctl, data: IOCTLReturn.NO_IOCTL

mdlbinder = Binder(ModuleInterface)
