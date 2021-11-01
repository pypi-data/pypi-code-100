"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with self source code.
"""

from merchantapi.abstract import Request
from merchantapi.abstract import Response
from merchantapi.abstract import Client

""" 
Handles sending multiple Request objects as one request.
:see: https://docs.miva.com/json-api/multicall
"""

from requests.models import Response as HttpResponse


class MultiCallRequest(Request):
	def __init__(self, client: Client = None, requests: list = None):
		"""
		MultiCallRequest Constructor.

		:param client: Client
		:param requests: list[Request]
		"""

		super().__init__(client)
		self.requests = []
		self.use_iterations = False
		self.auto_timeout_continue = False
		self._initial_response = None

		if isinstance(requests, list):
			self.add_requests(requests)

	def add_request(self, request: Request) -> 'MultiCallRequest':
		"""
		Add a request to be sent.

		:param request: Request
		:returns: MultiCallRequest
		"""

		if isinstance(request, MultiCallRequest):
			for r in request.get_requests():
				r.add_request(r)
		else:
			self.requests.append(request)
		return self

	def get_requests(self) -> list:
		"""
		Get the requests to be sent.

		:returns: list
		"""

		return self.requests

	def set_requests(self, requests: list):
		"""
		Set and override the requests to be sent.

		:param requests: list
		:returns: MultiCallRequest
		"""

		self.requests.clear()
		for r in requests:
			self.add_request(r)
		return self

	def add_requests(self, requests: list):
		"""
		Add requests to be sent.

		:param :Array requests
		:returns:MultiCallRequest
		"""

		for r in requests:
			self.add_request(r)
		return self

	def operation(self, request: Request = None, shared_data: dict = None) -> 'MultiCallOperation':
		"""
		Create an operation instance and add it to the request.

		:param request: Request|list[Request]|None
		:param shared_data: dict|None
		:returns:
		"""

		operation = MultiCallOperation(request, shared_data)
		self.add_operation(operation)
		return operation

	def add_operation(self, operation: 'MultiCallOperation') -> 'MultiCallRequest':
		"""
		Add a operation to be sent.

		:param operation: MultiCallOperation
		:returns: MultiCallRequest
		"""

		self.requests.append(operation)
		return self

	def add_operations(self, operations: list) -> 'MultiCallRequest':
		"""
		Add an array of operations.

		:param: list[MultiCallOperation]
		:returns: MultiCallRequest
		"""

		for o in operations:
			self.add_operation(o)
		return self

	def set_auto_timeout_continue(self, state: bool):
		"""
		Sets the state of the auto continue feature which will automatically fetch remaining data when  timeout occurs

		:param state: bool
		:returns: MultiCallRequest
		"""

		self.auto_timeout_continue = state
		return self

	def to_dict(self) -> dict:
		"""
		Reduce the request to an Object.

		:returns: dict
		"""

		data = {
			'Operations': []
		}

		for r in self.requests:
			merged = r.to_dict()
			merged.update({
				'Function': r.get_function()
			})
			data['Operations'].append(merged)
		return data

	def process_request_headers(self, headers: dict) -> dict:
		"""
		Allows manipulation of the request headers before sending.

		:param headers: dict
		:returns: dict
		"""

		if isinstance(self._initial_response, MultiCallResponse):
			if self._initial_response.timeout:
				headers['RANGE'] = 'Operations=%d-%d' % \
										(self._initial_response.completed + 1, self._initial_response.total)

		return headers

	def create_response(self, http_response: HttpResponse, data: dict) -> 'MultiCallResponse':
		"""
		:param http_response: requests.models.Response
		:param data: dict
		"""

		return MultiCallResponse(self, http_response, data)

	# noinspection PyTypeChecker
	def send(self) -> 'MultiCallResponse':
		return super().send()


""" 
Handles multicall response.
:see: https://docs.miva.com/json-api/multicall
"""


class MultiCallResponse(Response):
	def __init__(self, request: MultiCallRequest, http_response: HttpResponse, data: dict):
		"""
		MultiCallResponse constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, [])  # init super with no data

		self.responses = []
		self.timeout = False
		self.completed = 0
		self.total = 0

		# If we are continuing, we just set the data and let the initiating response handle it
		# Also if we did not receive an array of objects, we must have encountered some error
		if request._initial_response is not None or not isinstance(data, list):
			self.data = data
			return

		self._append_response_data(data)

		if self.http_response.status_code == 206:
			self.timeout = True
			try:
				self.completed, self.total = self._read_content_range(self.http_response.headers['Content-Range'])
			except KeyError:
				pass

			if not self.total:
				raise MultiCallException('Unexpected format', self.request, self)
			elif self.completed > self.total:
				raise MultiCallException('Completed exceeds total', self.request, self)
			elif self.total != len(self.request.get_requests()):
				raise MultiCallException('Total does not match request count', self.request, self)

		if self.timeout and self.request.auto_timeout_continue:
			self._process_continue()

		if not self.timeout and len(request.get_requests()) != len(self.data):
			raise MultiCallException('Resulting data does not match request count %d vs %d' % (len(request.get_requests()), len(self.data)), self.request, self)

		requests = request.get_requests()

		for index, rdata in enumerate(self.data, 0):
			crequest = requests[index]
			if crequest is None:
				raise MultiCallException('Unable to match response data chunk to request object', self.request, self)

			if isinstance(crequest, MultiCallOperation):
				for opindex, oprequest in enumerate(crequest.get_requests(), 0):
					self.add_response(oprequest.create_response(http_response, rdata[opindex]))
			else:
				self.add_response(crequest.create_response(http_response, rdata))

	def _append_response_data(self, data):
		"""
		Appends response data to be later processed into Response objects
		:param data:
		:return:
		"""

		if not isinstance(self.data, list):
			self.data = []

		if isinstance(data, dict):
			self.data.append(data)
		elif isinstance(data, list):
			for i in range(len(data)):
				self.data.append(data[i])

	def _process_continue(self):
		"""
		Processes the auto continue feature until completion or error
		:return:
		"""

		self.request._initial_response = self

		while self.completed != self.total:
			response = self.request.send()

			if not isinstance(response.data, list):
				raise MultiCallException('Expected an array of dict', self.request, self)

			self._append_response_data(response.data)

			try:
				completed, total = self._read_content_range(response.http_response.headers['Content-Range'])
				self.completed = self.completed + completed
			except KeyError:
				if (self.total - self.completed) == len(response.data):
					self.completed = self.total
		self.timeout = False
		self.request._initial_response = None

	@staticmethod
	def _read_content_range(range: str) -> (int, int):
		"""
		Reads the content range header into its parts
		:param range: str
		:return: (int,int)
		"""

		ranges = range.split('/')
		completed = 0
		total = 0

		if len(ranges) == 2:
			completed = int(ranges[0])
			total = int(ranges[1])

		return completed, total

	def is_success(self):
		"""
		:returns: bool
		"""

		return not self.is_timeout() and isinstance(self.data, list)

	def is_timeout(self):
		"""
		:returns: bool
		"""

		return self.timeout


	def get_responses(self) -> list:
		"""
		Get the responses.

		:returns: list[Response]
		"""

		return self.responses

	def add_response(self, response: Response) -> 'MultiCallResponse':
		"""
		Add a response.

		:param response: Response
		:returns: MultiCallResponse
		:raises ExceptionException:
		"""

		self.responses.append(response)
		return self

	def set_responses(self, responses: list) -> 'MultiCallResponse':
		"""
		Set and overwrite the responses.

		:param responses: list[Response]
		:returns: MultiCallResponse
		"""

		for response in responses:
			self.add_response(response)
		return self


""" 
Handles creation of an Operation with Iterations.

:see: MultiCallRequest
"""


class MultiCallOperation:
	def __init__(self, request: Request = None, shared_data: dict = None):
		"""
		MultiCallOperation Constructor.

		:param request: Request or list[Request]
		:param shared_data: dict
		"""

		self.requests = []

		if shared_data is not dict:
			shared_data = {}

		self.shared_data = shared_data

		if isinstance(request, Request):
			self.add_request(request)
		elif isinstance(request, list):
			for r in request:
				self.add_request(r)

	def get_function(self):
		if len(self.requests) > 0:
			return self.requests[0].get_function()
		return None

	def add_request(self, request: Request) -> 'MultiCallOperation':
		"""
		Add a request iteration.

		:param request: Request
		:returns: MultiCallOperation
		:raises Exception:
		"""

		if isinstance(request, MultiCallRequest):
			raise MultiCallException('Can\'t nest a MultiCallRequest in a MultiCallOperation')
		self.requests.append(request)
		return self

	def get_requests(self):
		"""
		Get the request iterations.

		:returns: list
		"""

		return self.requests

	def set_requests(self, requests: list) -> 'MultiCallOperation':
		"""
		Set and override the request iterations.

		:param requests: list[Request]
		:returns: MultiCallOperation
		:raises MultiCallException:
		"""

		self.requests = []
		for r in requests:
			self.add_request(r)
		return self

	def add_requests(self, requests: list) -> 'MultiCallOperation':
		"""
		Add an array of requests iterations.

		:param requests: list[Request]
		:returns: MultiCallOperation
		:raises MultiCallException:
		"""

		for r in requests:
			self.add_request(r)
		return self

	def add_shared_data(self, key: str, value) -> 'MultiCallOperation':
		"""
		Add a shared data value for key.

		:param key: str
		:param value: str|dict
		:returns: MultiCallOperation
		"""

		self.shared_data[key] = value
		return self

	def set_shared_data(self, values: dict) -> 'MultiCallOperation':
		"""
		Set the shared data object.

		:param values: dict
		:returns: MultiCallOperation
		"""

		self.shared_data = values
		return self

	def get_shared_data(self) -> dict:
		"""
		Get the shared data between the iterations.

		:returns: dict
		"""

		return self.shared_data

	def to_dict(self) -> dict:
		"""
		Reduce the operation to a dict

		:returns: dict
		"""

		if not len(self.requests):
			return {}

		data = self.shared_data.copy()
		data.update({
			'Function': self.requests[0].get_function(),
			'Iterations': []
		})

		for r in self.requests:
			data['Iterations'].append(r.to_dict())
		return data


'''
MultiCallException
'''


class MultiCallException(Exception):
	def __init__(self, message: str, request: MultiCallRequest = None, response: MultiCallResponse = None, other: Exception = None):
		"""
		Constructor
		:param message:
		:param request:
		:param response:
		:param other:
		"""
		super().__init__(message)
		self.request = request
		self.response = request
		self.other = other

	def get_request(self) -> MultiCallRequest:
		"""
		Get the MultiCallRequest object being sent, if applicable
		:return: MultiCallRequest
		"""

		return self.request

	def get_response(self) -> MultiCallResponse:
		"""
		Get the MultiCallResponse object at the state of the error, if applicable
		:return: MultiCallResponse
		"""

		return self.response


	def get_other(self) -> Exception:
		"""
		Get the passed Exception, if available
		:return: Exception|None
		"""

		return self.other
