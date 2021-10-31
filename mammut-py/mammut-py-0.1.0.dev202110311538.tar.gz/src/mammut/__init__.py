# coding=utf-8
import os
import configparser
import datetime
import logging.config
from pkg_resources import resource_string
from pytz import reference

__version__ = "0.1.0"

__all__ = ["apps", "data", "common", "linguistics", "models", "visualization"]

ZONED_DATETIME_FORMATTER = "%Y-%m-%dT%H:%M:%S%z"
LOCAL_DATE_FORMATTER = "%Y-%m-%d"
LOCAL_TIME_FORMATTER = "%H:%M:%S"
TIME_SEPARATOR = ":"
TIME_ALTERNATIVE_SEPARATOR = ";"

LOCAL_TIMEZONE = reference.LocalTimezone()


def get_timezone_aware_datetime_min():
    return datetime.datetime.fromtimestamp(0, LOCAL_TIMEZONE)


def get_timezone_aware_datetime_now():
    return datetime.datetime.now(LOCAL_TIMEZONE)


def str_format_datetime(dt):
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=LOCAL_TIMEZONE)
    ncoldts = dt.strftime(ZONED_DATETIME_FORMATTER)
    wcoldts = ncoldts[:-2] + ":" + ncoldts[-2:]
    return wcoldts


def str_parse_datetime(strdt):
    if len(strdt) <= 19:
        strdt = strdt + get_str_format_timezone_aware_datetime_now()[19:]
    elif len(strdt) <= 20:
        strdt = strdt + get_str_format_timezone_aware_datetime_now()[20:]
    strdt = strdt[:-3] + strdt[-2:]
    dt = datetime.datetime.strptime(strdt, ZONED_DATETIME_FORMATTER)
    return dt


def get_str_format_timezone_aware_datetime_now():
    return str_format_datetime(get_timezone_aware_datetime_now())


ES_CONFIGURATIONS = configparser.ConfigParser()
ES_CONFIGURATIONS.read_string(
    resource_string("mammut.resources", "elastic.ini").decode("utf-8")
)
ES_CONFIGURATIONS.read(["data/elastic.ini", "elastic.ini"])

IMAGES_CONFIGURATION = configparser.ConfigParser()
IMAGES_CONFIGURATION.read_string(
    resource_string("mammut.resources", "models.ini").decode("utf-8")
)
IMAGES_CONFIGURATION.read(["data/models.ini", "models.ini"])

if os.environ.get("ELASTIC_HOST") is not None:
    ES_HOST = os.environ.get("ELASTIC_HOST")
else:
    ES_HOST = ES_CONFIGURATIONS["DEFAULT"]["host"]
if os.environ.get("ELASTIC_PORT") is not None:
    ES_PORT = int(os.environ.get("ELASTIC_PORT"))
else:
    ES_PORT = int(ES_CONFIGURATIONS["DEFAULT"]["port"])
if os.environ.get("ELASTIC_USE_SSL") is not None:
    ES_USE_SSL = bool(os.environ.get("ELASTIC_USE_SSL"))
else:
    ES_USE_SSL = bool(ES_CONFIGURATIONS["DEFAULT"]["use_ssl"])
if os.environ.get("ELASTIC_HTTP_AUTH") is not None:
    ES_HTTP_AUTH = os.environ.get("ELASTIC_HTTP_AUTH")
else:
    ES_HTTP_AUTH = ES_CONFIGURATIONS["DEFAULT"]["http_auth"]

ES_HOSTS = [
    {"host": ES_HOST, "port": ES_PORT, "use_ssl": ES_USE_SSL, "http_auth": ES_HTTP_AUTH}
]
CONCORDANCE_QUERY_SIZE = int(ES_CONFIGURATIONS["DEFAULT"]["concordance_query_size"])

BASE_MODEL_VISON_DIR = IMAGES_CONFIGURATION["IMAGES"]["base_dir"]

LOGGING_CONFIGURATION = configparser.ConfigParser()
LOGGING_CONFIGURATION.read_string(
    resource_string("mammut.resources", "logging.ini").decode("utf-8")
)
logging.config.fileConfig(LOGGING_CONFIGURATION)
if os.path.exists("data/logging.ini"):
    logging.config.fileConfig("data/logging.ini")
if os.path.exists("logging.ini"):
    logging.config.fileConfig("logging.ini")
