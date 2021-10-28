# coding: utf-8

"""
    College Football Data API

    This is an API for accessing all sorts of college football data.  It currently has a wide array of data ranging from play by play to player statistics to game scores and more.  # noqa: E501

    OpenAPI spec version: 2.4.1
    Contact: admin@collegefootballdata.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class PlayerGameSchool(object):
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
        'conference': 'str'
    }

    attribute_map = {
        'name': 'name',
        'conference': 'conference'
    }

    def __init__(self, name=None, conference=None):  # noqa: E501
        """PlayerGameSchool - a model defined in Swagger"""  # noqa: E501

        self._name = None
        self._conference = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if conference is not None:
            self.conference = conference

    @property
    def name(self):
        """Gets the name of this PlayerGameSchool.  # noqa: E501


        :return: The name of this PlayerGameSchool.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this PlayerGameSchool.


        :param name: The name of this PlayerGameSchool.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def conference(self):
        """Gets the conference of this PlayerGameSchool.  # noqa: E501


        :return: The conference of this PlayerGameSchool.  # noqa: E501
        :rtype: str
        """
        return self._conference

    @conference.setter
    def conference(self, conference):
        """Sets the conference of this PlayerGameSchool.


        :param conference: The conference of this PlayerGameSchool.  # noqa: E501
        :type: str
        """

        self._conference = conference

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
        if issubclass(PlayerGameSchool, dict):
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
        if not isinstance(other, PlayerGameSchool):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
