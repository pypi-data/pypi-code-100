from aifactory.Authentication import AFAuth, AFCrypto
from aifactory.constants import *
import pandas as pd
from datetime import datetime
import logging
import os
import requests
import http
import json

class __AFAPIClient__:
    _summary_ = None
    logger = None
    log_path = None
    encrypt_mode = None
    base_header = {AUTH_REQUEST_KEYS.AIFACTORY_VERSION: AIFACTORY_VERSION}

    def __init__(self, debug=False, log_dir="./log/", encrypt_mode=True):
        self.debug = debug
        self.encrypt_mode = int(encrypt_mode)

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

    def __fail__(self, _status_=None):
        self.logger.error("API call Failed.")
        print("Please have a look at the logs in '{}' for more details.".format(self.log_path))
        return _status_

    def __succeed__(self, _status_=None):
        self.logger.info("API call was successful.")
        print("Results are recorded in the log file '{}'.".format(self.log_path))
        return _status_


class AFCompetition(__AFAPIClient__):
    auth_manager = None
    model_name_prefix = None
    encrypt_mode = None
    submit_url = None
    def __init__(self, auth_method=AUTH_METHOD.KEY, submit_key_path=None, submit_key=None,
                 user_email=None, task_id=None, debug=False, encrypt_mode=True,
                 model_name_prefix=None, log_dir="./log/",
                 submit_url=SUBMISSION_DEFAULT_URL, auth_url=AUTH_DEFAULT_URL):
        super().__init__(log_dir=log_dir, encrypt_mode=encrypt_mode)
        self.set_log_dir(log_dir)
        self.model_name_prefix = model_name_prefix
        self.submit_url = submit_url
        self.auth_manager = AFAuth(self.logger, auth_method=auth_method,
                                   submit_key_path=submit_key_path, submit_key=submit_key,
                                   user_email=user_email, task_id=task_id, auth_url=auth_url,
                                   encrypt_mode=encrypt_mode, debug=debug)

    def set_user_email(self, email: str):
        self.auth_manager.set_user_email(email)

    def set_task_id(self, task_id: int):
        self.auth_manager.set_task_id(task_id)

    def set_model_name_prefix(self, model_name_prefix: str):
        self.model_name_prefix = model_name_prefix

    def _is_file_valid_(self, file_path):
        if not os.path.exists(file_path):
            self.logger.error("File {} not found.".format(file_path))
            return False
        elif os.path.getsize(file_path) > FILE_STATUS.MAX_FILE_SIZE:
            self.logger.error(FileTooLargeError.ment)
            return False
        elif ('.'.join(file_path.split('.')[-2:]) != 'tar.gz') and (file_path.split('.')[-1] not in FILE_TYPE.available_file_extensions):
            self.logger.error(FileTypeNotAvailable.ment)
            return False
        return True

    def _send_file_(self, file_path, submit_url=SUBMISSION_DEFAULT_URL, num_trial=0):
        file_type = '.'.join(file_path.split('.')[-2:])
        if file_type != 'tar.gz':
            file_type = file_type.split('.')[-1]
        headers = {SUBMIT_HEADER_KEYS.FILE_TYPE: file_type, SUBMIT_HEADER_KEYS.MODEL_PREFIX: self.model_name_prefix}
        headers = self.auth_manager.pack_submit_key(headers)
        headers[AUTH_REQUEST_KEYS.KEY_ENCRYPTED_STATUS] = b'True'
        response = None
        with open(file_path, 'rb') as f:
            headers.update(self.base_header)
            response = requests.post(submit_url+SUBMIT_ENDPOINT,
                                     files={SUBMIT_FILES_KEYS.FILE: f}, headers=headers)
        if self.debug:
            self.logger.info('Response from submission server: {}'.format(response.text))
        if response.text == SUBMIT_RESPONSE.KEY_NOT_VALID:
            self.logger.info("Key not valid. Starting authentication again.")
            submit_key = self.auth_manager.get_submit_key(num_trial=num_trial+1, refresh=True)
            return self._send_file_(submit_key, file_path, submit_url, num_trial + 1)
        elif response.text == SUBMIT_RESPONSE.FILE_TYPE_NOT_VALID:
            self.logger.info("This type of file is not acceptable for now.")
            self.logger.info("Please check which type of file you have to use for this task.")
            return False
        elif response.status_code == http.HTTPStatus.OK:
            try:
                response_params = json.loads(response.text)
            except:
                self.logger.info("Submission failed.")
                self.logger.info("="*10+"response from the submission server"+"="*10)
                self.logger.info(response)
                self.logger.info(response.text)
                self.logger.info("="*10+"response from the submission server"+"="*10)
                return False
            self.logger.info("Submission completed. Please check the leader-board for scoring result.")
            self.logger.info("You have submitted for {} times.".format(response_params[SUBMIT_RESPONSE_KEYS.NUM_CURRENT_SUBMISSION]))
            self.logger.info("The model name was recorded as {}.".format(response_params[SUBMIT_RESPONSE_KEYS.MODEL_NAME]))
            self.logger.info("Other messages from the submission server: {}.".format(response_params[SUBMIT_RESPONSE_KEYS.SYSTEM_MESSAGE]))
        else:
            self.logger.info("Submission failed.")
            self.logger.info("="*10+"response from the submission server"+"="*10)
            self.logger.info(response)
            self.logger.info("="*10+"response from the submission server"+"="*10)
            return False
        return response

    def submit(self, file_path):
        # This method submit the answer file to the server.
        self.__reset_logger__(LOG_TYPE.SUBMISSION)
        method_list = [self._is_file_valid_, self.auth_manager.get_submit_key, self._send_file_]
        param_list = [[[file_path], {}], [[], {}], [[file_path], {}]]
        status_list = [SUBMIT_RESULT.FAIL_TO_SUBMIT, SUBMIT_RESULT.FAIL_TO_SUBMIT, SUBMIT_RESULT.FAIL_TO_SUBMIT]
        for method, params, status in zip(method_list, param_list, status_list):
            if not method(*params[0], **params[1]):
                return self.__fail__(status)
        return self.__succeed__(SUBMIT_RESULT.SUBMIT_SUCCESS)
        # if not self._is_file_valid_(file_path):
        #     return self.__fail__(self, status)
        # submit_key = self.auth_manager.get_submit_key()
        # if submit_key is False:
        #     return self.__fail__(self, status)
        # response = self._send_file_(file_path)
        # if response is False:
        #     return self.__fail__(self, status)
        # status = SUBMIT_RESULT.SUBMIT_SUCCESS
        # return self.__succeed__(self, status)

    def leader_board(self):
        # This method print the leader board.
        self.__reset_logger__(LOG_TYPE.LEADER_BOARD)
        if not self.auth_manager.get_submit_key():
            return False
        headers = {}
        headers = self.auth_manager.pack_submit_key(headers)
        headers[AUTH_REQUEST_KEYS.KEY_ENCRYPTED_STATUS] = b'True'
        response = None
        response_params = None
        headers.update(self.base_header)
        response = requests.get(self.submit_url + LEADERBOARD_ENDPOINT, headers=headers)
        if response.text == SUBMIT_RESPONSE.KEY_NOT_VALID:
            self.logger.info("Key not valid. Please check if you have the right key.")
            return False
        elif response.status_code == http.HTTPStatus.OK:
            try:
                response_params = json.loads(response.text)
            except:
                self.logger.info("Couldn't call the leader board.")
                self.logger.info("=" * 10 + "response from the submission server" + "=" * 10)
                self.logger.info(response)
                self.logger.info(response.text)
                self.logger.info("=" * 10 + "response from the submission server" + "=" * 10)
                return False
        else:
            self.logger.info("Submission failed.")
            self.logger.info("=" * 10 + "response from the submission server" + "=" * 10)
            self.logger.info(response)
            self.logger.info("=" * 10 + "response from the submission server" + "=" * 10)
            return False
        from aifactory.ascii_arts.titles import LEADER_BOARD
        print(LEADER_BOARD)
        leader_board = pd.DataFrame(response_params, columns=LEADERBOARD_RESPONSE.KEYS)
        leader_board.head()
        return True

    def my_score(self):
        # This method print the leader board.
        self.__reset_logger__(LOG_TYPE.LEADER_BOARD)
        if not self.auth_manager.get_submit_key():
            return False
        headers = {}
        headers = self.auth_manager.pack_submit_key(headers)
        headers[AUTH_REQUEST_KEYS.KEY_ENCRYPTED_STATUS] = b'True'
        response = None
        response_params = None
        headers.update(self.base_header)
        response = requests.get(submit_url + SCORE_ENDPOINT, headers=headers)
        if response.text == SUBMIT_RESPONSE.KEY_NOT_VALID:
            self.logger.info("Key not valid. Please check if you have the right key.")
            return False
        elif response.status_code == http.HTTPStatus.OK:
            try:
                response_params = json.loads(response.text)
            except:
                self.logger.info("Couldn't call the score.")
                self.logger.info("=" * 10 + "response from the submission server" + "=" * 10)
                self.logger.info(response)
                self.logger.info(response.text)
                self.logger.info("=" * 10 + "response from the submission server" + "=" * 10)
                return False
        else:
            self.logger.info("Submission failed.")
            self.logger.info("=" * 10 + "response from the submission server" + "=" * 10)
            self.logger.info(response)
            self.logger.info("=" * 10 + "response from the submission server" + "=" * 10)
            return False
        from aifactory.ascii_arts.titles import BEST_RESULT, LATEST_RESULT
        print(BEST_RESULT)
        print('Best Score:  ', response_params[SCORE_RESPONSE.KEYS.BEST_SCORE])
        print('             ', response_params[SCORE_RESPONSE.KEYS.BEST_RESULT])
        print(LATEST_RESULT)
        print('Latest Score: ', response_params[SCORE_RESPONSE.KEYS.LATEST_SCORE])
        print('              ', response_params[SCORE_RESPONSE.KEYS.LATEST_RESULT])
        return True

    def release(self):
        # This method submit the answer file and the code to the server.
        pass

    def summary(self):
        _summary_ = ">>> Contest Information <<<\n"
        _summary_ += self.auth_manager.summary()
        if self.model_name_prefix is not None:
            _summary_ += "Model Name Prefix: {}\n".format(self.model_name_prefix)
        return _summary_

