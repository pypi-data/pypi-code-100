from functools import wraps
import inspect
import warnings
from pyguardian import errors

class Guard:
	def __init__(self, *types, **kwtypes):
		"""
		Parameters:
		types   -- the accepted types for each argument (positional) 
		kwtypes -- the accepted types for each argument (keyword)
		"""
		self._types = self.__replace_none(types)
		self._kwtypes = self.__replace_none(kwtypes)
		self.__validate_constructor()

	def __call__(self, func):
		"""
		Entry point of validation. Therefore, this method is called when the guarded method is called.

		Parameters:
		func -- the guarded function
		"""
		self.func = func
		@wraps(func)
		def wrapper(*func_args, **func_kwargs):
			sig = inspect.signature(func)

			# raise warning if constructor received keyword argument that is not a parameter in the guarded method
			# cannot be placed in '__validate_constructor' because 'func' and 'func_kwargs' are only available on method call
			unknown_keywords = [k for k in self._kwtypes if func_kwargs.get(k) is None]
			if len(unknown_keywords) > 0:
				warnings.warn(
						errors.UnknownKeywordArgumentWarning(
								func=self.func,
								unknown_keywords=unknown_keywords
							),
						stacklevel=2
					)

			compiled_params = self.__compile_params(sig, *func_args, **func_kwargs)
			self.__validate_func(compiled_params)

			return func(*func_args, **func_kwargs)
		return wrapper

	def __compile_params(self, sig, *func_args, **func_kwargs):
		"""
		Compiles the function parameters and their respective types into a dictionary for further processing.
		The output of this function is generally passed to '__validate_func' via its 'compiled_params' argument for validation.
	
		Parameters:
		func_params -- a list of the items (as tuples) in an ordered dictionary ('OrderedDict') with the parameter name and its value as each respective item

		Examples:
		>>> func_params = OrderedDict([('a', 1), ('b', True), ('c', 2)])
		>>> __compile_params(func_params)
		{
			'a': (1, <class 'int'>, 'POSITIONAL_OR_KEYWORD'), 
			'b': (True, <class 'bool'>, 'POSITIONAL_OR_KEYWORD'), 
			'c': (2, <class 'str'>, 'POSITIONAL_OR_KEYWORD')
		}		
		"""
		argu = sig.bind(*func_args, **func_kwargs)
		argu.apply_defaults()
		param_kinds = {name:str(param.kind) for name, param in sig.parameters.items()}

		compiled_params = {}
		idx = 0
		for name,value in argu.arguments.items():
			# assign type to parameter by keyword first
			if self._kwtypes.get(name):
				compiled_params[name] = (value, self._kwtypes.get(name), param_kinds[name])
			else:
				# if type was not specified by keyword, assign the next type that was specified via positional argument
				try:
					compiled_params[name] = (value, self._types[idx], param_kinds[name])
					idx += 1
				# assign 'ANY_TYPE' if there are no types left to assign
				except IndexError:
					# 'ANY_TYPE' denotes that the passed value can be of any type
					# 'None' could not be used for this because 'None' is a specifiable type
					compiled_params[name] = (value, "ANY_TYPE", param_kinds[name])

		return compiled_params

	def __validate_constructor(self):
		"""
		Validates the arguments passed into the 'guard' constructor.

		Accepted arguments are positional and/or keyword arguments of type 'type' or 'NoneType'.
		Arguments of type 'list' or 'tuple' which contain elements of type 'type' and/or 'NoneType' are also accepted.

		The acceptance of 'NoneType' means the value 'None' itself is accepted. 
		Because 'NoneType' is not directly accessible, 'None' is accepted to deter the passing of 'type(None)' to the constructor.
		"""
		all_types = list(self._types) + list(self._kwtypes.values())

		for classinfo in all_types:
			if not isinstance(classinfo, (type, tuple)) and classinfo is not None:
				raise(ValueError(f"guard constructor not properly called!"))
			elif isinstance(classinfo, (list, tuple)):
				if not self.__allinstance(classinfo, type) or len(classinfo) == 0:
					raise(ValueError(f"guard constructor not properly called!"))

	def __validate_func(self, compiled_params):
		"""
		Raises an 'InvalidArgumentTypeError' if any passed value in 'compiled_params' is not an instance of the expected type.

		Parameters:
		compiled_params -- dictionary with necessary parameter info with parameter name as keys and value, expected type, and parameter kind as the values

		Examples:
		>>> compiled_params = {
				'a': (1, <class 'int'>, 'POSITIONAL_OR_KEYWORD'), 
				'b': (True, <class 'bool'>, 'POSITIONAL_OR_KEYWORD'), 
				'c': (2, <class 'str'>, 'POSITIONAL_OR_KEYWORD')
			}
		>>> __validate_func(compiled_params)
		Traceback (most recent call last):
			...
		errors.InvalidArgumentTypeError: 'foo' expects value of type 'str' for parameter 'c' but got 'int'
		"""
		illegal_type = None
		for name,(value,classinfo,kind) in compiled_params.items():

			# 'VAR_POSITIONAL' is an *args-like parameter 
			# 'VAR_KEYWORD' is a **kwargs-like parameter
			if kind == "VAR_POSITIONAL":
				illegal_type = self.__find_invalid_type(value, classinfo, arbitrary_args_n=True)
			elif kind == "VAR_KEYWORD":
				illegal_type = self.__find_invalid_type(value.values(), classinfo, arbitrary_args_n=True)
			else:
				illegal_type = self.__find_invalid_type(value, classinfo)

			# if 'illegal_type' is 'None' it means that the value passed for that parameter is valid
			if illegal_type is not None:
				raise errors.InvalidArgumentTypeError(
						func=self.func,
						param_name=name,
						classinfo=classinfo,
						passed_type=illegal_type
					)

	def __find_invalid_type(self, value, classinfo, arbitrary_args_n=False):
		"""
		Returns None if the parameter is valid, otherwise returns the type of the invalid parameter.

		Parameters:
		value            -- the name of the parameter
		classinfo        -- the type or class to check against
		arbitrary_args_n -- specifies whether the 'value' comes from *args-like or **kwargs-like parameters

		Examples:
		>>> __validate_param(1, str)
		int

		>>> # ('value' coming from function parameter *args or **kwargs)
		>>> __validate_param((1,2,3), int, arbitrary_args_n=True)
		None
		"""
		# 'bool' must be specifically checked for because it is a subclass of 'int'.
		# Therefore, 'isinstance(True, int)' and 'isinstance(False, int)' return True which may not be intended.
		if classinfo != "ANY_TYPE":
			if arbitrary_args_n:
				if any(isinstance(v, bool) for v in value):
					if isinstance(classinfo, (list, tuple)) and bool not in classinfo:
						return bool
					elif not isinstance(classinfo, (list, tuple)) and classinfo != bool:
						return bool
				illegal_value = self.__allinstance(value, classinfo, return_illegal=True)[1]
				if illegal_value:
					return type(illegal_value)
			else:
				if isinstance(value, bool):
					if isinstance(classinfo, (list, tuple)) and bool not in classinfo:
						return bool
					elif not isinstance(classinfo, (list, tuple)) and classinfo != bool:
						return bool
				elif not isinstance(value, classinfo):
					return type(value)

	@staticmethod
	def __replace_none(iterable):
		"""
		Replaces instances of 'None' with 'NoneType' in the iterable argument. 
		Instances of 'None' that are contained inside a nested iterable are also replaced.

		Parameters:
		iterable -- the iterable containing 'None'

		Examples:
		>>> __replace_none((str, None))
		(str, NoneType)

		>>> __replace_none((str, (int, None)))
		(str, (int, NoneType))
		"""
		if isinstance(iterable, dict):
			for idx, (name, classinfo) in enumerate(iterable.items()):
				if isinstance(classinfo, (list, tuple)) and None in classinfo:
					iterable[name] = tuple(type(None) if t is None else t for t in classinfo)
		else:
			for idx, classinfo in enumerate(iterable):
				if isinstance(classinfo, (list, tuple)) and None in classinfo:
					iterable[idx] = tuple(type(None) if t is None else t for t in classinfo)
				elif classinfo is None:
					iterable[idx] = type(None)
		return iterable

	@staticmethod
	def __allinstance(iterable, classinfo, return_illegal=False):
		"""
		'__allisntance' is responsible for scanning the elements of an iterable and verifying that all of those elements are of the specified type.
		
		Parameters:
		iterable       -- the iterable to scan
		classinfo      -- the type or class to check against
		return_illegal -- if True, the first element that is not an instance or direct/virtual subclass of is additionally returned

		Examples:
		>>> __allinstance([1, 2, 3], int, False)
		True
		
		>>> __allinstance([1, 2, 3], int, True)
		True, None

		>>> __allinstance([1, 2.1, 3], int, True)
		False, 2.1
		"""
		if return_illegal:
			for e in iterable:
				if not isinstance(e, classinfo):
					return False, e
			return True, None
		else:
			return all(isinstance(e, classinfo) for e in iterable)
