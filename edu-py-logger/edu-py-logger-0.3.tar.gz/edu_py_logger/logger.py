import logging
import socket


class LoggerService:
    def __init__(self, microservice_name: str, environment: str):
        self.environment = environment
        ip = socket.gethostbyname(socket.gethostname())
        self.logger = logging.LoggerAdapter(
            logging.getLogger(microservice_name),
            {
                "env": environment,
                "service_name": microservice_name,
                "ipv4": ip,
                "trace_id": "",
                "correlation_id": "",
                "user_id": "",
            },
        )

    def info(self, message, *args, extra=None, **kwargs):
        self.logger.extra = {**self.logger.extra, **(extra or {})}
        self.logger.info(message, *args, **kwargs)

    def debug(self, message, *args, extra=None, **kwargs):
        self.logger.extra = {**self.logger.extra, **(extra or {})}
        self.logger.debug(message, *args, **kwargs)

    def warning(self, message, *args, extra=None, **kwargs):
        self.logger.extra = {**self.logger.extra, **(extra or {})}
        self.logger.warning(message, *args, **kwargs)

    def error(self, message, *args, extra=None, **kwargs):
        self.logger.extra = {**self.logger.extra, **(extra or {})}
        self.logger.error(message, *args, **kwargs)

    def exception(self, message, *args, extra=None, exc_info=True, **kwargs):
        self.logger.extra = {**self.logger.extra, **(extra or {})}
        self.logger.exception(message, *args, exc_info=exc_info, **kwargs)

    def critical(self, message, *args, extra=None, **kwargs):
        self.logger.extra = {**self.logger.extra, **(extra or {})}
        self.logger.critical(message, *args, **kwargs)
