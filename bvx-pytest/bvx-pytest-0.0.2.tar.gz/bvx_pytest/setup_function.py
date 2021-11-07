import docker

from bvx_docker import network_exists
from bvx_network import unused_port_number
from .defines import DOCKER_NETWORK_NAME


def setup_function():
    # create docker client
    _client = docker.from_env()

    # find free port for elasticsearch
    _es_port = unused_port_number()

    # get docker networks
    _networks = _client.networks.list()

    # create docker network for pytest
    if not network_exists(DOCKER_NETWORK_NAME, networks=_networks):
        _client.networks.create(DOCKER_NETWORK_NAME, driver="bridge")


if __name__ == "__main__":
    # execute only if run as a script
    setup_function()

# EOF
