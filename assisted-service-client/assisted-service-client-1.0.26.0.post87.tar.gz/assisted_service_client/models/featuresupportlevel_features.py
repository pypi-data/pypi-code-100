# coding: utf-8

"""
    AssistedInstall

    Assisted installation  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class FeaturesupportlevelFeatures(object):
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
        'feature_id': 'str',
        'support_level': 'str'
    }

    attribute_map = {
        'feature_id': 'feature_id',
        'support_level': 'support_level'
    }

    def __init__(self, feature_id=None, support_level=None):  # noqa: E501
        """FeaturesupportlevelFeatures - a model defined in Swagger"""  # noqa: E501

        self._feature_id = None
        self._support_level = None
        self.discriminator = None

        if feature_id is not None:
            self.feature_id = feature_id
        if support_level is not None:
            self.support_level = support_level

    @property
    def feature_id(self):
        """Gets the feature_id of this FeaturesupportlevelFeatures.  # noqa: E501

        The ID of the feature  # noqa: E501

        :return: The feature_id of this FeaturesupportlevelFeatures.  # noqa: E501
        :rtype: str
        """
        return self._feature_id

    @feature_id.setter
    def feature_id(self, feature_id):
        """Sets the feature_id of this FeaturesupportlevelFeatures.

        The ID of the feature  # noqa: E501

        :param feature_id: The feature_id of this FeaturesupportlevelFeatures.  # noqa: E501
        :type: str
        """

        self._feature_id = feature_id

    @property
    def support_level(self):
        """Gets the support_level of this FeaturesupportlevelFeatures.  # noqa: E501


        :return: The support_level of this FeaturesupportlevelFeatures.  # noqa: E501
        :rtype: str
        """
        return self._support_level

    @support_level.setter
    def support_level(self, support_level):
        """Sets the support_level of this FeaturesupportlevelFeatures.


        :param support_level: The support_level of this FeaturesupportlevelFeatures.  # noqa: E501
        :type: str
        """
        allowed_values = ["supported", "unsupported", "tech-preview", "dev-preview"]  # noqa: E501
        if support_level not in allowed_values:
            raise ValueError(
                "Invalid value for `support_level` ({0}), must be one of {1}"  # noqa: E501
                .format(support_level, allowed_values)
            )

        self._support_level = support_level

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
        if issubclass(FeaturesupportlevelFeatures, dict):
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
        if not isinstance(other, FeaturesupportlevelFeatures):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
