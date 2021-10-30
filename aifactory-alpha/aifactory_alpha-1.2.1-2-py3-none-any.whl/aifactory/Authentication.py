from aifactory.constants import *
from Cryptodome import Random
from Cryptodome.Cipher import AES
from random import random
from hashlib import blake2b
import json
import requests
import http
import time
import os
import logging

BLOCK_SIZE=16

class AFAuth():
    submit_key = None
    task_id = None
    user_id = None
    def __init__(self, logger=None, user_email=None, task_id=None,
                 submit_key=None, submit_key_path=None, log_dir='./log',
                 password=None, auth_method=AUTH_METHOD.USERINFO, encrypt_mode=True,
                 auth_url=AUTH_DEFAULT_URL, debug=False):
        self.logger = logger
        if self.logger is None:
            self.set_log_dir(log_dir)
        self.auth_method = auth_method
        self.encrypt_mode = int(encrypt_mode)
        self.auth_url = auth_url
        self.debug = debug
        self.set_auth_method(auth_method, debug=debug, submit_key_path=submit_key_path, submit_key=submit_key,
                             user_email=user_email, task_id=task_id)
        if encrypt_mode:
            self.crypt = AFCrypto()

    def set_log_dir(self, log_dir: str):
        self.log_dir = os.path.abspath(log_dir)
        if not os.path.exists(self.log_dir):
            os.mkdir(self.log_dir)
        if not os.path.isdir(self.log_dir):
            raise AssertionError("{} is not a directory.".format(self.log_dir))
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(module)s:%(levelname)s: %(message)s')
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

    def __reset_logger__(self, prefix=LOG_TYPE.DEFAULT):
        cur_log_file_name = prefix+datetime.now().__str__().replace(" ", "-").replace(":", "-").split(".")[0]+".log"
        log_path = os.path.join(self.log_dir, cur_log_file_name)
        file_handler = logging.FileHandler(log_path)
        formatter = logging.Formatter('%(asctime)s:%(module)s:%(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.log_path = log_path

    def set_auth_method(self, auth_method, debug=False,
                        submit_key_path=None, submit_key=None,  # auth method is key
                        user_email=None, task_id=None):  # auth method is user-info
        self.auth_method = auth_method
        if self.auth_method == AUTH_METHOD.KEY:
            if debug:
                submit_key = DEBUGGING_PARAMETERS.KEY
            self.set_submit_key(submit_key_path, submit_key)
        elif auth_method==AUTH_METHOD.USERINFO:
            raise(AuthMethodNotAvailableError)
            self.set_user_email(user_email)
            self.set_task_id(task_id)
        else:
            raise(WrongAuthMethodError)

    def set_submit_key(self, key_path=None, key=None):
        if key_path is None and key is None:
            raise (KeyNotGivenError)
        elif key_path is not None:
            with open(key_path) as f:
                self.submit_key = f.read()
        elif key is not None:
            self.submit_key = key

    def set_user_email(self, email: str):
        self.user_email = email

    def set_task_id(self, task_id: int):
        self.task_id = task_id

    def _investigate_validation_(self):
        res = []
        if self.auth_method == AUTH_METHOD.KEY:
            if self.submit_key is None:
                res.append(KeyNotGivenError)
        elif self.auth_method == AUTH_METHOD.USERINFO:
            if self.user_email is None:
                res.append(UserInfoNotDefinedError)
            if self.task_id is None:
                res.append(TaskIDNotDefinedError)
        else:
            res = res.append(WrongAuthMethodError)
        for r in res:
            self.logger.error(r.ment)
        return res

    def _require_submit_key_(self):
        self.logger.info("Please enter your submit key.")
        self.logger.info("The key can be found from our website: http://aifactory.space")
        self.logger.info("제출용 키를 입력해주세요.")
        self.logger.info("제출용 키는 저희 홈페이지의 참가중이신 태스크 페이지에서 내려받으실 수 있습니다: http://aifactory.space")
        submit_key = None
        if self.debug:
            submit_key = DEBUGGING_PARAMETERS.KEY
        else:
            submit_key = input("Submit Key: ")
        return submit_key

    def _require_user_id_(self):
        user_id = None
        if self.debug:
            user_id = DEBUGGING_PARAMETERS.USER_NAME
        else:
            user_id = input("Please enter your user email: ")
        user_id = self.crypt.encrypt_aes(user_id, key=AIFACTORY_VERSION)
        return user_id

    def pack_user_info(self, params: dict):
        hashed_password = self._require_password_()
        if self.encrypt_mode:
            hashed_password = self.crypt.encrypt_aes(hashed_password, self.user_email)
        params[AUTH_REQUEST_KEYS.PASSWORD] = hashed_password
        params[AUTH_REQUEST_KEYS.PASSWORD_ENCRYPTED_STATUS] = self.encrypt_mode
        return params

    def pack_submit_key(self, params: dict):
        submit_key = None
        if self.encrypt_mode:
            submit_key = self.crypt.encrypt_aes(self.submit_key, AIFACTORY_VERSION)
        params[AUTH_REQUEST_KEYS.SUBMIT_KEY] = submit_key
        params[AUTH_REQUEST_KEYS.KEY_ENCRYPTED_STATUS] = 'True' # this should be changed.
        return params

    def _check_submit_key_validity_(self):
        params = {AUTH_REQUEST_KEYS.AUTH_METHOD: self.auth_method,
                  AUTH_REQUEST_KEYS.AIFACTORY_VERSION: AIFACTORY_VERSION}
        params = self.pack_submit_key(params)
        response = requests.get(self.auth_url + AUTH_ENDPOINT, params=params)
        self.logger.info('Response from auth server: {}'.format(response.text))
        if response.text == AUTH_RESPONSE.KEY_VALID:
            self.logger.info('Submit key validity checked.')
            return True
        elif response.text == AUTH_RESPONSE.VERSION_NOT_VALID:
            self.logger.info("Authentication failed. \nPlease check if you have the right version.")
            self.logger.info("Try installing the updated version of aifactory-alpha.")
            exit(1)
        elif response.status_code == http.HTTPStatus.OK:
            self.logger.warn("Authentication failed. Please check if your submit key is valid.")
            self.logger.info("제출 키가 유효하지 않습니다. 다시 한 번 확인해주세요.")
            return False
        else:
            self.logger.warn("Authentication procedure not available.")
            self.logger.warn("Skip the submit key validity check.")
        return True

    def request_submit_key(self, user_id):
        self.__reset_logger__(LOG_TYPE.KEY_REQUEST)
        if user_id is None:
            user_id = self._require_user_id_()
        params = {AUTH_REQUEST_KEYS.VERSION: AIFACTORY_VERSION,
                  AUTH_REQUEST_KEYS.USER_ID: self.user_id}

        response = requests.get(self.auth_url+KEYREQUEST_ENDPOINT, params=params)
        self.logger.info('Response from auth server: {}'.format(response.text))

        if response.text in [AUTH_RESPONSE.USER_NOT_EXIST, AUTH_RESPONSE.USER_NOT_PARTICIPATING]:
            self.logger.error(response.text)
        elif response.text == AUTH_RESPONSE.KEY_REQUEST_SECESSFUL:
            self.logger.info("Submission Key Requested.")
            self.logger.info("Please check your email including SPAM mail box")
        else:
            self.logger.error("This service is not available.")
            self.logger.error("Please contact to AI Factory to receive your key.")

    def get_submit_key(self, num_trial=0, refresh=False):
        if num_trial >= MAXIMUM_SUBMISSION_TRIAL:
            return False
        if refresh: self.submit_key = None
        if self.auth_method == AUTH_METHOD.KEY:
            if self.submit_key is None:
                self.submit_key = self._require_submit_key_()
                return self.get_submit_key(num_trial+1)
            else:
                if self._check_submit_key_validity_():
                    return self.submit_key
                else:
                    return self.get_submit_key(num_trial+1, refresh=True)

        res = self._investigate_validation_()
        if len(res) != 0:
            return False

        params = {AUTH_REQUEST_KEYS.AUTH_METHOD: self.auth_method, AUTH_REQUEST_KEYS.VERSION: AIFACTORY_VERSION,
                  AUTH_REQUEST_KEYS.TASK_ID: self.task_id, AUTH_REQUEST_KEYS.USER_ID: self.user_id}
        if self.auth_method == AUTH_METHOD.USERINFO or self.submit_key is None:
            params = self.pack_user_info(params)

        response = requests.get(self.auth_url+AUTH_ENDPOINT, params=params)
        self.logger.info('Response from auth server: {}'.format(response.text))

        if response.text == AUTH_RESPONSE.KEY_NOT_VALID:
            self.logger.error(KeyNotValidError.ment)
            raise(KeyNotValidError)
        elif response.text == AUTH_RESPONSE.USER_NOT_PARTICIPATING:  # if the user hasn't registered in the task.
            self.logger.error(UserNotRegisteredError.ment)
            raise(UserNotRegisteredError)
        elif response.text == AUTH_RESPONSE.NO_AVAILABLE_LAP:  # if there isn't any lap to submit the result.
            self.logger.error(TaskIDNotAvailableError.ment)
            raise(TaskIDNotAvailableError)
        elif response.text == AUTH_RESPONSE.DB_NOT_AVAILABLE:  # if the system has a problem.
            self.logger.error(AuthServerError.ment)
            raise(AuthServerError)
        elif response.text in [AUTH_RESPONSE.USER_NOT_EXIST, AUTH_RESPONSE.PASSWORD_NOT_VALID]:
            # if the user information was wrong
            if num_trial > AUTH_METHOD.MAX_TRIAL:
                return False
            self.logger.info('Authentication failed. Please check your user info and try again.')
            self.logger.info(self.summary())
            self.logger.info('Please check you have the right password and email that you use to log-in the AI Factory Website.')
            time.sleep(1)
            return self.get_submit_key(num_trial + 1)
        elif response.text == AUTH_RESPONSE.VERSION_NOT_VALID:
            self.logger.info("Authentication failed. \nPlease check if you have the right version.")
            self.logger.info("Try installing the updated version of aifactory-alpha.")
            exit(1)
        elif response.status_code == http.HTTPStatus.OK:
            submit_key_response = json.loads(response.text)
            self.submit_key = self.crypt.decrypt_aes(submit_key_response[AUTH_REQUEST_KEYS.SUBMIT_KEY], AIFACTORY_VERSION)
            if self.auth_method == AUTH_METHOD.USERINFO:
                self.submit_key = self.crypt.decrypt_aes(submit_key_response[AUTH_REQUEST_KEYS.SUBMIT_KEY], AIFACTORY_VERSION)
                self.auth_method = AUTH_METHOD.KEY
            self.logger.info('Authentication successful.')
            return self.submit_key
        return False

    def summary(self):
        _summary_ = ">>> User Authentication Info <<<\n"
        _summary_ += "Authentication Method:"
        if self.auth_method is AUTH_METHOD.KEY:
            _summary_ += "Submit Key \n"
            _summary_ += "    Submit Key: {} \n".format(self.submit_key)
        elif self.auth_method is AUTH_METHOD.USERINFO:
            _summary_ += "User Information \n"
            _summary_ += "    Task ID: {}\n".format(self.task_id)
            _summary_ += "    User e-mail: {}\n".format(self.user_email)
        return _summary_


class AFCrypto():
    LENGTH_PREFIX = 6
    def __init__(self):
        self.iv = bytes([0x00] * 16) #pycryptodomex 기준

    def encrypt_aes(self, data: str, key: str):
        key += '0'*(16 - (len(key) % 16))
        key = key.encode()
        crypto = AES.new(key, AES.MODE_CBC, self.iv)
        len_data = str(len(data))
        data = len_data.zfill(6) + data
        while len(data) % 16 != 0:
            data += str(int(random()))
        data = data.encode()
        enc = crypto.encrypt(data)
        del crypto
        return enc.hex()

    def decrypt_aes(self, enc: str, key: str):
        key += '0'*(16 - (len(key) % 16))
        key = key.encode()
        crypto = AES.new(key, AES.MODE_CBC, self.iv)
        enc = bytes.fromhex(enc)
        dec = crypto.decrypt(enc).decode()
        len_dec = int(dec[:self.LENGTH_PREFIX])
        dec = dec[self.LENGTH_PREFIX:self.LENGTH_PREFIX+len_dec]
        del crypto
        return dec

    def zero_salting(self, data: str):
        data += '0'*(AUTH_METHOD.SALTED_LENGTH - len(data))
        return data

    def encrypt_hash(self, data: str, zero_salting=True, salt=None):
        if zero_salting:
            data = self.zero_salting(data)
        elif salt is not None:
            data += salt
        return blake2b(data.encode()).hexdigest()


if __name__ == "__main__":
    a = AFCrypto()
    target = "The key is how I think of you."
    sample_key = 'i_love_you_:)'
    print("Target pattern to encrypt: %s" % target)
    print("A key for encryption: %s" % sample_key)
    b = a.encrypt_aes(target, sample_key)
    print("Encrypted Message: %s" % b)
    c = a.decrypt_aes(b, sample_key)
    print("Decrypted Message: %s" % c)
