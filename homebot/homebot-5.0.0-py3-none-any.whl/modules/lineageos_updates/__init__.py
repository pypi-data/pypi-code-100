"""HomeBot LineageOS updates module."""

from homebot.core.mdlintf import ModuleInterface, mdlbinder
from telegram.ext import CommandHandler

from homebot.modules.lineageos_updates.main import (
	add_user,
	remove_user,
	lineageos_updates,
)

class LineageosUpdatesModule(ModuleInterface):
	name = "lineageos_updates"
	version = "1.0"
	add_user = add_user
	remove_user = remove_user
	commands = {
		CommandHandler(["lineageos_updates"], lineageos_updates),
	}

mdlbinder.register_interface(LineageosUpdatesModule())
