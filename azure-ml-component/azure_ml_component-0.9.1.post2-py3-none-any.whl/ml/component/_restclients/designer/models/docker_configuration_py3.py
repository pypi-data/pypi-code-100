# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class DockerConfiguration(Model):
    """DockerConfiguration.

    :param use_docker:
    :type use_docker: bool
    :param shared_volumes:
    :type shared_volumes: bool
    :param arguments:
    :type arguments: list[str]
    """

    _attribute_map = {
        'use_docker': {'key': 'useDocker', 'type': 'bool'},
        'shared_volumes': {'key': 'sharedVolumes', 'type': 'bool'},
        'arguments': {'key': 'arguments', 'type': '[str]'},
    }

    def __init__(self, *, use_docker: bool=None, shared_volumes: bool=None, arguments=None, **kwargs) -> None:
        super(DockerConfiguration, self).__init__(**kwargs)
        self.use_docker = use_docker
        self.shared_volumes = shared_volumes
        self.arguments = arguments
