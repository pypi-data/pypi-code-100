from homebot import __version__
from homebot.core.bot import BOT_DATA_HOMEBOT, ModuleStatus
from homebot.core.mdlintf import mdlbinder
from homebot.lib.libadmin import user_is_admin
from telegram.ext import CallbackContext
from telegram.update import Update

def start(update: Update, context: CallbackContext):
	update.message.reply_text("Hi! I'm HomeBot, and I'm alive\n"
							  f"Version {__version__}\n"
							  "To see all the available modules, type /modules")

def modules(update: Update, context: CallbackContext):
	message = "Loaded modules:\n\n"
	for module_name in mdlbinder.get_registered_interfaces():
		module = mdlbinder.get_interface(module_name)
		message += f"{module_name}\n"
		modules = context.bot_data[BOT_DATA_HOMEBOT].modules
		if module_name in modules:
			message += f"Status: {modules[module_name]}\n"
		else:
			message += f"Status: {ModuleStatus.DISABLED}\n"
		message += f"Commands: {', '.join([command.__name__ for command in module.commands])}\n\n"

	update.message.reply_text(message)

def enable(update: Update, context: CallbackContext):
	if not user_is_admin(update.message.from_user.id):
		update.message.reply_text("Error: You are not authorized to load modules")
		return

	if len(context.args) < 1:
		update.message.reply_text("Error: Module name not provided")
		return

	result = {}
	for module_name in context.args:
		module = mdlbinder.get_interface(module_name)
		if module is None:
			result[module_name] = "Module not found"
			continue

		if module.core:
			result[module_name] = "You can't enable a core module"
			continue

		try:
			context.bot_data[BOT_DATA_HOMEBOT].enable_module(module_name)
		except AttributeError:
			result[module_name] = "Module already enabled"
			continue

		result[module_name] = "Module enabled"

	text = [f"{module_name}: {status}" for module_name, status in result.items()]
	update.message.reply_text("\n".join(text))

def disable(update: Update, context: CallbackContext):
	if not user_is_admin(update.message.from_user.id):
		update.message.reply_text("Error: You are not authorized to unload modules")
		return

	if len(context.args) < 1:
		update.message.reply_text("Error: Module name not provided")
		return

	result = {}
	for module_name in context.args:
		module = mdlbinder.get_interface(module_name)
		if module is None:
			result[module_name] = "Module not found"
			continue

		if module.core:
			result[module_name] = "You can't disable a core module"
			continue

		try:
			context.bot_data[BOT_DATA_HOMEBOT].disable_module(module_name)
		except AttributeError:
			result[module_name] = "Module already disabled"
			continue

		result[module_name] = "Module disabled"

	text = [f"{module_name}: {status}" for module_name, status in result.items()]
	update.message.reply_text("\n".join(text))
