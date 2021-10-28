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


class V1CreateClusterRequest(object):
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
        'name': 'str',
        'spec': 'V1ClusterSpec'
    }

    attribute_map = {
        'name': 'name',
        'spec': 'spec'
    }

    def __init__(self, name=None, spec=None, _configuration=None):  # noqa: E501
        """V1CreateClusterRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._name = None
        self._spec = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if spec is not None:
            self.spec = spec

    @property
    def name(self):
        """Gets the name of this V1CreateClusterRequest.  # noqa: E501


        :return: The name of this V1CreateClusterRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this V1CreateClusterRequest.


        :param name: The name of this V1CreateClusterRequest.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def spec(self):
        """Gets the spec of this V1CreateClusterRequest.  # noqa: E501


        :return: The spec of this V1CreateClusterRequest.  # noqa: E501
        :rtype: V1ClusterSpec
        """
        return self._spec

    @spec.setter
    def spec(self, spec):
        """Sets the spec of this V1CreateClusterRequest.


        :param spec: The spec of this V1CreateClusterRequest.  # noqa: E501
        :type: V1ClusterSpec
        """

        self._spec = spec

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
        if issubclass(V1CreateClusterRequest, dict):
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
        if not isinstance(other, V1CreateClusterRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1CreateClusterRequest):
            return True

        return self.to_dict() != other.to_dict()
