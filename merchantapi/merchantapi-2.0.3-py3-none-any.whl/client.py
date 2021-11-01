"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with self source code.
"""

import requests
import time
import json
from merchantapi.abstract import Request, Response
from merchantapi.multicall import MultiCallRequest, MultiCallOperation
from merchantapi.authenticator import Authenticator, TokenAuthenticator, SSHPrivateKeyAuthenticator, SSHAgentAuthenticator
from requests.exceptions import HTTPError, ConnectionError
from logging import Logger

'''
BaseClient - sending API requests

:see: https://docs.miva.com/json-api/#authentication
'''


class BaseClient:
	DEFAULT_OPTIONS = {
		'require_timestamps': True,
		'default_store_code': None,
		'ssl_verify': True,
		'operation_timeout': 60
	}

	def __init__(self, endpoint: str, authenticator: Authenticator, options: dict = None):
		"""
		Constructor
		:param endpoint: The URL to your store's json.mvc
		:param authenticator: The authenticator object used to authenticate requests
		:param options: Dictionary of client options
		"""
		self.set_endpoint(endpoint)
		self.logger = None
		self.options = Client.DEFAULT_OPTIONS.copy()
		self.global_headers = dict()

		if isinstance(options, dict):
			self.options.update(options)

		self.authenticator = authenticator

	def get_endpoint(self) -> str:
		"""
		Get the API endpoint URL.

		:returns: str
		"""

		return self.endpoint

	def set_endpoint(self, endpoint: str) -> 'BaseClient':
		"""
		Set the API endpoint URL.

		:param endpoint: str
		:returns: Client
		"""

		self.endpoint = endpoint
		return self

	def get_option(self, name: str, default=None):
		"""
		Get a client option.

		:param name: str
		:param default: default return value if not set
		:returns: mixed
		"""

		return self.options[name] if name in self.options else default

	def set_option(self, name: str, value) -> 'BaseClient':
		"""
		Set a client option.

		:param name: str
		:param value: mixed
		:returns: Client
		"""

		if name not in self.options:
			raise Exception('Invalid option %s' % name)

		self.options[name] = value
		return self

	def set_logger(self, logger: (Logger, None)) -> 'BaseClient':
		"""
		Set the logger to handle logging request and responses

		:param logger: An instance of Logger or None.
		:return:
		"""

		self.logger = logger
		return self

	def set_authenticator(self, authenticator: Authenticator) -> 'BaseClient':
		"""
		Set the clients authenticator. Default authenticator instance is a TokenAuthenticator
		:param authenticator:
		:return: Client
		:see: merchantapi.authenticator
		"""

		if not isinstance(authenticator, Authenticator):
			raise Exception('Expected instance of Authenticator')
		self.authenticator = authenticator
		return self

	def get_authenticator(self) -> Authenticator:
		"""
		Get the clients authenticator. Default authenticator instance is a TokenAuthenticator
		:return:
		:see: merchantapi.authenticator
		"""

		return self.authenticator
	
	def get_global_headers(self) -> dict:
		"""
		Gets all currently set global headers
		:return:
		"""

		return self.global_headers
	
	def set_global_header(self, key: str, value: str) -> 'BaseClient':
		"""
		Set a global header key and value to be sent with every request made
		:param key: str
		:param value: str
		:return:
		"""

		self.global_headers[key] = value
		return self

	def has_global_header(self, key: str) -> bool:
		"""
		Check to see if a global header is defined
		:param key: str
		:return:
		"""

		return key in self.global_headers

	def get_global_header(self, key: str) -> (str, None):
		"""
		Get a defined global header value or none if it does not exist
		:param key: str
		:return:
		"""

		return self.global_headers[key] if key in self.global_headers else None

	def remove_global_header(self, key: str) -> 'BaseClient':
		"""
		Remove a defined global header if it exists
		:param key: str
		:return:
		"""

		if key in self.global_headers:
			del self.global_headers[key]
		return self

	def send(self, request: Request) -> Response:
		"""
		Send a Request object with callback.

		:param request: Request
		:raises Exception:
		:returns: Response
		"""

		default_store = self.get_option('default_store_code')
		response = None

		if isinstance(request, MultiCallRequest):
			for r in request.get_requests():
				if isinstance(r, MultiCallOperation):
					for o in r.get_requests():
						if o.get_scope() == Request.SCOPE_STORE and \
								o.get_store_code() in (None, '') and default_store not in (None, ''):
							o.set_store_code(default_store)
				else:
					if r.get_scope() == Request.SCOPE_STORE and \
							r.get_store_code() in (None, '') and default_store not in (None, ''):
						r.set_store_code(default_store)

			data = request.to_dict()
		else:
			if request.get_scope() == Request.SCOPE_STORE and \
					request.get_store_code() in (None, '') and default_store not in (None, ''):
				request.set_store_code(default_store)

			data = request.to_dict()
			data.update({'Function': request.get_function()})

		if self.get_option('require_timestamps') is True:
			data['Miva_Request_Timestamp'] = int(time.time())

		data = json.dumps(data).encode('utf-8')

		headers = self.get_global_headers().copy()
		headers.update({
			'Content-Type': 'application/json',
			'Content-Length': str(len(data)),
			'X-Miva-API-Authorization': self.generate_auth_header(data)
		})

		if request.get_binary_encoding() == Request.BINARY_ENCODING_BASE64:
			headers['X-Miva-API-Binary-Encoding'] = Request.BINARY_ENCODING_BASE64

		if Client.DEFAULT_OPTIONS['operation_timeout'] != int(self.get_option('operation_timeout')):
			headers['X-Miva-API-Timeout'] = str(self.get_option('operation_timeout'))

		if self.logger is not None:
			self.logger.log_request(request, headers, data)

		json_response = ''
		http_response = None

		try:
			http_response = requests.post(self.endpoint, data=data, headers=request.process_request_headers(headers), verify=self.get_option('ssl_verify'))

			if 200 <= http_response.status_code < 300:
				json_response = http_response.json()
			
			response = request.create_response(http_response, json_response)

			if http_response.status_code == 401:
				raise ClientHttpAuthenticationError(request, http_response)
			return response
		except ConnectionError as e:
			raise ClientException(request, http_response, e)
		except HTTPError as e:
			raise ClientException(request, http_response, e)
		except ValueError as e:
			raise ClientException(request, http_response, e)
		finally:
			if self.logger is not None and http_response is not None:
				self.logger.log_response(response, http_response.headers, http_response.content)

	def generate_auth_header(self, data: str) -> str:
		"""
		Generates the authentication header value.

		:param data: str
		:returns: str
		"""

		if not isinstance(self.authenticator, Authenticator):
			raise Exception('No authenticator instance')

		return self.authenticator.generate_authentication_header(data)


'''
Client - The default Client. Uses TokenAuthenticator
'''


class Client(BaseClient):
	SIGN_DIGEST_NONE = None
	SIGN_DIGEST_SHA1 = 'sha1'
	SIGN_DIGEST_SHA256 = 'sha256'

	def __init__(self, endpoint: str, api_token: str, signing_key: str, options: dict = None):
		"""
		Constructor
		:param endpoint: The URL to your store's json.mvc
		:param api_token: The api token to authenticate with
		:param signing_key: The base64 string of your api token signing key
		:param options: Dictionary of client options. See BaseClient
		"""
		digest_type = Client.SIGN_DIGEST_SHA256
		if isinstance(options, dict) and 'signing_key_digest' in options:
			digest_type = options['signing_key_digest']
			del options['signing_key_digest']
		super().__init__(endpoint, TokenAuthenticator(api_token, signing_key, digest_type), options)

	def get_api_token(self) -> str:
		"""
		Get the api token used to authenticate the request.

		:returns: str
		"""

		if isinstance(self.authenticator, TokenAuthenticator):
			return self.authenticator.get_api_token()
		return ''

	def set_api_token(self, api_token: str) -> 'Client':
		"""
		Set the api token used to authenticate the request.

		:param api_token: str
		:returns: Client
		"""

		if isinstance(self.authenticator, TokenAuthenticator):
			self.authenticator.set_api_token(api_token)
		return self

	def get_signing_key(self) -> str:
		"""
		Get the HMAC signing key used to sign requests. Base64 encoded.

		:returns: str
		"""
		if isinstance(self.authenticator, TokenAuthenticator):
			return self.authenticator.get_signing_key()
		return ''

	def set_signing_key(self, signing_key: str) -> 'Client':
		"""
		Set the HMAC signing key used to sign requests. Base64 encoded.

		:param signing_key: str
		:returns: Client
		"""

		if isinstance(self.authenticator, TokenAuthenticator):
			self.authenticator.set_signing_key(signing_key)
		return self

	def get_option(self, name: str, default=None):
		"""
		Override base get_option to account for removed option `signing_key_digest`

		:param name:
		:param default:
		:return:
		"""
		if name == 'signing_key_digest':
			if isinstance(self.authenticator, TokenAuthenticator):
				return self.authenticator.get_digest_type()
			return default
		return super().get_option(name, default)

	def set_option(self, name: str, value) -> 'Client':
		"""
		Override base set_option to account for removed option `signing_key_digest`
		:param name:
		:param value:
		:returns: Client
		"""
		if name == 'signing_key_digest':
			if isinstance(self.authenticator, TokenAuthenticator):
				self.authenticator.set_digest_type(value)
			return self
		super().set_option(name, value)
		return self


'''
SSHClient - Use this client to authenticate with ssh private key signing.

The configured username should
'''


class SSHClient(BaseClient):
	def __init__(self, endpoint: str, username: str, private_key_file: str, password: (str, None) = None, digest_type = SSHPrivateKeyAuthenticator.DIGEST_SSH_RSA_SHA256, options: dict = None):
		"""
		Constructor
		:param endpoint: The URL to your store's json.mvc
		:param username: The username of the store user to authenticate with. Make sure it exists in your store
						and has SSHAuthentication enabled with the public key
		:param private_key_file: The path to your private key.
		:param password: The password for your private key. None if no password was used to encrypt the key.
		:param digest_type: Use constants SSHPrivateKeyAuthenticator.DIGEST_SSH_RSA_SHA256 or SSHPrivateKeyAuthenticator.DIGEST_SSH_RSA_SHA512
		:param options: Dictionary of client options. See BaseClient
		"""
		super().__init__(endpoint, SSHPrivateKeyAuthenticator(username, private_key_file, password, digest_type), options)

	def set_private_key(self, private_key_path, password: (str, None) = None) -> 'SSHClient':
		"""
		Set the private key file
		:param private_key_path:
		:param password:
		:return:
		"""
		if isinstance(self.authenticator, SSHPrivateKeyAuthenticator):
			self.authenticator.set_private_key(private_key_path, password)
		return self

	def set_private_key_string(self, private_key, password: (str, None) = None) -> 'SSHClient':
		"""
		Set the private key from a string
		:param private_key:
		:param password:
		:return:
		"""
		if isinstance(self.authenticator, SSHPrivateKeyAuthenticator):
			self.authenticator.set_private_key_string(private_key, password)
		return self

	def set_digest_type(self, digest_type: str) -> 'SSHClient':
		"""
		Set the sign digest type
		:param digest_type:
		:return:
		"""
		if isinstance(self.authenticator, SSHPrivateKeyAuthenticator):
			self.authenticator.set_digest_type(digest_type)
		return self


'''
SSHAgentClient - Use this client to authenticate with ssh private key signing via your local ssh-agent socket
'''


class SSHAgentClient(BaseClient):
	def __init__(self, endpoint: str, username: str, public_key_file: str, digest_type: int = SSHAgentAuthenticator.DIGEST_SSH_RSA_SHA256, agent_socket_path: (str, None) = None, options: (dict, None) = None):
		"""
		Constructor
		:param endpoint: The URL to your store's json.mvc
		:param username: The username of the store user to authenticate with
		:param public_key_file: THe path to your public key.
		:param digest_type: SSHAgentAuthenticator.DIGEST_SSH_RSA_SHA256 or SSHAgentAuthenticator.DIGEST_SSH_RSA_SHA512
		:param agent_socket_path: The path the unix socket of your ssh agent. You can leave this blank to use the
									environment variable SSH_AUTH_SOCK
		:param options: Dictionary of client options

		"""
		super().__init__(endpoint, SSHAgentAuthenticator(username, public_key_file, digest_type, agent_socket_path), options)

	def set_public_key(self, public_key_path) -> 'SSHAgentClient':
		"""
		Set the public key file
		:param public_key_path:
		:return:
		"""
		if isinstance(self.authenticator, SSHAgentAuthenticator):
			self.authenticator.set_public_key(public_key_path)
		return self

	def set_public_key_string(self, public_key: (str, bytes)) -> 'SSHAgentClient':
		"""
		Set the public key from a string.
		You can just copy/paste the a key from the output of `ssh-add -L`
		:param public_key:
		:return:
		"""
		if isinstance(self.authenticator, SSHAgentAuthenticator):
			self.authenticator.set_public_key_string(public_key)
		return self

	def set_digest_type(self, digest_type: int) -> 'SSHAgentClient':
		"""
		Set the sign digest type
		:param digest_type:
		:return:
		"""
		if isinstance(self.authenticator, SSHAgentAuthenticator):
			self.authenticator.set_digest_type(digest_type)
		return self


'''
ClientException
'''


class ClientException(Exception):
	def __init__(self, request: Request = None, http_response: requests.Response = None, other: Exception = None):
		self.request = request
		self.http_response = http_response
		self.other = other

	def get_request(self) -> Request:
		"""
		Get the Request object being sent
		:return: Request
		"""

		return self.request

	def get_http_response(self) -> requests.Response:
		"""
		Get the Response object of the resulting http request, if available
		:return: requests.Response|None
		"""

		return self.http_response

	def get_other(self) -> Exception:
		"""
		Get the passed Exception, if available
		:return: Exception|None
		"""

		return self.other


class ClientHttpAuthenticationError(ClientException):
	pass

