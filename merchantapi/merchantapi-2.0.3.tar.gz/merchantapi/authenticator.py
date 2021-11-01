"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with self source code.
"""

import abc
import base64
import hmac
import hashlib
from merchantapi.sshagent import SSHAgentClient
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Hash import SHA512
from Crypto.Signature import pkcs1_15

'''
Abstract base authenticator
'''


class Authenticator:
	@abc.abstractmethod
	def generate_authentication_header(self, data: (str, bytes)) -> str:
		"""
		Generates the authentication header value
		:param data:
		:return:
		"""
		pass

	@abc.abstractmethod
	def sign_data(self, data: (str, bytes)) -> str:
		"""
		Signs the data
		:param data:
		:return:
		"""
		pass


'''
TokenAuthenticator

Authenticates a request using an api token and optional (but default) hmac signature
'''


class TokenAuthenticator(Authenticator):
	DIGEST_NONE = None
	DIGEST_SHA1 = 'sha1'
	DIGEST_SHA256 = 'sha256'

	def __init__(self, api_token: str, signing_key: str, digest_type : str = DIGEST_SHA256):
		"""
		Constructor
		:param api_token:
		:param signing_key:
		:param digest_type:
		"""
		self.api_token = api_token
		self.signing_key = ''
		self.digest_type = digest_type
		self.set_signing_key(signing_key)

	def get_api_token(self) -> str:
		"""
		Get the api token used to authenticate the request.

		:returns: str
		"""

		return self.api_token

	def set_api_token(self, api_token: str) -> 'TokenAuthenticator':
		"""
		Set the api token used to authenticate the request.

		:param api_token: str
		:returns: Client
		"""

		self.api_token = api_token
		return self

	def get_signing_key(self) -> str:
		"""
		Get the HMAC signing key used to sign requests. Base64 encoded.

		:returns: str
		"""

		return self.signing_key

	def set_signing_key(self, signing_key: str) -> 'TokenAuthenticator':
		"""
		Set the HMAC signing key used to sign requests. Base64 encoded.

		:param signing_key: str
		:returns: Client
		"""

		if len(signing_key) % 4 != 0:
			signing_key = signing_key + ('=' * (4 - (len(signing_key) % 4)))

		self.signing_key = signing_key
		return self

	def get_digest_type(self):
		"""
		Get the digest type used to sign the request
		:return:
		"""
		return self.digest_type

	def set_digest_type(self, digest_type: str) -> 'TokenAuthenticator':
		"""
		Set the digest type to sign the request with
		:param type:
		:return:
		"""
		self.digest_type = digest_type.lower() if isinstance(digest_type, str) else digest_type
		return self

	def generate_authentication_header(self, data: (str, bytes)) -> str:
		"""
		Generates the authentication header value
		:param data:
		:return:
		"""
		if self.digest_type in [TokenAuthenticator.DIGEST_SHA1, TokenAuthenticator.DIGEST_SHA256]:
			return 'MIVA-HMAC-%s %s:%s' % (self.digest_type.upper(), self.get_api_token(), self.sign_data(data))
		return 'MIVA %s' % (self.get_api_token())

	def sign_data(self, data: (str, bytes)) -> str:
		"""
		Signs the data
		:param data:
		:return:
		"""
		if self.digest_type == TokenAuthenticator.DIGEST_SHA1:
			return base64.b64encode(hmac.new(base64.b64decode(self.signing_key), data, hashlib.sha1).digest()).decode()
		elif self.digest_type == TokenAuthenticator.DIGEST_SHA256:
			return base64.b64encode(hmac.new(base64.b64decode(self.signing_key), data, hashlib.sha256).digest()).decode()
		else:
			raise Exception('Invalid hmac digest type')


'''
SSHPrivateKeyAuthenticator

Authenticates a requests using an ssh private key to sign the data
'''


class SSHPrivateKeyAuthenticator(Authenticator):
	DIGEST_SSH_RSA_SHA256 = 'rsa256'
	DIGEST_SSH_RSA_SHA512 = 'rsa512'

	def __init__(self, username: str, private_key_file: str, password: (str, None) = None, digest_type: str = DIGEST_SSH_RSA_SHA256):
		"""
		Constructor
		:param username:
		:param private_key_file:
		:param password:
		:param digest_type:
		"""
		self.username = username
		self.private_key_file = private_key_file
		self.password = password
		self.digest_type = digest_type
		self.private_key = None

		if isinstance(private_key_file, str) and len(private_key_file):
			self.set_private_key(private_key_file, password)

	def set_private_key(self, private_key_path, password: (str, None) = None) -> 'SSHPrivateKeyAuthenticator':
		"""
		Set the ssh private key file to be used when signing requests
		:param private_key_path:
		:param password:
		:return:
		"""
		with open(private_key_path, 'rb') as key_file:
			self.set_private_key_string(key_file.read(), password)
		return self

	def set_private_key_string(self, private_key, password: (str, None) = None) -> 'SSHPrivateKeyAuthenticator':
		"""
		Set the ssh private key from a string to be used when signing requests
		:param private_key:
		:param password:
		:return:
		"""
		if not isinstance(private_key, bytes):
			private_key = bytes(private_key, 'utf-8')

		if password != self.password:
			self.password = password

		pw_bytes = None
		if self.password is not None:
			pw_bytes = self.password if isinstance(self.password, bytes) else bytes(self.password, 'utf-8')
		try:
			self.private_key = RSA.import_key(private_key, passphrase=pw_bytes)
		except ValueError as e:
			errstr = str(e).lower()
			if 'incorrect checksum' in errstr:		# OpenSSL Decryption Error
				raise SSHPrivateKeyPasswordError
			elif 'padding is incorrect' in errstr:	# PCKS1 Decryption Error
				raise SSHPrivateKeyPasswordError
			elif 'no passphrase available' in errstr:	# PCKS1 Missing Passphrase
				raise SSHPrivateKeyPasswordError
			raise e

		return self

	def get_digest_type(self) -> str:
		"""
		Get the digest type of the signature hash
		:return:
		"""
		return self.digest_type

	def set_digest_type(self, digest_type: str) -> 'SSHPrivateKeyAuthenticator':
		"""
		Set the digest type for the signature hash
		:param digest_type:
		:return:
		"""
		digest_type = digest_type.lower() if isinstance(digest_type, str) else digest_type
		if digest_type not in [SSHPrivateKeyAuthenticator.DIGEST_SSH_RSA_SHA256, SSHPrivateKeyAuthenticator.DIGEST_SSH_RSA_SHA512]:
			raise Exception('Invalid digest type')
		self.digest_type = digest_type
		return self

	def generate_authentication_header(self, data: (str, bytes)) -> str:
		"""
		Generates the authentication header value
		:param data:
		:return:
		"""
		if self.digest_type == SSHPrivateKeyAuthenticator.DIGEST_SSH_RSA_SHA256:
			return 'SSH-RSA-SHA2-256 %s:%s' % (base64.b64encode(bytes(self.username, 'utf-8')).decode(), self.sign_data(data))
		elif self.digest_type == SSHPrivateKeyAuthenticator.DIGEST_SSH_RSA_SHA512:
			return 'SSH-RSA-SHA2-512 %s:%s' % (base64.b64encode(bytes(self.username, 'utf-8')).decode(), self.sign_data(data))
		else:
			raise Exception('Invalid ssh key digest type')

	def sign_data(self, data: (str, bytes)) -> str:
		"""
		Signs the data
		:param data:
		:return:
		"""
		data_bytes = bytes(data, 'utf-8') if isinstance(data, str) else data

		if self.digest_type == SSHPrivateKeyAuthenticator.DIGEST_SSH_RSA_SHA256:

			return base64.b64encode(pkcs1_15.new(self.private_key).sign(SHA256.new(data))).decode()
		elif self.digest_type == SSHPrivateKeyAuthenticator.DIGEST_SSH_RSA_SHA512:
			return base64.b64encode(pkcs1_15.new(self.private_key).sign(SHA512.new(data))).decode()
		else:
			raise Exception('Invalid ssh key digest type')


'''
SSHPrivateKeyPasswordError

Raised when unable to decrypt the private key
'''

class SSHPrivateKeyPasswordError(Exception):
	pass


'''
SSHAgentAuthenticator

Authenticates a request by signing using a private key via local ssh authentication agent socket.
The private key to sign with is designated by the public key loaded into the authenticator.

'''


class SSHAgentAuthenticator(Authenticator):
	DIGEST_SSH_RSA_SHA256 = SSHAgentClient.SSH_AGENT_RSA_SHA2_256
	DIGEST_SSH_RSA_SHA512 = SSHAgentClient.SSH_AGENT_RSA_SHA2_512

	def __init__(self, username: str, public_key_file: str, digest_type: int = DIGEST_SSH_RSA_SHA256, agent_socket_path: (str, None) = None):
		"""
		Constructor
		:param username:
		:param public_key_file:
		:param agent_socket_path:
		"""
		self.username = username
		self.public_key_file = public_key_file
		self.agent_socket_path = agent_socket_path
		self.public_key = None
		self.ssh_agent = SSHAgentClient(agent_socket_path)
		self.digest_type = digest_type
		self.connected = False

		if isinstance(public_key_file, str) and len(public_key_file):
			self.set_public_key(public_key_file)

	def set_public_key(self, public_key_path) -> 'SSHAgentAuthenticator':
		"""
		Set the ssh public key from a file to be used to identify the key to sign with via the SSH Agent
		:param public_key_path:
		:return:
		"""
		with open(public_key_path, 'rb') as key_file:
			self.set_public_key_string(key_file.read())
		return self

	def set_public_key_string(self, public_key: (str, bytes)) -> 'SSHAgentAuthenticator':
		"""
		Set the ssh public key (from a string) to be used to identify the key to sign with via the SSH Agent
		:param public_key:
		:return:
		"""
		if not isinstance(public_key, bytes):
			public_key = bytes(public_key, 'utf-8')

		self.public_key = RSA.import_key(public_key)
		return self

	def set_ssh_agent_client(self, agent: SSHAgentClient) -> 'SSHAgentAuthenticator':
		"""
		Set the ssh agent client instance
		:param agent:
		:return:
		"""
		self.ssh_agent = agent
		return self

	def get_digest_type(self) -> int:
		"""
		Get the digest type of the signature hash
		:return:
		"""
		return self.digest_type

	def set_digest_type(self, digest_type: int) -> 'SSHAgentAuthenticator':
		"""
		Set the digest type for the signature hash
		:param digest_type:
		:return:
		"""
		digest_type = digest_type.lower() if isinstance(digest_type, str) else digest_type
		if digest_type not in [SSHAgentAuthenticator.DIGEST_SSH_RSA_SHA256, SSHAgentAuthenticator.DIGEST_SSH_RSA_SHA512]:
			raise Exception('Invalid digest type')
		self.digest_type = digest_type
		return self

	def generate_authentication_header(self, data: (str, bytes)) -> str:
		"""
		Generates the authentication header value
		:param data:
		:return:
		"""
		if self.digest_type == SSHAgentAuthenticator.DIGEST_SSH_RSA_SHA512:
			return 'SSH-RSA-SHA2-512 %s:%s' % (base64.b64encode(bytes(self.username, 'utf-8')).decode(), self.sign_data(data))
		return 'SSH-RSA-SHA2-256 %s:%s' % (base64.b64encode(bytes(self.username, 'utf-8')).decode(), self.sign_data(data))

	def sign_data(self, data: (str, bytes)) -> str:
		"""
		Signs the data
		:param data:
		:return:
		"""
		self.ssh_agent.connect()

		key = str(self.public_key.export_key('OpenSSH'))

		key_parts = key.split(' ')

		try:
			sign_data = self.ssh_agent.sign_data(base64.b64decode(key_parts[1]), self.digest_type, data)
		finally:
			self.ssh_agent.disconnect()

		return base64.b64encode(sign_data).decode('utf-8')


