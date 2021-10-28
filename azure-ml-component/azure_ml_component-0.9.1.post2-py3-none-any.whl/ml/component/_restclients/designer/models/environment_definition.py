# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class EnvironmentDefinition(Model):
    """EnvironmentDefinition.

    :param name:
    :type name: str
    :param version:
    :type version: str
    :param python:
    :type python: ~designer.models.PythonSection
    :param environment_variables:
    :type environment_variables: dict[str, str]
    :param docker:
    :type docker: ~designer.models.DockerSection
    :param spark:
    :type spark: ~designer.models.SparkSection
    :param r:
    :type r: ~designer.models.RSection
    :param inferencing_stack_version:
    :type inferencing_stack_version: str
    """

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'version': {'key': 'version', 'type': 'str'},
        'python': {'key': 'python', 'type': 'PythonSection'},
        'environment_variables': {'key': 'environmentVariables', 'type': '{str}'},
        'docker': {'key': 'docker', 'type': 'DockerSection'},
        'spark': {'key': 'spark', 'type': 'SparkSection'},
        'r': {'key': 'r', 'type': 'RSection'},
        'inferencing_stack_version': {'key': 'inferencingStackVersion', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(EnvironmentDefinition, self).__init__(**kwargs)
        self.name = kwargs.get('name', None)
        self.version = kwargs.get('version', None)
        self.python = kwargs.get('python', None)
        self.environment_variables = kwargs.get('environment_variables', None)
        self.docker = kwargs.get('docker', None)
        self.spark = kwargs.get('spark', None)
        self.r = kwargs.get('r', None)
        self.inferencing_stack_version = kwargs.get('inferencing_stack_version', None)
