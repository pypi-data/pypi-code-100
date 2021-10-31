# coding=utf-8

import redis
import functools
from abc import *
from mammut.models import MODELS_CONFIGURATIONS, MODELS_CONFIGURATIONS_FILE_NAME

CONFIGURATION_PROPERTIES_DEFAULT_VALUES = {}
CONFIGURATION_PROPERTIES_PARSE_FUNCTION = {}


def _get_configuration_property(self, class_name, property_name):
    configuration_path = self._get_configuration_path()
    default_value = CONFIGURATION_PROPERTIES_DEFAULT_VALUES[class_name][property_name]
    parser_function = CONFIGURATION_PROPERTIES_PARSE_FUNCTION[class_name][property_name]
    if self._redisProxy != None:
        if not self._redisProxy.hexists(configuration_path, property_name):
            _set_configuration_property(self, default_value, property_name)
        if parser_function != None:
            return parser_function(
                self._redisProxy.hget(configuration_path, property_name)
            )
        else:
            return self._redisProxy.hget(configuration_path, property_name)
    else:
        if not MODELS_CONFIGURATIONS.has_option(configuration_path, property_name):
            _set_configuration_property(self, default_value, property_name)
        if parser_function != None:
            return parser_function(
                MODELS_CONFIGURATIONS[configuration_path][property_name]
            )
        else:
            return MODELS_CONFIGURATIONS[configuration_path][property_name]


def _set_configuration_property(self, value, property_name):
    configuration_path = self._get_configuration_path()
    if self._redisProxy != None:
        self._redisProxy.hset(configuration_path, property_name, value)
    else:
        if not MODELS_CONFIGURATIONS.has_section(configuration_path):
            MODELS_CONFIGURATIONS[configuration_path] = {}
        MODELS_CONFIGURATIONS[configuration_path][property_name] = str(value)
        with open(MODELS_CONFIGURATIONS_FILE_NAME, "w") as configfile:
            MODELS_CONFIGURATIONS.write(configfile)


class Configurable(metaclass=ABCMeta):
    def __init__(
        self, configuration_path, configuration_name, redis_connection_pool=None
    ):
        """"""
        self._configuration_parent = configuration_path
        self._configuration = configuration_name
        self._redisProxy = None
        if redis_connection_pool != None:
            self._redisProxy = redis.Redis(connection_pool=redis_connection_pool)

    def _get_configuration_path(self):
        return self._configuration_parent + "." + self._configuration

    @staticmethod
    def _add_configuration_property(
        class_name,
        property_name,
        default_value,
        parser_function=None,
        property_doc=None,
    ):
        if class_name not in CONFIGURATION_PROPERTIES_DEFAULT_VALUES:
            CONFIGURATION_PROPERTIES_DEFAULT_VALUES[class_name] = {}
            CONFIGURATION_PROPERTIES_PARSE_FUNCTION[class_name] = {}
        CONFIGURATION_PROPERTIES_DEFAULT_VALUES[class_name][
            property_name
        ] = default_value
        CONFIGURATION_PROPERTIES_PARSE_FUNCTION[class_name][
            property_name
        ] = parser_function
        return property(
            fget=functools.partial(
                _get_configuration_property,
                class_name=class_name,
                property_name=property_name,
            ),
            fset=functools.partial(
                _set_configuration_property, property_name=property_name
            ),
            doc=property_doc,
        )
