# coding=utf-8
import os
import configparser
from pkg_resources import resource_string

__all__ = [
    "agenda",
    "agenda_app",
    "corpus_compiler_service",
    "InterpreterMain_pb2",
    "Protos_pb2",
    "WorkingMemory_pb2",
]

APPS_CONFIGURATIONS = configparser.ConfigParser()
APPS_CONFIGURATIONS.read_string(
    resource_string("mammut.resources", "apps.ini").decode("utf-8")
)
APPS_CONFIGURATIONS.read(["data/apps.ini", "apps.ini"])

KAFKA_BROKER_STR = (
    APPS_CONFIGURATIONS["KAFKA"]["host"] + ":" + APPS_CONFIGURATIONS["KAFKA"]["port"]
)
COMPILER_SERVICE_INPUT_TOPIC = APPS_CONFIGURATIONS["KAFKA"][
    "compiler_service_input_topic"
]
COMPILER_SERVICE_OUTPUT_TOPIC = APPS_CONFIGURATIONS["KAFKA"][
    "compiler_service_output_topic"
]
COMPILER_OUTPUT_RETRIES = int(APPS_CONFIGURATIONS["KAFKA"]["compiler_output_retries"])
COMPILER_OUTPUT_TIMEOUT = int(APPS_CONFIGURATIONS["KAFKA"]["compiler_output_timeout"])
COMPILER_OUTPUT_MAX_RECORDS = int(
    APPS_CONFIGURATIONS["KAFKA"]["compiler_output_max_records"]
)
