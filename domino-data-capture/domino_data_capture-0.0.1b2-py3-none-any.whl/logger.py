import json
from logging import getLoggerClass, addLevelName, setLoggerClass, NOTSET, Formatter, getLogger, FileHandler, INFO, StreamHandler
from logging.handlers import WatchedFileHandler

"""
These values should be in range from 1-9
As 0 is considered no-set level and from 10 we have
standard levels like "Info", "Debug" etc
"""
PREDICTION_FILE = 8
CONSOLE = 9


class PredictionLogger(getLoggerClass()):
    def __init__(self, name, level=NOTSET):
        super().__init__(name, level)
        addLevelName(PREDICTION_FILE, "PREDICTION")
        addLevelName(CONSOLE, "CONSOLE")

    def console(self, msg, *args, **kwargs):
        self._log(CONSOLE, msg, args, **kwargs)

    def prediction(self, msg, *args, **kwargs):
        self._log(PREDICTION_FILE, msg, args, **kwargs)


class PredictionLoggerFactory:

    def __init__(self, filename):
        self.filename = filename
        prediction_handler = self.get_file_handler_with_prediction_level()
        console_handler = PredictionLoggerFactory.get_console_handler()
        setLoggerClass(PredictionLogger)
        prediction_logger = getLogger(__name__)
        if not prediction_logger.handlers:
            prediction_logger.addHandler(prediction_handler)
            prediction_logger.addHandler(console_handler)
        self.logger = prediction_logger

    def get_logger(self) -> PredictionLogger:
        return self.logger

    def get_file_handler_with_prediction_level(self) -> FileHandler:
        formatter = Formatter("%(message)s")
        handler = WatchedFileHandler(filename=self.filename)
        handler.setFormatter(formatter)
        handler.setLevel(PREDICTION_FILE)
        return handler

    @staticmethod
    def get_console_handler() -> StreamHandler:
        formatter = Formatter(
            "The information shown below represents the structure and format of "
            "the prediction data recorded by Domino when this model is deployed "
            "as a Domino Model API\n"
            "\n"
            "%(message)s")
        handler = StreamHandler()
        handler.setFormatter(formatter)
        handler.setLevel(CONSOLE)
        return handler


class PredictionLoggerManager:
    def __init__(self, filename, is_dev_mode):
        self.prediction_logger = PredictionLoggerFactory(filename).get_logger()
        self.is_dev_mode = is_dev_mode

    def record(self, message):
        json_encode_message = json.dumps(message)
        if self.is_dev_mode:
            self.prediction_logger.console(json_encode_message)
        else:
            self.prediction_logger.prediction(json_encode_message)
