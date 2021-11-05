from utility.config import Config
from utility.logger_handler import Logger

class DB():
    client = None

    def __init__(self, name, logger: Logger = None):
        self.name = name
        self.db_uri = Config.db_uri
        self.logger = Logger(Config.name).get_logger()
        self.get_connection()

    def get_connection(self):
        raise NotImplemented

    def log(self, message: str):
        if self.logger is not None:
            self.logger.debug(message)
        else:
            print(message)