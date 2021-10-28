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


class ImportDetail(object):
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
        'imported_by': 'str',
        'creation_date': 'datetime',
        'status': 'str',
        'error_message': 'str',
        'size': 'int',
        'deployments': 'dict(str, object)',
        'pipelines': 'dict(str, object)',
        'environment_variables': 'dict(str, object)'
    }

    attribute_map = {
        'id': 'id',
        'imported_by': 'imported_by',
        'creation_date': 'creation_date',
        'status': 'status',
        'error_message': 'error_message',
        'size': 'size',
        'deployments': 'deployments',
        'pipelines': 'pipelines',
        'environment_variables': 'environment_variables'
    }

    def __init__(self, id=None, imported_by=None, creation_date=None, status='pending', error_message=None, size=None, deployments=None, pipelines=None, environment_variables=None, local_vars_configuration=None):  # noqa: E501
        """ImportDetail - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._imported_by = None
        self._creation_date = None
        self._status = None
        self._error_message = None
        self._size = None
        self._deployments = None
        self._pipelines = None
        self._environment_variables = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if imported_by is not None:
            self.imported_by = imported_by
        if creation_date is not None:
            self.creation_date = creation_date
        if status is not None:
            self.status = status
        self.error_message = error_message
        self.size = size
        if deployments is not None:
            self.deployments = deployments
        if pipelines is not None:
            self.pipelines = pipelines
        if environment_variables is not None:
            self.environment_variables = environment_variables

    @property
    def id(self):
        """Gets the id of this ImportDetail.  # noqa: E501


        :return: The id of this ImportDetail.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ImportDetail.


        :param id: The id of this ImportDetail.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                id is not None and not isinstance(id, str)):
            raise ValueError("Parameter `id` must be a string")  # noqa: E501

        self._id = id

    @property
    def imported_by(self):
        """Gets the imported_by of this ImportDetail.  # noqa: E501


        :return: The imported_by of this ImportDetail.  # noqa: E501
        :rtype: str
        """
        return self._imported_by

    @imported_by.setter
    def imported_by(self, imported_by):
        """Sets the imported_by of this ImportDetail.


        :param imported_by: The imported_by of this ImportDetail.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                imported_by is not None and not isinstance(imported_by, str)):
            raise ValueError("Parameter `imported_by` must be a string")  # noqa: E501

        self._imported_by = imported_by

    @property
    def creation_date(self):
        """Gets the creation_date of this ImportDetail.  # noqa: E501


        :return: The creation_date of this ImportDetail.  # noqa: E501
        :rtype: datetime
        """
        return self._creation_date

    @creation_date.setter
    def creation_date(self, creation_date):
        """Sets the creation_date of this ImportDetail.


        :param creation_date: The creation_date of this ImportDetail.  # noqa: E501
        :type: datetime
        """

        self._creation_date = creation_date

    @property
    def status(self):
        """Gets the status of this ImportDetail.  # noqa: E501


        :return: The status of this ImportDetail.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this ImportDetail.


        :param status: The status of this ImportDetail.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                status is not None and not isinstance(status, str)):
            raise ValueError("Parameter `status` must be a string")  # noqa: E501
        allowed_values = ["pending", "scanning", "confirmation", "confirmation_pending", "processing", "completed", "failed"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and status not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"  # noqa: E501
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def error_message(self):
        """Gets the error_message of this ImportDetail.  # noqa: E501


        :return: The error_message of this ImportDetail.  # noqa: E501
        :rtype: str
        """
        return self._error_message

    @error_message.setter
    def error_message(self, error_message):
        """Sets the error_message of this ImportDetail.


        :param error_message: The error_message of this ImportDetail.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                error_message is not None and not isinstance(error_message, str)):
            raise ValueError("Parameter `error_message` must be a string")  # noqa: E501

        if (self.local_vars_configuration.client_side_validation and
                error_message is not None and len(error_message) > 1024):
            raise ValueError("Invalid value for `error_message`, length must be less than or equal to `1024`")  # noqa: E501

        self._error_message = error_message

    @property
    def size(self):
        """Gets the size of this ImportDetail.  # noqa: E501


        :return: The size of this ImportDetail.  # noqa: E501
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """Sets the size of this ImportDetail.


        :param size: The size of this ImportDetail.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                size is not None and not isinstance(size, int)):
            raise ValueError("Parameter `size` must be an integer")  # noqa: E501

        self._size = size

    @property
    def deployments(self):
        """Gets the deployments of this ImportDetail.  # noqa: E501


        :return: The deployments of this ImportDetail.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._deployments

    @deployments.setter
    def deployments(self, deployments):
        """Sets the deployments of this ImportDetail.


        :param deployments: The deployments of this ImportDetail.  # noqa: E501
        :type: dict(str, object)
        """
        if (self.local_vars_configuration.client_side_validation and
                deployments is not None and not isinstance(deployments, dict)):
            raise ValueError("Parameter `deployments` must be a dictionary")  # noqa: E501

        self._deployments = deployments

    @property
    def pipelines(self):
        """Gets the pipelines of this ImportDetail.  # noqa: E501


        :return: The pipelines of this ImportDetail.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._pipelines

    @pipelines.setter
    def pipelines(self, pipelines):
        """Sets the pipelines of this ImportDetail.


        :param pipelines: The pipelines of this ImportDetail.  # noqa: E501
        :type: dict(str, object)
        """
        if (self.local_vars_configuration.client_side_validation and
                pipelines is not None and not isinstance(pipelines, dict)):
            raise ValueError("Parameter `pipelines` must be a dictionary")  # noqa: E501

        self._pipelines = pipelines

    @property
    def environment_variables(self):
        """Gets the environment_variables of this ImportDetail.  # noqa: E501


        :return: The environment_variables of this ImportDetail.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._environment_variables

    @environment_variables.setter
    def environment_variables(self, environment_variables):
        """Sets the environment_variables of this ImportDetail.


        :param environment_variables: The environment_variables of this ImportDetail.  # noqa: E501
        :type: dict(str, object)
        """
        if (self.local_vars_configuration.client_side_validation and
                environment_variables is not None and not isinstance(environment_variables, dict)):
            raise ValueError("Parameter `environment_variables` must be a dictionary")  # noqa: E501

        self._environment_variables = environment_variables

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
        if not isinstance(other, ImportDetail):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ImportDetail):
            return True

        return self.to_dict() != other.to_dict()
