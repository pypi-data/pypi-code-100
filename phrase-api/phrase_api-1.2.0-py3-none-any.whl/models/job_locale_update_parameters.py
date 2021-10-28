# coding: utf-8

"""
    Phrase API Reference

    The version of the OpenAPI document: 2.0.0
    Contact: support@phrase.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from phrase_api.configuration import Configuration


class JobLocaleUpdateParameters(object):
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
        'branch': 'str',
        'locale_id': 'str',
        'user_ids': 'list[str]'
    }

    attribute_map = {
        'branch': 'branch',
        'locale_id': 'locale_id',
        'user_ids': 'user_ids'
    }

    def __init__(self, branch=None, locale_id=None, user_ids=None, local_vars_configuration=None):  # noqa: E501
        """JobLocaleUpdateParameters - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._branch = None
        self._locale_id = None
        self._user_ids = None
        self.discriminator = None

        if branch is not None:
            self.branch = branch
        if locale_id is not None:
            self.locale_id = locale_id
        if user_ids is not None:
            self.user_ids = user_ids

    @property
    def branch(self):
        """Gets the branch of this JobLocaleUpdateParameters.  # noqa: E501

        specify the branch to use  # noqa: E501

        :return: The branch of this JobLocaleUpdateParameters.  # noqa: E501
        :rtype: str
        """
        return self._branch

    @branch.setter
    def branch(self, branch):
        """Sets the branch of this JobLocaleUpdateParameters.

        specify the branch to use  # noqa: E501

        :param branch: The branch of this JobLocaleUpdateParameters.  # noqa: E501
        :type: str
        """

        self._branch = branch

    @property
    def locale_id(self):
        """Gets the locale_id of this JobLocaleUpdateParameters.  # noqa: E501

        locale id  # noqa: E501

        :return: The locale_id of this JobLocaleUpdateParameters.  # noqa: E501
        :rtype: str
        """
        return self._locale_id

    @locale_id.setter
    def locale_id(self, locale_id):
        """Sets the locale_id of this JobLocaleUpdateParameters.

        locale id  # noqa: E501

        :param locale_id: The locale_id of this JobLocaleUpdateParameters.  # noqa: E501
        :type: str
        """

        self._locale_id = locale_id

    @property
    def user_ids(self):
        """Gets the user_ids of this JobLocaleUpdateParameters.  # noqa: E501

        Array of user ids to be assigned to the job locale  # noqa: E501

        :return: The user_ids of this JobLocaleUpdateParameters.  # noqa: E501
        :rtype: list[str]
        """
        return self._user_ids

    @user_ids.setter
    def user_ids(self, user_ids):
        """Sets the user_ids of this JobLocaleUpdateParameters.

        Array of user ids to be assigned to the job locale  # noqa: E501

        :param user_ids: The user_ids of this JobLocaleUpdateParameters.  # noqa: E501
        :type: list[str]
        """

        self._user_ids = user_ids

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
        if not isinstance(other, JobLocaleUpdateParameters):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, JobLocaleUpdateParameters):
            return True

        return self.to_dict() != other.to_dict()
