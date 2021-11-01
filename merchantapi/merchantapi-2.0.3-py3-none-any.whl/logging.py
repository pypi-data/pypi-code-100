"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

from merchantapi.abstract import Model, Request, Response
import abc
import sys

'''
Logger

Abstract logger
'''


class Logger:
	def log_request(self, request: Request, headers: dict, content: bytes):
		"""
		Logs the Request headers and content
		:param request:
		:param headers:
		:param content:
		:return:
		"""
		self.write_line(f'\r\n============= Request: {request.get_function()} [HEADERS] =============\r\n')
		for k, v in headers.items():
			self.write_line(f"{k} = {v}")

		self.write_line(f'\r\n============= Request: {request.get_function()} [BODY] =============\r\n')
		self.write_line(content.decode('utf-8'))

	def log_response(self, response: Response, headers: dict, content: bytes):
		"""
		Logs the Response headers and content

		:param response:
		:param headers:
		:param content:
		:return:
		"""
		func = response.request.get_function() if response is not None else ''
		self.write_line(f'\r\n============= Response: {func} [HEADERS] =============\r\n')
		for k, v in headers.items():
			self.write_line(f"{k} = {v}")

		self.write_line(f'\r\n============= Response: {func} [BODY] =============\r\n')
		self.write_line(content.decode('utf-8'))

	@abc.abstractmethod
	def write(self, data: str):
		raise Exception('Method must be implemented by inheritor')

	@abc.abstractmethod
	def write_line(self, data: str):
		raise Exception('Method must be implemented by inheritor')


'''
ConsoleLogger

Logs Request and Responses to STDOUT or STDERR
'''


class ConsoleLogger(Logger):
	DESTINATION_STDOUT = 'stdout'
	DESTINATION_STDERR = 'stderr'

	def __init__(self, destination: str):
		"""
		Constructor

		:param destination: DESTINATION_STDOUT|DESTINATION_STDERR
		"""

		self.destination = destination

	def write(self, data: str):
		"""
		Writes data to stdout/err
		:param data:
		:return:
		"""
		if self.destination == ConsoleLogger.DESTINATION_STDERR:
			sys.stderr.write(data)
		else:
			sys.stdout.write(data)

	def write_line(self, data: str):
		"""
		Writes data to stdout/err
		:param data:
		:return:
		"""
		self.write(data + '\r\n')


'''
FileLogger

Logs Request and Responses to a file
'''


class FileLogger(Logger):
	def __init__(self, file_path: str):
		"""
		Constructor

		:param file_path:
		"""
		self.file_path = file_path
		self.file = open(file_path, 'a+')

	def __del__(self):
		"""
		Destructor

		:return:
		"""
		if not self.file.closed:
			self.file.close()

	def write(self, data: str):
		"""
		Writes data to stdout/err
		:param data:
		:return:
		"""
		self.file.write(data)

	def write_line(self, data: str):
		"""
		Writes data to stdout/err
		:param data:
		:return:
		"""
		self.write(data + '\r\n')
