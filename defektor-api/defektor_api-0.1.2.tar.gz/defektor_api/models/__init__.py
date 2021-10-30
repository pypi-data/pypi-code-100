# flake8: noqa

# import all models into this package
# if you have many models here with many references from one model to another this may
# raise a RecursionError
# to avoid this, import only the models that you directly need like:
# from from defektor_api.model.pet import Pet
# or import this package, but before doing it, use:
# import sys
# sys.setrecursionlimit(n)

from defektor_api.model.campaign import Campaign
from defektor_api.model.data_collector import DataCollector
from defektor_api.model.data_output_uri import DataOutputURI
from defektor_api.model.docker_image import DockerImage
from defektor_api.model.ijk import Ijk
from defektor_api.model.injektion import Injektion
from defektor_api.model.key_value import KeyValue
from defektor_api.model.plan import Plan
from defektor_api.model.run import Run
from defektor_api.model.ssh_credentials import SSHCredentials
from defektor_api.model.slave import Slave
from defektor_api.model.system_config import SystemConfig
from defektor_api.model.system_type import SystemType
from defektor_api.model.work_load import WorkLoad
