from homebot.core.error_handler import error_handler, format_exception
from homebot.core.logging import LOGE, LOGI
from homebot.core.mdlintf import mdlbinder
from telegram.ext import ContextTypes, Updater
from threading import Lock

class _ModuleStatus:
	(
		_DISABLED,
		_ENABLED,
		_ENABLING,
		_DISABLING,
		_ERROR,
	) = range(5)

	STRINGS = {
		_DISABLED: "Disabled",
		_ENABLED: "Enabled",
		_ENABLING: "Enabling",
		_DISABLING: "Disabling",
		_ERROR: "Error",
	}

	def __init__(self, status: int):
		self.status = status

	def __int__(self):
		return self.status

	def __str__(self) -> str:
		return self.STRINGS[self.status]

class ModuleStatus(_ModuleStatus):
	"""
	Module status.

	This class indicates the status of a HomeBot module for the bot.
	Can be casted to int and str.
	"""
	DISABLED = _ModuleStatus(_ModuleStatus._DISABLED)
	ENABLED = _ModuleStatus(_ModuleStatus._ENABLED)
	ENABLING = _ModuleStatus(_ModuleStatus._ENABLING)
	DISABLING = _ModuleStatus(_ModuleStatus._DISABLING)
	ERROR = _ModuleStatus(_ModuleStatus._ERROR)

BOT_DATA_HOMEBOT = "homebot"

class HomeBot(Updater):
	"""
	Main HomeBot class.

	It is a subclass of telegram.ext.Updater with the addition of:
	- A basic error handler that send the traceback to
	  the user and to the console
	- mdlintf modules loading on init
	"""
	def __init__(self, token: str):
		"""Initialize the bot."""
		context_types = ContextTypes(bot_data=lambda: {BOT_DATA_HOMEBOT: self})
		super().__init__(token=token, context_types=context_types)

		self.dispatcher.add_error_handler(error_handler, True)

		self.modules: dict[str, ModuleStatus] = {}
		self.modules_lock = Lock()

		for module_name in mdlbinder.get_registered_interfaces():
			self.enable_module(module_name)

	def enable_module(self, module_name: str):
		"""
		Enable a provided module and add its command handler
		to the bot's dispatcher.
		"""
		LOGI(f"Enabling module {module_name}")

		module = mdlbinder.get_interface(module_name)
		if module is None:
			raise ModuleNotFoundError(f"Module {module_name} not found")

		with self.modules_lock:
			if not module_name in self.modules:
				self.modules[module_name] = ModuleStatus.DISABLED

			if self.modules[module_name] == ModuleStatus.ENABLED:
				raise AttributeError("Module is already enabled")

			self.modules[module_name] = ModuleStatus.ENABLING

			try:
				for command in module.handlers:
					self.dispatcher.add_handler(command)
				module.add_user(self.dispatcher.bot)
			except Exception as e:
				LOGE(f"Failed to add handler for module {module_name}\n"
				     f"{format_exception(e)}")
				self.modules[module_name] = ModuleStatus.ERROR
			else:
				self.modules[module_name] = ModuleStatus.ENABLED
				LOGI(f"Module {module_name} enabled")

	def disable_module(self, module_name: str):
		"""
		Disable a provided module and remove its command handler
		from the bot's dispatcher.
		"""
		LOGI(f"Disabling module {module_name}")

		module = mdlbinder.get_interface(module_name)
		if module is None:
			raise ModuleNotFoundError(f"Module {module_name} not found")

		with self.modules_lock:
			if not module_name in self.modules:
				self.modules[module_name] = ModuleStatus.DISABLED

			if self.modules[module_name] == ModuleStatus.DISABLED:
				raise AttributeError("Module is already disabled")

			self.modules[module_name] = ModuleStatus.DISABLING

			try:
				for command in module.handlers:
					self.dispatcher.remove_handler(command)
				module.remove_user(self.dispatcher.bot)
			except Exception as e:
				LOGE(f"Failed to remove handler for module {module_name}\n"
				     f"{format_exception(e)}")
				self.modules[module_name] = ModuleStatus.ERROR
			else:
				self.modules[module_name] = ModuleStatus.DISABLED
				LOGI(f"Module {module_name} disabled")
