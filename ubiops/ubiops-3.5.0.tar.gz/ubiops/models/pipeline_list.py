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


class PipelineList(object):
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
        'project': 'str',
        'description': 'str',
        'input_type': 'str',
        'input_fields': 'list[PipelineInputFieldList]',
        'output_type': 'str',
        'output_fields': 'list[PipelineOutputFieldList]',
        'labels': 'dict(str, str)',
        'creation_date': 'datetime',
        'last_updated': 'datetime'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'project': 'project',
        'description': 'description',
        'input_type': 'input_type',
        'input_fields': 'input_fields',
        'output_type': 'output_type',
        'output_fields': 'output_fields',
        'labels': 'labels',
        'creation_date': 'creation_date',
        'last_updated': 'last_updated'
    }

    def __init__(self, id=None, name=None, project=None, description=None, input_type=None, input_fields=None, output_type=None, output_fields=None, labels=None, creation_date=None, last_updated=None, local_vars_configuration=None):  # noqa: E501
        """PipelineList - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._name = None
        self._project = None
        self._description = None
        self._input_type = None
        self._input_fields = None
        self._output_type = None
        self._output_fields = None
        self._labels = None
        self._creation_date = None
        self._last_updated = None
        self.discriminator = None

        if id is not None:
            self.id = id
        self.name = name
        self.project = project
        if description is not None:
            self.description = description
        self.input_type = input_type
        self.input_fields = input_fields
        self.output_type = output_type
        self.output_fields = output_fields
        self.labels = labels
        if creation_date is not None:
            self.creation_date = creation_date
        if last_updated is not None:
            self.last_updated = last_updated

    @property
    def id(self):
        """Gets the id of this PipelineList.  # noqa: E501


        :return: The id of this PipelineList.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this PipelineList.


        :param id: The id of this PipelineList.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                id is not None and not isinstance(id, str)):
            raise ValueError("Parameter `id` must be a string")  # noqa: E501

        self._id = id

    @property
    def name(self):
        """Gets the name of this PipelineList.  # noqa: E501


        :return: The name of this PipelineList.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this PipelineList.


        :param name: The name of this PipelineList.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and not isinstance(name, str)):
            raise ValueError("Parameter `name` must be a string")  # noqa: E501

        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) > 64):
            raise ValueError("Invalid value for `name`, length must be less than or equal to `64`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) < 1):
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `1`")  # noqa: E501

        self._name = name

    @property
    def project(self):
        """Gets the project of this PipelineList.  # noqa: E501


        :return: The project of this PipelineList.  # noqa: E501
        :rtype: str
        """
        return self._project

    @project.setter
    def project(self, project):
        """Sets the project of this PipelineList.


        :param project: The project of this PipelineList.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and project is None:  # noqa: E501
            raise ValueError("Invalid value for `project`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                project is not None and not isinstance(project, str)):
            raise ValueError("Parameter `project` must be a string")  # noqa: E501

        if (self.local_vars_configuration.client_side_validation and
                project is not None and len(project) < 1):
            raise ValueError("Invalid value for `project`, length must be greater than or equal to `1`")  # noqa: E501

        self._project = project

    @property
    def description(self):
        """Gets the description of this PipelineList.  # noqa: E501


        :return: The description of this PipelineList.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this PipelineList.


        :param description: The description of this PipelineList.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                description is not None and not isinstance(description, str)):
            raise ValueError("Parameter `description` must be a string")  # noqa: E501

        if (self.local_vars_configuration.client_side_validation and
                description is not None and len(description) > 200):
            raise ValueError("Invalid value for `description`, length must be less than or equal to `200`")  # noqa: E501

        self._description = description

    @property
    def input_type(self):
        """Gets the input_type of this PipelineList.  # noqa: E501


        :return: The input_type of this PipelineList.  # noqa: E501
        :rtype: str
        """
        return self._input_type

    @input_type.setter
    def input_type(self, input_type):
        """Sets the input_type of this PipelineList.


        :param input_type: The input_type of this PipelineList.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and input_type is None:  # noqa: E501
            raise ValueError("Invalid value for `input_type`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                input_type is not None and not isinstance(input_type, str)):
            raise ValueError("Parameter `input_type` must be a string")  # noqa: E501

        if (self.local_vars_configuration.client_side_validation and
                input_type is not None and len(input_type) < 1):
            raise ValueError("Invalid value for `input_type`, length must be greater than or equal to `1`")  # noqa: E501

        self._input_type = input_type

    @property
    def input_fields(self):
        """Gets the input_fields of this PipelineList.  # noqa: E501


        :return: The input_fields of this PipelineList.  # noqa: E501
        :rtype: list[PipelineInputFieldList]
        """
        return self._input_fields

    @input_fields.setter
    def input_fields(self, input_fields):
        """Sets the input_fields of this PipelineList.


        :param input_fields: The input_fields of this PipelineList.  # noqa: E501
        :type: list[PipelineInputFieldList]
        """
        if self.local_vars_configuration.client_side_validation and input_fields is None:  # noqa: E501
            raise ValueError("Invalid value for `input_fields`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                input_fields is not None and not isinstance(input_fields, list)):
            raise ValueError("Parameter `input_fields` must be a list")  # noqa: E501
        if self.local_vars_configuration.client_side_validation and input_fields is not None:
            from ubiops.models.pipeline_input_field_list import PipelineInputFieldList

            input_fields = [
                PipelineInputFieldList(**item) if isinstance(item, dict) else item  # noqa: E501
                for item in input_fields
            ]

        self._input_fields = input_fields

    @property
    def output_type(self):
        """Gets the output_type of this PipelineList.  # noqa: E501


        :return: The output_type of this PipelineList.  # noqa: E501
        :rtype: str
        """
        return self._output_type

    @output_type.setter
    def output_type(self, output_type):
        """Sets the output_type of this PipelineList.


        :param output_type: The output_type of this PipelineList.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and output_type is None:  # noqa: E501
            raise ValueError("Invalid value for `output_type`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                output_type is not None and not isinstance(output_type, str)):
            raise ValueError("Parameter `output_type` must be a string")  # noqa: E501

        if (self.local_vars_configuration.client_side_validation and
                output_type is not None and len(output_type) < 1):
            raise ValueError("Invalid value for `output_type`, length must be greater than or equal to `1`")  # noqa: E501

        self._output_type = output_type

    @property
    def output_fields(self):
        """Gets the output_fields of this PipelineList.  # noqa: E501


        :return: The output_fields of this PipelineList.  # noqa: E501
        :rtype: list[PipelineOutputFieldList]
        """
        return self._output_fields

    @output_fields.setter
    def output_fields(self, output_fields):
        """Sets the output_fields of this PipelineList.


        :param output_fields: The output_fields of this PipelineList.  # noqa: E501
        :type: list[PipelineOutputFieldList]
        """
        if self.local_vars_configuration.client_side_validation and output_fields is None:  # noqa: E501
            raise ValueError("Invalid value for `output_fields`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                output_fields is not None and not isinstance(output_fields, list)):
            raise ValueError("Parameter `output_fields` must be a list")  # noqa: E501
        if self.local_vars_configuration.client_side_validation and output_fields is not None:
            from ubiops.models.pipeline_output_field_list import PipelineOutputFieldList

            output_fields = [
                PipelineOutputFieldList(**item) if isinstance(item, dict) else item  # noqa: E501
                for item in output_fields
            ]

        self._output_fields = output_fields

    @property
    def labels(self):
        """Gets the labels of this PipelineList.  # noqa: E501


        :return: The labels of this PipelineList.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """Sets the labels of this PipelineList.


        :param labels: The labels of this PipelineList.  # noqa: E501
        :type: dict(str, str)
        """
        if (self.local_vars_configuration.client_side_validation and
                labels is not None and not isinstance(labels, dict)):
            raise ValueError("Parameter `labels` must be a dictionary")  # noqa: E501

        self._labels = labels

    @property
    def creation_date(self):
        """Gets the creation_date of this PipelineList.  # noqa: E501


        :return: The creation_date of this PipelineList.  # noqa: E501
        :rtype: datetime
        """
        return self._creation_date

    @creation_date.setter
    def creation_date(self, creation_date):
        """Sets the creation_date of this PipelineList.


        :param creation_date: The creation_date of this PipelineList.  # noqa: E501
        :type: datetime
        """

        self._creation_date = creation_date

    @property
    def last_updated(self):
        """Gets the last_updated of this PipelineList.  # noqa: E501


        :return: The last_updated of this PipelineList.  # noqa: E501
        :rtype: datetime
        """
        return self._last_updated

    @last_updated.setter
    def last_updated(self, last_updated):
        """Sets the last_updated of this PipelineList.


        :param last_updated: The last_updated of this PipelineList.  # noqa: E501
        :type: datetime
        """

        self._last_updated = last_updated

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
        if not isinstance(other, PipelineList):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PipelineList):
            return True

        return self.to_dict() != other.to_dict()
