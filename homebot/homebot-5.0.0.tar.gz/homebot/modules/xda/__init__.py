"""HomeBot XDA module."""

from homebot.core.mdlintf import ModuleInterface, mdlbinder
from telegram.ext import CommandHandler

from homebot.modules.xda.main import (
	xda,
)

class XdaModule(ModuleInterface):
	name = "xda"
	version = "1.0"
	commands = {
		CommandHandler(["xda"], xda),
	}

mdlbinder.register_interface(XdaModule())
