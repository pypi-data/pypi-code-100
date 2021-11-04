#
# Module Binder IPC
#

from homebot.core.logging import LOGI, LOGW
from threading import Lock

class BinderInterface:
	"""
	Generic Binder interface.

	It is used as a superclass of other interfaces.

	Attributes:
	- name: Name of the interface
	- version: Version of the interface
	- core: The interface implements vital features
	"""
	name: str = "none"
	version: str = "0.0"
	core: bool = False

class Binder:
	"""
	A class simulating Android Binder IPC.

	It allows safe interfaces management and interaction.

	Attributes:
	- interface_type: Type of the interface instances
	"""
	def __init__(self, interface_type: type):
		"""
		Initialize the class.
		
		interface_type must be a subclass of BinderInterface, raises AssertionError otherwise.
		"""
		self.interface_type = interface_type

		if not issubclass(self.interface_type, BinderInterface):
			raise AssertionError("Type is not a subclass of BinderInterface")

		self.__interfaces: dict[str, BinderInterface] = {}
		self.__lock = Lock()

	def get_registered_interfaces(self):
		"""Return the list of all registered interfaces' names"""
		with self.__lock:
			return self.__interfaces.keys()

	def get_interface(self, module_name: str):
		"""
		Given a module name, get a module instance.

		Raises ModuleNotFoundError if the module isn't registered.
		"""
		with self.__lock:
			if module_name not in self.__interfaces:
				raise ModuleNotFoundError(f'Module {module_name} not found')

			return self.__interfaces[module_name]

	def register_interface(self, interface):
		"""
		Register a module instance. Will replace the registered interface if it already exists.

		Raises AssertionError if the instance type isn't the expected one.
		"""
		if not issubclass(type(interface), self.interface_type):
			raise AssertionError("Interface type is different from the expected one")

		with self.__lock:
			name = interface.name
			if name in self.__interfaces:
				LOGW(f'Replacing already registered module "{interface.name}" with a new instance, '
				     f'old ID: {id(self.__interfaces[name])}, new ID: {id(interface)}')
				del self.__interfaces[name]

			self.__interfaces[name] = interface

			LOGI(f'Registered module "{name}" with ID {id(self.__interfaces[name])}')
