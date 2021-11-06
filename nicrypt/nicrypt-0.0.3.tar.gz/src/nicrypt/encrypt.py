#!/usr/bin/env python

from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os, fire, sys



env_vars = {
	'key': os.environ.get('ENC_PASSWORD'),
	'salt': os.environ.get('ENC_SALT')
}


class Ncrypt:
	try:
		key = env_vars.get('key')
		salt = env_vars.get('salt')
	except Exception:
		print('Ncrypt requires encyption key and salt!')
	
	def __init__(self,text):
		self.text = text

	def integrity(cls):
		return {
			'key': str.encode(cls.key),
			'salt': str.encode(cls.salt)
		}

	def enc_string(self):
		kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=self.integrity().get('salt'), iterations=100000)
		key = base64.urlsafe_b64encode(kdf.derive(self.integrity().get('key')))
		enc = Fernet(key)
		encText = enc.encrypt(str.encode(self.text)).decode("utf-8")
		return encText

	def dec_string(self):
		enc_text = str.encode(self.text)
		kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=self.integrity().get('salt'), iterations=100000)
		key = base64.urlsafe_b64encode(kdf.derive(self.integrity().get('key')))
		enc = Fernet(key)
		try:
			decText = enc.decrypt(enc_text).decode("utf-8")
			return decText
		except Exception as e:
			return f'can only decrypt encrypted text!'






def ficha(text,arg):
	if arg == 'enc':
		try:
			return Ncrypt(f'{text}').enc_string()
		except Exception as e:
			return e
	elif arg == 'dec':
		encrypted = f'{text}'
		try:
			return Ncrypt(encrypted).dec_string()
		except Exception as e:
			return e
	else:
		return 'invalid argument!  see --help for more details'


if __name__ == '__main__':
	fire.Fire(ficha)