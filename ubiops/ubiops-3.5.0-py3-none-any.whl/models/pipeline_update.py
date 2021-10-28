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


class PipelineUpdate(object):
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
        'name': 'str',
        'description': 'str',
        'input_type': 'str',
        'input_fields': 'list[PipelineInputFieldCreate]',
        'output_type': 'str',
        'output_fields': 'list[PipelineOutputFieldCreate]',
        'labels': 'object',
        'default_version': 'str'
    }

    attribute_map = {
        'name': 'name',
        'description': 'description',
        'input_type': 'input_type',
        'input_fields': 'input_fields',
        'output_type': 'output_type',
        'output_fields': 'output_fields',
        'labels': 'labels',
        'default_version': 'default_version'
    }

    def __init__(self, name=None, description=None, input_type=None, input_fields=None, output_type=None, output_fields=None, labels=None, default_version=None, local_vars_configuration=None):  # noqa: E501
        """PipelineUpdate - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._description = None
        self._input_type = None
        self._input_fields = None
        self._output_type = None
        self._output_fields = None
        self._labels = None
        self._default_version = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if input_type is not None:
            self.input_type = input_type
        if input_fields is not None:
            self.input_fields = input_fields
        if output_type is not None:
            self.output_type = output_type
        if output_fields is not None:
            self.output_fields = output_fields
        if labels is not None:
            self.labels = labels
        if default_version is not None:
            self.default_version = default_version

    @property
    def name(self):
        """Gets the name of this PipelineUpdate.  # noqa: E501


        :return: The name of this PipelineUpdate.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this PipelineUpdate.


        :param name: The name of this PipelineUpdate.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                name is not None and not isinstance(name, str)):
            raise ValueError("Parameter `name` must be a string")  # noqa: E501

        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) < 1):
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `1`")  # noqa: E501

        self._name = name

    @property
    def description(self):
        """Gets the description of this PipelineUpdate.  # noqa: E501


        :return: The description of this PipelineUpdate.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this PipelineUpdate.


        :param description: The description of this PipelineUpdate.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                description is not None and not isinstance(description, str)):
            raise ValueError("Parameter `description` must be a string")  # noqa: E501

        self._description = description

    @property
    def input_type(self):
        """Gets the input_type of this PipelineUpdate.  # noqa: E501


        :return: The input_type of this PipelineUpdate.  # noqa: E501
        :rtype: str
        """
        return self._input_type

    @input_type.setter
    def input_type(self, input_type):
        """Sets the input_type of this PipelineUpdate.


        :param input_type: The input_type of this PipelineUpdate.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                input_type is not None and not isinstance(input_type, str)):
            raise ValueError("Parameter `input_type` must be a string")  # noqa: E501
        allowed_values = ["structured", "plain"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and input_type not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `input_type` ({0}), must be one of {1}"  # noqa: E501
                .format(input_type, allowed_values)
            )

        self._input_type = input_type

    @property
    def input_fields(self):
        """Gets the input_fields of this PipelineUpdate.  # noqa: E501


        :return: The input_fields of this PipelineUpdate.  # noqa: E501
        :rtype: list[PipelineInputFieldCreate]
        """
        return self._input_fields

    @input_fields.setter
    def input_fields(self, input_fields):
        """Sets the input_fields of this PipelineUpdate.


        :param input_fields: The input_fields of this PipelineUpdate.  # noqa: E501
        :type: list[PipelineInputFieldCreate]
        """
        if (self.local_vars_configuration.client_side_validation and
                input_fields is not None and not isinstance(input_fields, list)):
            raise ValueError("Parameter `input_fields` must be a list")  # noqa: E501
        if self.local_vars_configuration.client_side_validation and input_fields is not None:
            from ubiops.models.pipeline_input_field_create import PipelineInputFieldCreate

            input_fields = [
                PipelineInputFieldCreate(**item) if isinstance(item, dict) else item  # noqa: E501
                for item in input_fields
            ]

        self._input_fields = input_fields

    @property
    def output_type(self):
        """Gets the output_type of this PipelineUpdate.  # noqa: E501


        :return: The output_type of this PipelineUpdate.  # noqa: E501
        :rtype: str
        """
        return self._output_type

    @output_type.setter
    def output_type(self, output_type):
        """Sets the output_type of this PipelineUpdate.


        :param output_type: The output_type of this PipelineUpdate.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                output_type is not None and not isinstance(output_type, str)):
            raise ValueError("Parameter `output_type` must be a string")  # noqa: E501
        allowed_values = ["structured", "plain"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and output_type not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `output_type` ({0}), must be one of {1}"  # noqa: E501
                .format(output_type, allowed_values)
            )

        self._output_type = output_type

    @property
    def output_fields(self):
        """Gets the output_fields of this PipelineUpdate.  # noqa: E501


        :return: The output_fields of this PipelineUpdate.  # noqa: E501
        :rtype: list[PipelineOutputFieldCreate]
        """
        return self._output_fields

    @output_fields.setter
    def output_fields(self, output_fields):
        """Sets the output_fields of this PipelineUpdate.


        :param output_fields: The output_fields of this PipelineUpdate.  # noqa: E501
        :type: list[PipelineOutputFieldCreate]
        """
        if (self.local_vars_configuration.client_side_validation and
                output_fields is not None and not isinstance(output_fields, list)):
            raise ValueError("Parameter `output_fields` must be a list")  # noqa: E501
        if self.local_vars_configuration.client_side_validation and output_fields is not None:
            from ubiops.models.pipeline_output_field_create import PipelineOutputFieldCreate

            output_fields = [
                PipelineOutputFieldCreate(**item) if isinstance(item, dict) else item  # noqa: E501
                for item in output_fields
            ]

        self._output_fields = output_fields

    @property
    def labels(self):
        """Gets the labels of this PipelineUpdate.  # noqa: E501


        :return: The labels of this PipelineUpdate.  # noqa: E501
        :rtype: object
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """Sets the labels of this PipelineUpdate.


        :param labels: The labels of this PipelineUpdate.  # noqa: E501
        :type: object
        """

        self._labels = labels

    @property
    def default_version(self):
        """Gets the default_version of this PipelineUpdate.  # noqa: E501


        :return: The default_version of this PipelineUpdate.  # noqa: E501
        :rtype: str
        """
        return self._default_version

    @default_version.setter
    def default_version(self, default_version):
        """Sets the default_version of this PipelineUpdate.


        :param default_version: The default_version of this PipelineUpdate.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                default_version is not None and not isinstance(default_version, str)):
            raise ValueError("Parameter `default_version` must be a string")  # noqa: E501

        if (self.local_vars_configuration.client_side_validation and
                default_version is not None and len(default_version) < 1):
            raise ValueError("Invalid value for `default_version`, length must be greater than or equal to `1`")  # noqa: E501

        self._default_version = default_version

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
        if not isinstance(other, PipelineUpdate):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PipelineUpdate):
            return True

        return self.to_dict() != other.to_dict()
