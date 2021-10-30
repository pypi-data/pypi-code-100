import hashlib
import uuid

def hash(text):
	# uuid используется для генерации случайного числа
	salt = uuid.uuid4().hex
	return hashlib.sha256(salt.encode() + text.encode()).hexdigest() + ':' + salt
		    

def password_verify(hashed_password, old_password):
	password, salt = hashed_password.split(':')
	return password == hashlib.sha256(salt.encode() + old_password.encode()).hexdigest()