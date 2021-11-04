import abc
import argparse
import logging
import typing as T
import warnings

from cvargparse.argument import Argument as Arg
from cvargparse.factory import BaseFactory
from cvargparse.utils.logger_config import init_logging_handlers

class LoggerMixin(abc.ABC):

	def __init__(self, *args, nologging: bool = False, **kw):
		self._nologging = nologging
		super().__init__(*args, **kw)

		if not self.has_logging: return

		self.add_args([
			Arg('--logfile', type=str, default='',
				help='file for logging output'),
			Arg('--loglevel', type=str, default='INFO',
				help='logging level. see logging module for more information'),
		], group_name="Logger arguments")

	@property
	def has_logging(self):
		return not self._nologging

	def _logging_config(self, simple=False):

		if self._args.logfile:
			handler = logging.FileHandler(self._args.logfile, mode="w")
		else:
			handler = logging.StreamHandler()

		# fmt = '%(message)s' if simple else '%(levelname)s - [%(asctime)s] %(filename)s:%(lineno)d [%(funcName)s]: %(message)s'
		fmt = '{message}' if simple else '{levelname: ^7s} - [{asctime}] {filename}:{lineno} [{funcName}]: {message}'
		if getattr(self._args, "debug", False):
			lvl = logging.DEBUG
		else:
			lvl = getattr(logging, self._args.loglevel.upper(), logging.WARNING)

		self._logger = init_logging_handlers([(handler, fmt, lvl)])

	def init_logger(self, simple=False):
		warnings.warn("This method is deprecated and does nothing since v0.3.0!",
			DeprecationWarning, stacklevel=2)


class BaseParser(LoggerMixin, argparse.ArgumentParser):

	def __init__(self, arglist: T.Union[T.List[Arg], BaseFactory] = [], *args, **kw):
		self._groups = {}
		self._args = None

		super().__init__(*args, **kw)

		self.add_args(arglist)


	@property
	def args(self):
		return self._args

	def get_group(self, name):
		return self._groups.get(name)

	def has_group(self, name):
		return name in self._groups

	def add_argument_group(self, title, description=None, *args, **kwargs):
		group = super().add_argument_group(title=title, description=description, *args, **kwargs)
		self._groups[title] = group
		return group

	def add_args(self, arglist, group_name=None, group_kwargs={}):

		if isinstance(arglist, BaseFactory):
			arglist = arglist.get()

		if group_name is None:
			group = self
		elif self.has_group(group_name):
			group = self.get_group(group_name)
		else:
			group = self.add_argument_group(group_name, **group_kwargs)

		for arg in arglist:
			if isinstance(arg, Arg):
				group.add_argument(*arg.args, **arg.kw)
			else:
				group.add_argument(*arg[0], **arg[1])

	def parse_args(self, args=None, namespace=None):
		self._args = super().parse_args(args, namespace)

		if self.has_logging:
			self._logging_config()

		return self._args

