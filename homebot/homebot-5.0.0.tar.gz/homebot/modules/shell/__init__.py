"""HomeBot shell module."""

from homebot.core.mdlintf import ModuleInterface, mdlbinder
from telegram.ext import CommandHandler

from homebot.modules.shell.main import (
	shell,
)

class ShellModule(ModuleInterface):
	name = "shell"
	version = "1.0"
	core: True
	commands = {
		CommandHandler(["shell"], shell),
	}

mdlbinder.register_interface(ShellModule())
