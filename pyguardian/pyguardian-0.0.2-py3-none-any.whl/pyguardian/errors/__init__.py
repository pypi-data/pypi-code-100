from pyguardian.errors.grammar import list_items

class InvalidArgumentTypeError(TypeError):
	"""
	Raised when a value of an incorrect type is passed to a guarded function.
	Subclass of 'TypeError'

	Parameters:
	func        -- the guarded function
	param_name  -- the name of the parameter that received an incorrectly-typed value
	classinfo   -- the type or class that was enforced
	passed_type -- the incorrect type
	"""
	def __init__(self, func, param_name, classinfo, passed_type):
		if isinstance(classinfo, (list, tuple)):
			classinfo = list_items([c.__name__ for c in classinfo])
		else:
			classinfo = list_items(classinfo.__name__)

		self.err_msg = f"'{func.__qualname__}' expects value of type {classinfo} for parameter '{param_name}' but got '{passed_type.__name__}'"

	def __str__(self):
		return self.err_msg

class UnknownKeywordArgumentWarning(Warning):
	"""
	Raised when a the guard constructor receives a keyword argument that does not exist in the guarded method's signature.
	Subclass of 'Warning'

	Parameters:
	func             -- the guarded function
	unknown_keywords -- the keywords that do not exist in the guarded method's signature
	"""
	def __init__(self, func, unknown_keywords):
		plural = len(unknown_keywords) > 1
		unknown_keywords = list_items(unknown_keywords)
		self.wrn_msg = f"guard constructor received unknown keyword {'arguments' if plural else 'argument'} {unknown_keywords} which may produce unexpected results as {'these arguments' if plural else 'this argument'} will not be applied."

	def __str__(self):
		return self.wrn_msg
