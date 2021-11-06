import importlib.util
from typing import Any, Optional, Callable, TypeVar, List
from pathlib import Path
import sys

import plover  # type: ignore

T=TypeVar("T", bound=Callable[[], None])

class Main:
	plugin_running: bool
	start_functions: List[Callable[[], None]]
	stop_functions: List[Callable[[], None]]

	def __init__(self, engine: "plover.engine.StenoEngine") -> None:
		self.engine=engine
		self.plugin_running=False

		try:
			self.load_file()
		except:
			plover.log.error("while running plover_startup_py:__init__", exc_info=True)

		global instance
		assert instance is None
		instance=self


	# [[convenience functions]] passed to the file.
	def register_start(self, f: T)->T:
		"""
		Register a function to be executed when the plugin starts.

		Can be used as a decorator.

		Functions are executed in register order.
		"""
		self.start_functions.append(f)
		return f

	def register_stop(self, f: T)->T:
		"""
		Register a function to be executed when the plugin stops.

		Can be used as a decorator.

		Functions are executed in reverse register order.
		"""
		self.stop_functions.append(f)
		return f

	def patch_function(self, o: Any, prop: str, f: Callable=None)->Any:
		"""
		Register a function to be executed when the plugin starts.
		The convenience functions are passed in as global variables.

		Can be used as a decorator.

		The original function is accessible as <the function function>.

		Parameters:
			o: the object.
			prop: the property name.
			f: the function. If None is passed then the function returns a decorator to apply to the function f.

		Return:
			The decorator function, or the function verbatim, with additional `_original` method set.
		"""
		if f is None:
			return lambda f: self.patch_function(o, prop, f)

		def do_patch_start()->None:
			assert not hasattr(f, "_original")
			f._original=getattr(o, prop)  # type: ignore
			setattr(o, prop, f)

		def do_patch_stop()->None:
			assert hasattr(getattr(o, prop), "_original")
			setattr(o, prop, getattr(o, prop)._original)

		self.register_start(do_patch_start)
		self.register_stop(do_patch_stop)
		return f

	def load_file(self)->None:
		"""
		Function to (re)load the file.

		Might raise an error if the file failed to load.

		In any case, start_functions and stop_functions are set to the correct value/emptied.
		"""

		if self.plugin_running:
			try:
				self.stop()
			finally:
				try:
					self.load_file()
				finally:
					self.start()
			return

		self.start_functions=[]
		self.stop_functions=[]
		# NOTE this line is mentioned in the documentation
		exec(
				(Path(plover.oslayer.config.CONFIG_DIR)/"plover_startup_py_config.py").read_text(),
				dict(
					register_start=self.register_start,
					register_stop=self.register_stop,
					patch_function=self.patch_function,
					engine=self.engine,
					)
				)

	def start(self) -> None:
		"""
		Function to start the extension plugin. Called by Plover.

		Will never raise an error. Direct error log to plover.log instead.
		"""
		assert not self.plugin_running
		self.plugin_running=True
		try:
			for f in self.start_functions:
				f()
		except:
			plover.log.error(f"while running plover_startup_py:start - {f}", exc_info=True)

	def stop(self) -> None:
		"""
		Function to stop the extension plugin. Called by Plover.

		Will never raise an error. Direct error log to plover.log instead.
		"""
		try:
			for f in reversed(self.stop_functions):
				f()
		except:
			plover.log.error(f"while running plover_startup_py:stop - {f}", exc_info=True)
		assert self.plugin_running
		self.plugin_running=False

instance: Optional[Main]=None

def reload(engine, argument: str)->None:
	if instance is None:
		plover.log.error("The extension plugin is not running!")
		return
	instance.load_file()
