from typing import Dict

from pydantic import BaseModel


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str
    LOG_FORMAT_EXTENDED: str = (
        "%(service_name)s | "
        "%(ipv4)s | "
        "%(env)s | "
        "%(trace_id)s | "
        "%(correlation_id)s | "
        "%(user_id)s | "
        "%(levelprefix)s | "
        "%(asctime)s | "
        "%(message)s"
    )
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "file": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT_EXTENDED,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: Dict = {}
    loggers: Dict = {}


def get_config(microservice_name, file_path):
    config = LogConfig(LOGGER_NAME=microservice_name).dict()
    config["loggers"][microservice_name] = {
        "handlers": ["file"],
        "level": config["LOG_LEVEL"],
    }

    config["handlers"]["file"] = {
        "formatter": "file",
        "class": "logging.FileHandler",
        "filename": file_path or "logfile.log",
        "level": "DEBUG",
    }
    return config
