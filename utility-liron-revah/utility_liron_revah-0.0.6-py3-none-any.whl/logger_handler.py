import logging
import logging.handlers
from utility.config import Config
from utility.path_handler import PathHandler
from cmreslogging.handlers import CMRESHandler

class Logger:
    logger: logging = None

    def __init__(self, name: str, path: str = None, logger=None, backupCount: int = 10):
        logging.raiseExceptions = Config.env == "Development"
        self.logger = self.start(name, path, logger, backupCount)

    def get_logger(self):
        return self.logger

    # input - logName as string, logPath as string, logger as logging class
    # output - logger as logging class
    # do - set logger settings
    @staticmethod
    def start(log_name: str = 'test', log_path: str = None, logger=None, backupCount: int = 10):
        name = log_name.replace('.log', '')
        path = log_path if log_path is not None else f"{PathHandler.get_path()}/logs"
        new_logger = logging.getLogger(name) if logger is None else logger
        
        new_logger.setLevel(logging.DEBUG)  # level per system status
        msg = '%(asctime)s %(levelname)s %(module)s %(name)s: %(message)s'
        formatter = logging.Formatter(msg, datefmt='%d-%m-%Y %H-%M-%S')
    
        # Stream Handler - cmd line
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        # CMRES Handler - Elastic
        http_handler = CMRESHandler(hosts=[{'host': Config.elastic_url, 'port': Config.elastic_port}], es_index_name=name, 
                            auth_type=CMRESHandler.AuthType.NO_AUTH, es_additional_fields={'App': Config.name, 'Environment': Config.env})
        
        # File handler
        PathHandler.create_dir(path)
        file_handler = logging.handlers.RotatingFileHandler(f"{path}/{name}.log", maxBytes=10485760, 
                            backupCount=backupCount, encoding="UTF-8")
        file_handler.setFormatter(formatter)
        
        # adding Handlers
        new_logger.addHandler(file_handler)
        new_logger.addHandler(http_handler)
        new_logger.addHandler(stream_handler)

        new_logger.info('Initialize Logger')
        return new_logger
