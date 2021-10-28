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


class InheritedEnvironmentVariableList(object):
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
        'id': 'str',
        'name': 'str',
        'value': 'str',
        'secret': 'bool',
        'inheritance_type': 'str',
        'inheritance_name': 'str'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'value': 'value',
        'secret': 'secret',
        'inheritance_type': 'inheritance_type',
        'inheritance_name': 'inheritance_name'
    }

    def __init__(self, id=None, name=None, value=None, secret=None, inheritance_type=None, inheritance_name=None, local_vars_configuration=None):  # noqa: E501
        """InheritedEnvironmentVariableList - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._name = None
        self._value = None
        self._secret = None
        self._inheritance_type = None
        self._inheritance_name = None
        self.discriminator = None

        self.id = id
        self.name = name
        self.value = value
        self.secret = secret
        self.inheritance_type = inheritance_type
        self.inheritance_name = inheritance_name

    @property
    def id(self):
        """Gets the id of this InheritedEnvironmentVariableList.  # noqa: E501


        :return: The id of this InheritedEnvironmentVariableList.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this InheritedEnvironmentVariableList.


        :param id: The id of this InheritedEnvironmentVariableList.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                id is not None and not isinstance(id, str)):
            raise ValueError("Parameter `id` must be a string")  # noqa: E501

        self._id = id

    @property
    def name(self):
        """Gets the name of this InheritedEnvironmentVariableList.  # noqa: E501


        :return: The name of this InheritedEnvironmentVariableList.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this InheritedEnvironmentVariableList.


        :param name: The name of this InheritedEnvironmentVariableList.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and not isinstance(name, str)):
            raise ValueError("Parameter `name` must be a string")  # noqa: E501

        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) < 1):
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `1`")  # noqa: E501

        self._name = name

    @property
    def value(self):
        """Gets the value of this InheritedEnvironmentVariableList.  # noqa: E501


        :return: The value of this InheritedEnvironmentVariableList.  # noqa: E501
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this InheritedEnvironmentVariableList.


        :param value: The value of this InheritedEnvironmentVariableList.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                value is not None and not isinstance(value, str)):
            raise ValueError("Parameter `value` must be a string")  # noqa: E501

        if (self.local_vars_configuration.client_side_validation and
                value is not None and len(value) < 1):
            raise ValueError("Invalid value for `value`, length must be greater than or equal to `1`")  # noqa: E501

        self._value = value

    @property
    def secret(self):
        """Gets the secret of this InheritedEnvironmentVariableList.  # noqa: E501


        :return: The secret of this InheritedEnvironmentVariableList.  # noqa: E501
        :rtype: bool
        """
        return self._secret

    @secret.setter
    def secret(self, secret):
        """Sets the secret of this InheritedEnvironmentVariableList.


        :param secret: The secret of this InheritedEnvironmentVariableList.  # noqa: E501
        :type: bool
        """
        if self.local_vars_configuration.client_side_validation and secret is None:  # noqa: E501
            raise ValueError("Invalid value for `secret`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                secret is not None and not isinstance(secret, bool)):
            raise ValueError("Parameter `secret` must be a boolean")  # noqa: E501

        self._secret = secret

    @property
    def inheritance_type(self):
        """Gets the inheritance_type of this InheritedEnvironmentVariableList.  # noqa: E501


        :return: The inheritance_type of this InheritedEnvironmentVariableList.  # noqa: E501
        :rtype: str
        """
        return self._inheritance_type

    @inheritance_type.setter
    def inheritance_type(self, inheritance_type):
        """Sets the inheritance_type of this InheritedEnvironmentVariableList.


        :param inheritance_type: The inheritance_type of this InheritedEnvironmentVariableList.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                inheritance_type is not None and not isinstance(inheritance_type, str)):
            raise ValueError("Parameter `inheritance_type` must be a string")  # noqa: E501

        if (self.local_vars_configuration.client_side_validation and
                inheritance_type is not None and len(inheritance_type) < 1):
            raise ValueError("Invalid value for `inheritance_type`, length must be greater than or equal to `1`")  # noqa: E501

        self._inheritance_type = inheritance_type

    @property
    def inheritance_name(self):
        """Gets the inheritance_name of this InheritedEnvironmentVariableList.  # noqa: E501


        :return: The inheritance_name of this InheritedEnvironmentVariableList.  # noqa: E501
        :rtype: str
        """
        return self._inheritance_name

    @inheritance_name.setter
    def inheritance_name(self, inheritance_name):
        """Sets the inheritance_name of this InheritedEnvironmentVariableList.


        :param inheritance_name: The inheritance_name of this InheritedEnvironmentVariableList.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                inheritance_name is not None and not isinstance(inheritance_name, str)):
            raise ValueError("Parameter `inheritance_name` must be a string")  # noqa: E501

        if (self.local_vars_configuration.client_side_validation and
                inheritance_name is not None and len(inheritance_name) < 1):
            raise ValueError("Invalid value for `inheritance_name`, length must be greater than or equal to `1`")  # noqa: E501

        self._inheritance_name = inheritance_name

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
        if not isinstance(other, InheritedEnvironmentVariableList):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InheritedEnvironmentVariableList):
            return True

        return self.to_dict() != other.to_dict()
