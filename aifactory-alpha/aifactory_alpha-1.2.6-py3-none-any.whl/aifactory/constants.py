AIFACTORY_VERSION = '1.2.4'
SUBMISSION_DEFAULT_URL = 'http://submit-alpha.aifactory.solutions'
SUBMIT_ENDPOINT = '/submit'
LEADERBOARD_ENDPOINT = '/leader_board'
SCORE_ENDPOINT = '/score'
AUTH_DEFAULT_URL = 'http://auth-alpha.aifactory.solutions'
AUTH_ENDPOINT = '/submit_key'
KEYREQUEST_ENDPOINT = '/request_key'

class FILE_STATUS:
    _kb_ = 1024
    _mb_ = 1024*1024
    MAX_FILE_SIZE = 100*_mb_

class FILE_TYPE:
    CSV = 0
    NUMPY = 1
    ZIP = 2
    TAR = 3
    TAR_ZIP = 4
    available_file_extensions = ['csv', 'npy', 'zip', 'tar', 'tar.gz']
    file_type_by_extension = {
                                'csv': CSV, 'npy': NUMPY, 'zip': ZIP, 'tar': TAR, 'tar.gz': TAR_ZIP
                              }
    extension_by_file_type = {
                                CSV: 'csv', NUMPY: 'npy', ZIP: 'zip', TAR: 'tar', TAR_ZIP: 'tar.gz'
                             }

# Authentication method
class AUTH_METHOD:
    USERINFO = 0
    KEY = 1
    MAX_TRIAL = 3
    SALTED_LENGTH = 64
    NUM_KEY_STRETCHING = 2

class AUTH_REQUEST_KEYS:
    AUTH_METHOD = 'auth-method'
    AIFACTORY_VERSION = 'version'
    SUBMIT_KEY = 'submit-key'
    KEY_ENCRYPTED_STATUS = 'is-submit-key-encrypted'
    TASK_ID = 'task-id'
    USER_ID = 'user-id'
    PASSWORD = 'password'
    PASSWORD_ENCRYPTED_STATUS = 'password-encrypted'

class AUTH_RESPONSE:
    SERVICE_NOT_AVAILABLE = 'SERVICE_NOT_AVAILABLE'
    NO_AVAILABLE_LAP = 'NO_AVAILABLE_LAP'
    KEY_VALID = 'KEY_VALID'
    KEY_NOT_VALID = 'KEY_NOT_VALID'
    DB_NOT_AVAILABLE = 'DB_NOT_AVAILABLE'
    USER_NOT_EXIST = 'USER_NOT_EXIST'
    USER_NOT_PARTICIPATING = 'USER_NOT_PARTICIPATING'
    PASSWORD_NOT_VALID = 'PASSWORD_NOT_VALID'
    VERSION_NOT_VALID = 'VERSION_NOT_VALID'
    KEY_REQUEST_SECCESSFUL = 'KEY_REQUEST_SUCCESSFUL'

class SCORING_SERVER_TYPE:
    DAEMON = 'DAEMON'
    API = 'API'

MAXIMUM_SUBMISSION_TRIAL = 5
MAXIMUM_SUBMISSION_TRIAL_PERIOC_SEC = 3600

class SUBMIT_FILES_KEYS:
    FILE = 'file'

class SUBMIT_HEADER_KEYS:
    AIFACTORY_VERSION = 'version'
    SUBMIT_KEY = AUTH_REQUEST_KEYS.SUBMIT_KEY
    KEY_ENCRYPTED_STATUS = AUTH_REQUEST_KEYS.KEY_ENCRYPTED_STATUS
    FILE_TYPE = 'file-type'
    MODEL_PREFIX = 'model-prefix'

class SUBMIT_STATUS:
    RECEIVED = 'RECEIVED'
    SCORING = 'SCORING'
    FAIL = 'FAIL'
    SUCCESS = 'SUCCESS'

class SUBMIT_RESPONSE_KEYS:
    NUM_CURRENT_SUBMISSION = 'num-submit'
    MODEL_NAME = 'model-name'
    SYSTEM_MESSAGE = 'system-message'

class SUBMIT_RESPONSE:
    VERSION_NOT_VALID = 'VERSION_NOT_VALID'
    DB_NOT_AVAILABLE = 'DB_NOT_AVAILABLE'
    SYSTEM_ERROR = 'SYSTEM_ERROR'
    KEY_NOT_VALID = 'KEY_NOT_VALID'
    NO_AVAILABLE_LAP = 'NO_AVAILABLE_LAP'
    USER_NOT_FOUND = 'USER_NOT_FOUND'
    FILE_TYPE_NOT_VALID = 'FILE_TYPE_NOT_VALID'
    TOO_MANY_TRIALS = 'TOO_MANY_TRIALS'

class LEADERBOARD_RESPONSE:
    KEYS = ['LAP', 'RANKING', 'NICKNAME', 'TRIAL', 'SCORE', 'TIMESTAMP']

class SCORE_RESPONSE:
    class KEYS:
        BEST_SCORE = 'BEST_SCORE'
        LATEST_SCORE = 'LATEST_SCORE'
        BEST_RESULT = 'BEST_RESULT'
        LATEST_RESULT = 'LATEST_RESULT'

class DEBUGGING_PARAMETERS:
    KEY = "qkdrma-cnfrmsgoTsmsep-xhlrmsgkrhtlvek"
    USER_NAME = 'user0'
    PASSWORD = 'qlqjs1'

class SUBMIT_RESULT:
    FAIL_TO_SUBMIT = 0
    SUBMIT_SUCCESS = 200

class LOG_TYPE:
    DEFAULT = 'AI_Factory_LOG'
    SUBMISSION = 'SUBMISSION_LOG'
    RELEASE = 'RELEASE_LOG'
    KEY_REQUEST = 'KEY_REQUEST_LOG'
    LEADER_BOARD = 'LEADER_BOARD_LOG'


class KeyNotGivenError(Exception):
    ment = "A path to the key or the string of the key should be given.\n"
    ment += "Please check the usage of the `aifactory-submit` or `aifactory_alpha.API` in the document.\n"
    ment += "http://gitlab.aifactory.solutions/aifactorypd/aifactory-alpha"
    def __repr__(self):
        return self.ment

class KeyNotValidError(Exception):
    ment = "The key you provied is not valid.\n"
    ment += "Please check the validity of your key from our website.\n"
    ment += "http://aifactory.space"

    def __repr__(self):
        return self.ment


class FileTooLargeError(Exception):
    ment = "File size is too large. "
    ment += "Maximum file size is {} MB".format(int(FILE_STATUS.MAX_FILE_SIZE/FILE_STATUS._mb_))
    def __repr__(self):
        return self.ment


class FileTypeNotAvailable(Exception):
    ment = "This type of file is not available. "
    ment += "Available type of files are like below. \n "
    ment += str(FILE_TYPE.available_file_extensions)
    def __repr__(self):
        return self.ment


class SubmitServerError(Exception):
    ment = "The auth server has an error. \n"
    ment += "Please ask the system administrator or try submitting later. \n"
    def __str__(self):
        return self.ment


class AuthServerError(Exception):
    ment = "The auth server has an error. \n"
    ment += "Please ask the system administrator or try submitting later. \n"
    def __str__(self):
        return self.ment


class AuthMethodNotAvailableError(Exception):
    ment = "This auth method is not available in this version. \n"
    ment += "Please check the updated version of aifactory_alpha package. \n"
    def __str__(self):
        return self.ment


class UserInfoNotDefinedError(Exception):
    ment = "You must provide `email` or `user_id` to submit your result."
    def __str__(self):
        return self.ment


class TaskIDNotDefinedError(Exception):
    ment = "You must provide `task_id` to submit your result."
    def __str__(self):
        return self.ment


class WrongAuthMethodError(Exception):
    ment = "Wrong Authentification Method."
    def __str__(self):
        return self.ment


class AuthentificationNotValidError(Exception):
    ment="Information for authentification not enough."
    def __str__(self):
        return self.ment

