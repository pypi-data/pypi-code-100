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


class DistributionCreateParameters(object):
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
        'project_id': 'str',
        'platforms': 'list[str]',
        'locale_ids': 'list[str]',
        'format_options': 'dict(str, str)',
        'fallback_to_non_regional_locale': 'bool',
        'fallback_to_default_locale': 'bool',
        'use_last_reviewed_version': 'bool'
    }

    attribute_map = {
        'name': 'name',
        'project_id': 'project_id',
        'platforms': 'platforms',
        'locale_ids': 'locale_ids',
        'format_options': 'format_options',
        'fallback_to_non_regional_locale': 'fallback_to_non_regional_locale',
        'fallback_to_default_locale': 'fallback_to_default_locale',
        'use_last_reviewed_version': 'use_last_reviewed_version'
    }

    def __init__(self, name=None, project_id=None, platforms=None, locale_ids=None, format_options=None, fallback_to_non_regional_locale=None, fallback_to_default_locale=None, use_last_reviewed_version=None, local_vars_configuration=None):  # noqa: E501
        """DistributionCreateParameters - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._project_id = None
        self._platforms = None
        self._locale_ids = None
        self._format_options = None
        self._fallback_to_non_regional_locale = None
        self._fallback_to_default_locale = None
        self._use_last_reviewed_version = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if project_id is not None:
            self.project_id = project_id
        if platforms is not None:
            self.platforms = platforms
        if locale_ids is not None:
            self.locale_ids = locale_ids
        if format_options is not None:
            self.format_options = format_options
        if fallback_to_non_regional_locale is not None:
            self.fallback_to_non_regional_locale = fallback_to_non_regional_locale
        if fallback_to_default_locale is not None:
            self.fallback_to_default_locale = fallback_to_default_locale
        if use_last_reviewed_version is not None:
            self.use_last_reviewed_version = use_last_reviewed_version

    @property
    def name(self):
        """Gets the name of this DistributionCreateParameters.  # noqa: E501

        Name of the distribution  # noqa: E501

        :return: The name of this DistributionCreateParameters.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this DistributionCreateParameters.

        Name of the distribution  # noqa: E501

        :param name: The name of this DistributionCreateParameters.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def project_id(self):
        """Gets the project_id of this DistributionCreateParameters.  # noqa: E501

        Project id the distribution should be assigned to.  # noqa: E501

        :return: The project_id of this DistributionCreateParameters.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this DistributionCreateParameters.

        Project id the distribution should be assigned to.  # noqa: E501

        :param project_id: The project_id of this DistributionCreateParameters.  # noqa: E501
        :type: str
        """

        self._project_id = project_id

    @property
    def platforms(self):
        """Gets the platforms of this DistributionCreateParameters.  # noqa: E501

        List of platforms the distribution should support.  # noqa: E501

        :return: The platforms of this DistributionCreateParameters.  # noqa: E501
        :rtype: list[str]
        """
        return self._platforms

    @platforms.setter
    def platforms(self, platforms):
        """Sets the platforms of this DistributionCreateParameters.

        List of platforms the distribution should support.  # noqa: E501

        :param platforms: The platforms of this DistributionCreateParameters.  # noqa: E501
        :type: list[str]
        """

        self._platforms = platforms

    @property
    def locale_ids(self):
        """Gets the locale_ids of this DistributionCreateParameters.  # noqa: E501

        List of locale ids that will be part of distribution releases  # noqa: E501

        :return: The locale_ids of this DistributionCreateParameters.  # noqa: E501
        :rtype: list[str]
        """
        return self._locale_ids

    @locale_ids.setter
    def locale_ids(self, locale_ids):
        """Sets the locale_ids of this DistributionCreateParameters.

        List of locale ids that will be part of distribution releases  # noqa: E501

        :param locale_ids: The locale_ids of this DistributionCreateParameters.  # noqa: E501
        :type: list[str]
        """

        self._locale_ids = locale_ids

    @property
    def format_options(self):
        """Gets the format_options of this DistributionCreateParameters.  # noqa: E501

        Additional formatting and render options. Only <code>enclose_in_cdata</code> is available for platform <code>android</code>.  # noqa: E501

        :return: The format_options of this DistributionCreateParameters.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._format_options

    @format_options.setter
    def format_options(self, format_options):
        """Sets the format_options of this DistributionCreateParameters.

        Additional formatting and render options. Only <code>enclose_in_cdata</code> is available for platform <code>android</code>.  # noqa: E501

        :param format_options: The format_options of this DistributionCreateParameters.  # noqa: E501
        :type: dict(str, str)
        """

        self._format_options = format_options

    @property
    def fallback_to_non_regional_locale(self):
        """Gets the fallback_to_non_regional_locale of this DistributionCreateParameters.  # noqa: E501

        Indicates whether to fallback to non regional locale when locale can not be found  # noqa: E501

        :return: The fallback_to_non_regional_locale of this DistributionCreateParameters.  # noqa: E501
        :rtype: bool
        """
        return self._fallback_to_non_regional_locale

    @fallback_to_non_regional_locale.setter
    def fallback_to_non_regional_locale(self, fallback_to_non_regional_locale):
        """Sets the fallback_to_non_regional_locale of this DistributionCreateParameters.

        Indicates whether to fallback to non regional locale when locale can not be found  # noqa: E501

        :param fallback_to_non_regional_locale: The fallback_to_non_regional_locale of this DistributionCreateParameters.  # noqa: E501
        :type: bool
        """

        self._fallback_to_non_regional_locale = fallback_to_non_regional_locale

    @property
    def fallback_to_default_locale(self):
        """Gets the fallback_to_default_locale of this DistributionCreateParameters.  # noqa: E501

        Indicates whether to fallback to projects default locale when locale can not be found  # noqa: E501

        :return: The fallback_to_default_locale of this DistributionCreateParameters.  # noqa: E501
        :rtype: bool
        """
        return self._fallback_to_default_locale

    @fallback_to_default_locale.setter
    def fallback_to_default_locale(self, fallback_to_default_locale):
        """Sets the fallback_to_default_locale of this DistributionCreateParameters.

        Indicates whether to fallback to projects default locale when locale can not be found  # noqa: E501

        :param fallback_to_default_locale: The fallback_to_default_locale of this DistributionCreateParameters.  # noqa: E501
        :type: bool
        """

        self._fallback_to_default_locale = fallback_to_default_locale

    @property
    def use_last_reviewed_version(self):
        """Gets the use_last_reviewed_version of this DistributionCreateParameters.  # noqa: E501

        Use last reviewed instead of latest translation in a project  # noqa: E501

        :return: The use_last_reviewed_version of this DistributionCreateParameters.  # noqa: E501
        :rtype: bool
        """
        return self._use_last_reviewed_version

    @use_last_reviewed_version.setter
    def use_last_reviewed_version(self, use_last_reviewed_version):
        """Sets the use_last_reviewed_version of this DistributionCreateParameters.

        Use last reviewed instead of latest translation in a project  # noqa: E501

        :param use_last_reviewed_version: The use_last_reviewed_version of this DistributionCreateParameters.  # noqa: E501
        :type: bool
        """

        self._use_last_reviewed_version = use_last_reviewed_version

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
        if not isinstance(other, DistributionCreateParameters):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DistributionCreateParameters):
            return True

        return self.to_dict() != other.to_dict()
