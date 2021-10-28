# coding: utf-8

"""
    UbiOps

    Client Library to interact with the UbiOps API.  # noqa: E501

    The version of the OpenAPI document: v2.1
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from ubiops.configuration import Configuration


class DeploymentVersionCreate(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'version': 'str',
        'language': 'str',
        'memory_allocation': 'int',
        'maximum_instances': 'int',
        'minimum_instances': 'int',
        'maximum_idle_time': 'int',
        'description': 'str',
        'labels': 'dict(str, str)',
        'request_retention_time': 'int',
        'request_retention_mode': 'str',
        'deployment_mode': 'str'
    }

    attribute_map = {
        'version': 'version',
        'language': 'language',
        'memory_allocation': 'memory_allocation',
        'maximum_instances': 'maximum_instances',
        'minimum_instances': 'minimum_instances',
        'maximum_idle_time': 'maximum_idle_time',
        'description': 'description',
        'labels': 'labels',
        'request_retention_time': 'request_retention_time',
        'request_retention_mode': 'request_retention_mode',
        'deployment_mode': 'deployment_mode'
    }

    def __init__(self, version=None, language='python3.7', memory_allocation=None, maximum_instances=None, minimum_instances=None, maximum_idle_time=None, description=None, labels=None, request_retention_time=None, request_retention_mode='full', deployment_mode='express', local_vars_configuration=None):  # noqa: E501
        """DeploymentVersionCreate - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._version = None
        self._language = None
        self._memory_allocation = None
        self._maximum_instances = None
        self._minimum_instances = None
        self._maximum_idle_time = None
        self._description = None
        self._labels = None
        self._request_retention_time = None
        self._request_retention_mode = None
        self._deployment_mode = None
        self.discriminator = None

        self.version = version
        if language is not None:
            self.language = language
        if memory_allocation is not None:
            self.memory_allocation = memory_allocation
        if maximum_instances is not None:
            self.maximum_instances = maximum_instances
        if minimum_instances is not None:
            self.minimum_instances = minimum_instances
        if maximum_idle_time is not None:
            self.maximum_idle_time = maximum_idle_time
        if description is not None:
            self.description = description
        self.labels = labels
        if request_retention_time is not None:
            self.request_retention_time = request_retention_time
        if request_retention_mode is not None:
            self.request_retention_mode = request_retention_mode
        if deployment_mode is not None:
            self.deployment_mode = deployment_mode

    @property
    def version(self):
        """Gets the version of this DeploymentVersionCreate.  # noqa: E501


        :return: The version of this DeploymentVersionCreate.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this DeploymentVersionCreate.


        :param version: The version of this DeploymentVersionCreate.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and version is None:  # noqa: E501
            raise ValueError("Invalid value for `version`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                version is not None and not isinstance(version, str)):
            raise ValueError("Parameter `version` must be a string")  # noqa: E501

        if (self.local_vars_configuration.client_side_validation and
                version is not None and len(version) < 1):
            raise ValueError("Invalid value for `version`, length must be greater than or equal to `1`")  # noqa: E501

        self._version = version

    @property
    def language(self):
        """Gets the language of this DeploymentVersionCreate.  # noqa: E501


        :return: The language of this DeploymentVersionCreate.  # noqa: E501
        :rtype: str
        """
        return self._language

    @language.setter
    def language(self, language):
        """Sets the language of this DeploymentVersionCreate.


        :param language: The language of this DeploymentVersionCreate.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                language is not None and not isinstance(language, str)):
            raise ValueError("Parameter `language` must be a string")  # noqa: E501
        allowed_values = ["python3.6", "python3.7", "python3.8", "r4.0"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and language not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `language` ({0}), must be one of {1}"  # noqa: E501
                .format(language, allowed_values)
            )

        self._language = language

    @property
    def memory_allocation(self):
        """Gets the memory_allocation of this DeploymentVersionCreate.  # noqa: E501


        :return: The memory_allocation of this DeploymentVersionCreate.  # noqa: E501
        :rtype: int
        """
        return self._memory_allocation

    @memory_allocation.setter
    def memory_allocation(self, memory_allocation):
        """Sets the memory_allocation of this DeploymentVersionCreate.


        :param memory_allocation: The memory_allocation of this DeploymentVersionCreate.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                memory_allocation is not None and not isinstance(memory_allocation, int)):
            raise ValueError("Parameter `memory_allocation` must be an integer")  # noqa: E501

        if (self.local_vars_configuration.client_side_validation and
                memory_allocation is not None and memory_allocation > 1048576):  # noqa: E501
            raise ValueError("Invalid value for `memory_allocation`, must be a value less than or equal to `1048576`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                memory_allocation is not None and memory_allocation < 256):  # noqa: E501
            raise ValueError("Invalid value for `memory_allocation`, must be a value greater than or equal to `256`")  # noqa: E501

        self._memory_allocation = memory_allocation

    @property
    def maximum_instances(self):
        """Gets the maximum_instances of this DeploymentVersionCreate.  # noqa: E501


        :return: The maximum_instances of this DeploymentVersionCreate.  # noqa: E501
        :rtype: int
        """
        return self._maximum_instances

    @maximum_instances.setter
    def maximum_instances(self, maximum_instances):
        """Sets the maximum_instances of this DeploymentVersionCreate.


        :param maximum_instances: The maximum_instances of this DeploymentVersionCreate.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                maximum_instances is not None and not isinstance(maximum_instances, int)):
            raise ValueError("Parameter `maximum_instances` must be an integer")  # noqa: E501

        self._maximum_instances = maximum_instances

    @property
    def minimum_instances(self):
        """Gets the minimum_instances of this DeploymentVersionCreate.  # noqa: E501


        :return: The minimum_instances of this DeploymentVersionCreate.  # noqa: E501
        :rtype: int
        """
        return self._minimum_instances

    @minimum_instances.setter
    def minimum_instances(self, minimum_instances):
        """Sets the minimum_instances of this DeploymentVersionCreate.


        :param minimum_instances: The minimum_instances of this DeploymentVersionCreate.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                minimum_instances is not None and not isinstance(minimum_instances, int)):
            raise ValueError("Parameter `minimum_instances` must be an integer")  # noqa: E501

        self._minimum_instances = minimum_instances

    @property
    def maximum_idle_time(self):
        """Gets the maximum_idle_time of this DeploymentVersionCreate.  # noqa: E501


        :return: The maximum_idle_time of this DeploymentVersionCreate.  # noqa: E501
        :rtype: int
        """
        return self._maximum_idle_time

    @maximum_idle_time.setter
    def maximum_idle_time(self, maximum_idle_time):
        """Sets the maximum_idle_time of this DeploymentVersionCreate.


        :param maximum_idle_time: The maximum_idle_time of this DeploymentVersionCreate.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                maximum_idle_time is not None and not isinstance(maximum_idle_time, int)):
            raise ValueError("Parameter `maximum_idle_time` must be an integer")  # noqa: E501

        self._maximum_idle_time = maximum_idle_time

    @property
    def description(self):
        """Gets the description of this DeploymentVersionCreate.  # noqa: E501


        :return: The description of this DeploymentVersionCreate.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this DeploymentVersionCreate.


        :param description: The description of this DeploymentVersionCreate.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                description is not None and not isinstance(description, str)):
            raise ValueError("Parameter `description` must be a string")  # noqa: E501

        self._description = description

    @property
    def labels(self):
        """Gets the labels of this DeploymentVersionCreate.  # noqa: E501


        :return: The labels of this DeploymentVersionCreate.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """Sets the labels of this DeploymentVersionCreate.


        :param labels: The labels of this DeploymentVersionCreate.  # noqa: E501
        :type: dict(str, str)
        """
        if (self.local_vars_configuration.client_side_validation and
                labels is not None and not isinstance(labels, dict)):
            raise ValueError("Parameter `labels` must be a dictionary")  # noqa: E501

        self._labels = labels

    @property
    def request_retention_time(self):
        """Gets the request_retention_time of this DeploymentVersionCreate.  # noqa: E501


        :return: The request_retention_time of this DeploymentVersionCreate.  # noqa: E501
        :rtype: int
        """
        return self._request_retention_time

    @request_retention_time.setter
    def request_retention_time(self, request_retention_time):
        """Sets the request_retention_time of this DeploymentVersionCreate.


        :param request_retention_time: The request_retention_time of this DeploymentVersionCreate.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                request_retention_time is not None and not isinstance(request_retention_time, int)):
            raise ValueError("Parameter `request_retention_time` must be an integer")  # noqa: E501

        if (self.local_vars_configuration.client_side_validation and
                request_retention_time is not None and request_retention_time > 2.4192E+6):  # noqa: E501
            raise ValueError("Invalid value for `request_retention_time`, must be a value less than or equal to `2.4192E+6`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                request_retention_time is not None and request_retention_time < 3.6E+3):  # noqa: E501
            raise ValueError("Invalid value for `request_retention_time`, must be a value greater than or equal to `3.6E+3`")  # noqa: E501

        self._request_retention_time = request_retention_time

    @property
    def request_retention_mode(self):
        """Gets the request_retention_mode of this DeploymentVersionCreate.  # noqa: E501


        :return: The request_retention_mode of this DeploymentVersionCreate.  # noqa: E501
        :rtype: str
        """
        return self._request_retention_mode

    @request_retention_mode.setter
    def request_retention_mode(self, request_retention_mode):
        """Sets the request_retention_mode of this DeploymentVersionCreate.


        :param request_retention_mode: The request_retention_mode of this DeploymentVersionCreate.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                request_retention_mode is not None and not isinstance(request_retention_mode, str)):
            raise ValueError("Parameter `request_retention_mode` must be a string")  # noqa: E501
        allowed_values = ["none", "metadata", "full"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and request_retention_mode not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `request_retention_mode` ({0}), must be one of {1}"  # noqa: E501
                .format(request_retention_mode, allowed_values)
            )

        self._request_retention_mode = request_retention_mode

    @property
    def deployment_mode(self):
        """Gets the deployment_mode of this DeploymentVersionCreate.  # noqa: E501


        :return: The deployment_mode of this DeploymentVersionCreate.  # noqa: E501
        :rtype: str
        """
        return self._deployment_mode

    @deployment_mode.setter
    def deployment_mode(self, deployment_mode):
        """Sets the deployment_mode of this DeploymentVersionCreate.


        :param deployment_mode: The deployment_mode of this DeploymentVersionCreate.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                deployment_mode is not None and not isinstance(deployment_mode, str)):
            raise ValueError("Parameter `deployment_mode` must be a string")  # noqa: E501
        allowed_values = ["express", "batch"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and deployment_mode not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `deployment_mode` ({0}), must be one of {1}"  # noqa: E501
                .format(deployment_mode, allowed_values)
            )

        self._deployment_mode = deployment_mode

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, DeploymentVersionCreate):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DeploymentVersionCreate):
            return True

        return self.to_dict() != other.to_dict()
