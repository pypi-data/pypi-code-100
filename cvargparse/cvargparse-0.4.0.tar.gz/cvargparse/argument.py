import pyaml

from dataclasses import dataclass

class Argument(object):
	def __init__(self, *args, **kw):
		super(Argument, self).__init__()
		self.args = args # positional arugments
		self.kw = kw # keyword arguments


class FileArgument(Argument):
	def __init__(self, *args, **kw):
		super(FileArgument, self).__init__(*args, **kw)

	@classmethod
	def mode(cls, file_mode, encoding=None):
		def wrapper(*args, **kw):
			obj = cls(*args, **kw)
			obj.kw["type"] = argparse.FileType(file_mode, encoding=encoding)
			return obj
		return wrapper

def JupyterArguments(cls=None, *args, repr=False, **kwargs):

	def _yaml_repr_(self) -> str:
		cls_name = type(self).__name__
		return pyaml.dump({cls_name: self.__dict__}, sort_dicts=False)

	def wrap(cls):
		if not repr and "__repr__" not in cls.__dict__:
			setattr(cls, "__repr__", _yaml_repr_)
		return dataclass(cls, *args, repr=repr, **kwargs)

	# See if we're being called as @dataclass or @dataclass().
	if cls is None:
		return wrap

	return wrap(cls)

if __name__ == '__main__':

	@JupyterArguments
	class Args:
		arg1: int = 0
		arg2: int = 1

	print(Args())
