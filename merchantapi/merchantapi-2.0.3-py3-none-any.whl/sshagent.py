"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with self source code.
"""

import os
import socket
import struct


'''
SSHAgentMessage

Object wrapper for a generic agent message
'''


class SSHAgentMessage():
	def __init__(self, data: bytes = None):
		"""
		Constructor
		:param data:
		"""
		self.data = data if isinstance(data, bytes) else bytes()

	def parse(self):
		"""
		Parses the response
		:return:
		"""
		pass

	def prepare(self):
		"""
		Prepares the request
		:return:
		"""
		pass

	def len(self) -> int:
		"""
		Get the length of the data
		:return:
		"""
		return len(self.data)

	def append(self, data: bytes):
		"""
		Append to the existing data
		:param data:
		:return:
		"""
		self.data = self.data + data


'''
SSHAgentKey

Object wrapper for single key
'''


class SSHAgentKey:
	def __init__(self, blob: bytes, comment: str):
		"""
		Constructor
		:param blob:
		:param comment:
		"""
		self.blob = blob
		self.comment = comment

	def get_blob(self) -> bytes:
		"""
		Get the key blob
		:return:
		"""
		return self.blob

	def get_comment(self) -> str:
		"""
		Get the key comment
		:return:
		"""
		return self.comment

	def get_key_type(self) -> str:
		"""
		Parse and get the key type from the key blob
		:return:
		"""
		key_type = ''
		if len(self.blob):
			key_type_len, = struct.unpack_from('!I', self.blob, 0)
			if key_type_len > 0:
				key_type, = struct.unpack_from('!{}s'.format(key_type_len), self.blob, struct.calcsize('!I'))
				if isinstance(key_type, bytes):
					key_type = key_type.decode('utf-8')
		return key_type


'''
SSHAgentKeyListResponse

Object wrapper for a agent key list response
'''


class SSHAgentKeyListResponse(SSHAgentMessage):
	def __init__(self, data: bytes = None):
		super().__init__(data)
		self.keys = list()

	def parse(self):
		"""
		Parses the response
		:return:
		"""
		response, key_count = struct.unpack_from('!BI', self.data, 0)

		if response != SSHAgentClient.SSH_AGENT_IDENTITIES_ANSWER:
			raise Exception('Invalid Response')

		offset = struct.calcsize('!BI')

		for i in range(0, key_count):
			key_blob_len, = struct.unpack_from('!I', self.data, offset)
			offset = offset + struct.calcsize('!I')
			key_blob, = struct.unpack_from('!{}s'.format(key_blob_len), self.data, offset)
			offset = offset + key_blob_len
			comment_len, = struct.unpack_from('!I', self.data, offset)
			offset = offset + struct.calcsize('!I')
			comment, = struct.unpack_from('!{}s'.format(comment_len), self.data, offset)
			offset = offset + comment_len
			key = SSHAgentKey(key_blob, comment.decode('utf-8'))
			self.keys.append(key)

	def get_keys(self) -> list:
		return self.keys


'''
SSHAgentSignRequest

Object wrapper for a agent sign request
'''


class SSHAgentSignRequest(SSHAgentMessage):
	def __init__(self, data: bytes = None):
		"""
		Constructor
		:param data:
		"""
		super().__init__(data)
		self.key_blob = bytes()
		self.sign_data = bytes()
		self.sign_type = SSHAgentClient.SSH_AGENT_RSA_SHA2_256

	def set_key_blob(self, blob: bytes):
		"""
		Set the public key blob of the private key the agent should sign with
		:param blob:
		:return:
		"""
		self.key_blob = blob

	def set_sign_data(self, data: bytes):
		"""
		Set the data to sign from bytes
		:param data:
		:return:
		"""
		self.sign_data = data

	def set_sign_data_string(self, data: str):
		"""
		Set the data to sign from a string
		:param data:
		:return:
		"""
		self.sign_data = bytes(data, 'utf-8')

	def set_sign_type(self, sign_type: int):
		"""
		Set the sign type to use
		:param sign_type: int
		:return:
		"""
		if sign_type not in [SSHAgentClient.SSH_AGENT_RSA_SHA2_256, SSHAgentClient.SSH_AGENT_RSA_SHA2_512]:
			raise Exception('Invalid Sign Type')
		self.sign_type = sign_type

	def prepare(self):
		"""
		Parses the request
		:return:
		"""
		self.data = struct.pack('!BI{}sI{}sI'.format(len(self.key_blob), len(self.sign_data)),
			SSHAgentClient.SSH_AGENTC_SIGN_REQUEST,
			len(self.key_blob),
			self.key_blob,
			len(self.sign_data),
			self.sign_data,
			self.sign_type)


'''
SSHAgentSignResponse

Object wrapper for a agent sign response
'''


class SSHAgentSignResponse(SSHAgentMessage):
	def __init__(self, data: bytes = None):
		"""
		Constructor
		:param data:
		"""
		super().__init__(data)
		self.signature_type = ''
		self.signature = bytes()

	def parse(self):
		"""
		Parses the response
		:return:
		"""
		offset = 0
		response, = struct.unpack_from('!B', self.data, offset)
		offset = offset + struct.calcsize('!B')

		if response != SSHAgentClient.SSH_AGENT_SIGN_RESPONSE:
			raise Exception('Invalid Response')

		total_signature_size, = struct.unpack_from('!I', self.data, offset)

		offset = offset + struct.calcsize('!I')

		if total_signature_size + struct.calcsize('!BI') != len(self.data):
			raise Exception('Size Mismatch')

		if not total_signature_size > 0:
			raise Exception('No Signature Received')

		sign_type_len, = struct.unpack_from('!I', self.data, offset)
		offset = offset + struct.calcsize('!I')

		sign_type, = struct.unpack_from('!{}s'.format(sign_type_len), self.data, offset)
		self.signature_type = sign_type.decode('utf-8')
		offset = offset + sign_type_len

		signature_len, = struct.unpack_from('!I', self.data, offset)
		offset = offset + struct.calcsize('!I')
		self.signature, = struct.unpack_from('!{}s'.format(signature_len), self.data, offset)

	def get_signature_type(self):
		"""
		Gets the parsed signature type
		:return:
		"""
		return self.signature_type

	def get_signature(self):
		"""
		Get the parsed signature blob
		:return:
		"""
		return self.signature


'''
SSHAgentClient

Used to connect to and sign data using a local ssh agent socket
'''


class SSHAgentClient():
	SSH_AGENTC_REQUEST_IDENTITIES = 11
	SSH_AGENTC_SIGN_REQUEST = 13

	SSH_AGENT_FAILURE = 5
	SSH_AGENT_SUCCESS = 6
	SSH_AGENT_IDENTITIES_ANSWER = 12
	SSH_AGENT_SIGN_RESPONSE = 14

	SSH_AGENT_RSA_SHA2_256 = 2
	SSH_AGENT_RSA_SHA2_512 = 4

	def __init__(self, agent_socket_path = None):
		"""
		Constructor
		:param agent_socket_path: Optional, defaults to environment value of SSH_AUTH_SOCK
		"""
		self.connection = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		if agent_socket_path is None or not len(agent_socket_path):
			self.agent_socket_path = os.environ.get('SSH_AUTH_SOCK')
		else:
			self.agent_socket_path = agent_socket_path

	def connect(self):
		"""
		Connects to the socket
		:return:
		"""
		self.connection.connect(self.agent_socket_path)

	def disconnect(self):
		"""
		Disconnects from the socket
		:return:
		"""
		try:
			self.connection.close()
		except:
			pass

	def get_key_list(self) -> list:
		"""
		Get a list of keys from the agent
		:return:
		"""
		self.send(SSHAgentMessage(struct.pack('!B', SSHAgentClient.SSH_AGENTC_REQUEST_IDENTITIES)))
		response = SSHAgentKeyListResponse()
		self.receive_into(response)
		return response.get_keys()

	def send(self, message: SSHAgentMessage):
		"""
		Sends a message to the agent
		:param message: SSHAgentMessage
		:return:
		"""
		message.prepare()
		self.connection.sendall(struct.pack('!I', len(message.data)) + message.data)

	def receive(self) -> SSHAgentMessage:
		"""
		Receives a message from the agent
		:return: SSHAgentMessage
		"""
		message = SSHAgentMessage()
		message_size, = struct.unpack('!I', self.connection.recv(struct.calcsize('!I')))
		if message_size > 0:
			message.data = self.connection.recv(message_size)
		message.parse()
		return message

	def receive_into(self, message: SSHAgentMessage) -> int:
		"""
		Receives a message from the agent into the given message object
		:param message: SSHAgentMessage
		:return:
		"""
		message_size, = struct.unpack('!I', self.connection.recv(struct.calcsize('!I')))
		if message_size > 0:
			message.data = self.connection.recv(message_size)
		message.parse()
		return message_size

	def sign_data(self, public_key_blob, sign_type, data) -> (str, bytes):
		"""
		Signs the given data using the given signature type and public key blob
		:param public_key_blob: The public key blob of the private key that should be used by the agent to sign the data
		:param sign_type: The signature type, either SSH_AGENT_RSA_SHA2_256 or SSH_AGENT_RSA_SHA2_512
		:param data: The data to sign
		:return: signature blob
		"""
		request = SSHAgentSignRequest()
		request.set_key_blob(public_key_blob)
		request.set_sign_type(sign_type)

		if isinstance(data, str):
			request.set_sign_data_string(data)
		else:
			request.set_sign_data(data)

		self.send(request)

		response = SSHAgentSignResponse()

		self.receive_into(response)

		return response.get_signature()
