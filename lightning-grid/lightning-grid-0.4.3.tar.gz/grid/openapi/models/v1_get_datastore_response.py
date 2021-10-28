# coding: utf-8

"""
    external/v1/external_session_service.proto

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: version not set
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six

from grid.openapi.configuration import Configuration


class V1GetDatastoreResponse(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'created_at': 'datetime',
        'id': 'str',
        'name': 'str',
        'spec': 'Externalv1DatastoreSpec',
        'status': 'Externalv1DatastoreStatus'
    }

    attribute_map = {
        'created_at': 'createdAt',
        'id': 'id',
        'name': 'name',
        'spec': 'spec',
        'status': 'status'
    }

    def __init__(self, created_at=None, id=None, name=None, spec=None, status=None, _configuration=None):  # noqa: E501
        """V1GetDatastoreResponse - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._created_at = None
        self._id = None
        self._name = None
        self._spec = None
        self._status = None
        self.discriminator = None

        if created_at is not None:
            self.created_at = created_at
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if spec is not None:
            self.spec = spec
        if status is not None:
            self.status = status

    @property
    def created_at(self):
        """Gets the created_at of this V1GetDatastoreResponse.  # noqa: E501


        :return: The created_at of this V1GetDatastoreResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this V1GetDatastoreResponse.


        :param created_at: The created_at of this V1GetDatastoreResponse.  # noqa: E501
        :type: datetime
        """

        self._created_at = created_at

    @property
    def id(self):
        """Gets the id of this V1GetDatastoreResponse.  # noqa: E501


        :return: The id of this V1GetDatastoreResponse.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this V1GetDatastoreResponse.


        :param id: The id of this V1GetDatastoreResponse.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this V1GetDatastoreResponse.  # noqa: E501


        :return: The name of this V1GetDatastoreResponse.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this V1GetDatastoreResponse.


        :param name: The name of this V1GetDatastoreResponse.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def spec(self):
        """Gets the spec of this V1GetDatastoreResponse.  # noqa: E501


        :return: The spec of this V1GetDatastoreResponse.  # noqa: E501
        :rtype: Externalv1DatastoreSpec
        """
        return self._spec

    @spec.setter
    def spec(self, spec):
        """Sets the spec of this V1GetDatastoreResponse.


        :param spec: The spec of this V1GetDatastoreResponse.  # noqa: E501
        :type: Externalv1DatastoreSpec
        """

        self._spec = spec

    @property
    def status(self):
        """Gets the status of this V1GetDatastoreResponse.  # noqa: E501


        :return: The status of this V1GetDatastoreResponse.  # noqa: E501
        :rtype: Externalv1DatastoreStatus
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this V1GetDatastoreResponse.


        :param status: The status of this V1GetDatastoreResponse.  # noqa: E501
        :type: Externalv1DatastoreStatus
        """

        self._status = status

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(V1GetDatastoreResponse, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, V1GetDatastoreResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1GetDatastoreResponse):
            return True

        return self.to_dict() != other.to_dict()
