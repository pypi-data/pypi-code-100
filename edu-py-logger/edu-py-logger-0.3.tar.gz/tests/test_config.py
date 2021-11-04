from unittest import TestCase

from edu_py_logger.config import get_config


class TestLogger(TestCase):
    def test_get_config(self):
        path = "logpath.log"
        frm = (
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
        expected = {
            "LOGGER_NAME": "name",
            "LOG_FORMAT_EXTENDED": frm,
            "LOG_LEVEL": "DEBUG",
            "handlers": {
                "file": {
                    "formatter": "file",
                    "class": "logging.FileHandler",
                    "filename": path,
                    "level": "DEBUG",
                }
            },
            "loggers": {"name": {"handlers": ["file"], "level": "DEBUG"}},
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "file": {
                    "()": "uvicorn.logging.DefaultFormatter",
                    "fmt": frm,
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                }
            },
        }

        result = get_config("name", path)
        self.assertEqual(result, expected)
