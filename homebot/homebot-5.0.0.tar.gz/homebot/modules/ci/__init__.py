"""HomeBot CI module."""

from homebot.core.mdlintf import ModuleInterface, mdlbinder
from telegram.ext import CommandHandler

from homebot.modules.ci.main import (
	ci,
)

class CiModule(ModuleInterface):
	name = "ci"
	version = "1.0"
	commands = [
		CommandHandler(["ci"], ci),
	]

mdlbinder.register_interface(CiModule())
