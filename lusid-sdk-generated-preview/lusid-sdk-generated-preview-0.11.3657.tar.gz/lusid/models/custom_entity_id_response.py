# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 0.11.3657
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from lusid.configuration import Configuration


class CustomEntityIdResponse(object):
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
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'identifier_scope': 'str',
        'identifier_type': 'str',
        'identifier_value': 'str',
        'effective_range': 'DateRange',
        'as_at_range': 'DateRange'
    }

    attribute_map = {
        'identifier_scope': 'identifierScope',
        'identifier_type': 'identifierType',
        'identifier_value': 'identifierValue',
        'effective_range': 'effectiveRange',
        'as_at_range': 'asAtRange'
    }

    required_map = {
        'identifier_scope': 'required',
        'identifier_type': 'required',
        'identifier_value': 'required',
        'effective_range': 'required',
        'as_at_range': 'required'
    }

    def __init__(self, identifier_scope=None, identifier_type=None, identifier_value=None, effective_range=None, as_at_range=None, local_vars_configuration=None):  # noqa: E501
        """CustomEntityIdResponse - a model defined in OpenAPI"
        
        :param identifier_scope:  (required)
        :type identifier_scope: str
        :param identifier_type:  (required)
        :type identifier_type: str
        :param identifier_value:  (required)
        :type identifier_value: str
        :param effective_range:  (required)
        :type effective_range: lusid.DateRange
        :param as_at_range:  (required)
        :type as_at_range: lusid.DateRange

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._identifier_scope = None
        self._identifier_type = None
        self._identifier_value = None
        self._effective_range = None
        self._as_at_range = None
        self.discriminator = None

        self.identifier_scope = identifier_scope
        self.identifier_type = identifier_type
        self.identifier_value = identifier_value
        self.effective_range = effective_range
        self.as_at_range = as_at_range

    @property
    def identifier_scope(self):
        """Gets the identifier_scope of this CustomEntityIdResponse.  # noqa: E501


        :return: The identifier_scope of this CustomEntityIdResponse.  # noqa: E501
        :rtype: str
        """
        return self._identifier_scope

    @identifier_scope.setter
    def identifier_scope(self, identifier_scope):
        """Sets the identifier_scope of this CustomEntityIdResponse.


        :param identifier_scope: The identifier_scope of this CustomEntityIdResponse.  # noqa: E501
        :type identifier_scope: str
        """
        if self.local_vars_configuration.client_side_validation and identifier_scope is None:  # noqa: E501
            raise ValueError("Invalid value for `identifier_scope`, must not be `None`")  # noqa: E501

        self._identifier_scope = identifier_scope

    @property
    def identifier_type(self):
        """Gets the identifier_type of this CustomEntityIdResponse.  # noqa: E501


        :return: The identifier_type of this CustomEntityIdResponse.  # noqa: E501
        :rtype: str
        """
        return self._identifier_type

    @identifier_type.setter
    def identifier_type(self, identifier_type):
        """Sets the identifier_type of this CustomEntityIdResponse.


        :param identifier_type: The identifier_type of this CustomEntityIdResponse.  # noqa: E501
        :type identifier_type: str
        """
        if self.local_vars_configuration.client_side_validation and identifier_type is None:  # noqa: E501
            raise ValueError("Invalid value for `identifier_type`, must not be `None`")  # noqa: E501

        self._identifier_type = identifier_type

    @property
    def identifier_value(self):
        """Gets the identifier_value of this CustomEntityIdResponse.  # noqa: E501


        :return: The identifier_value of this CustomEntityIdResponse.  # noqa: E501
        :rtype: str
        """
        return self._identifier_value

    @identifier_value.setter
    def identifier_value(self, identifier_value):
        """Sets the identifier_value of this CustomEntityIdResponse.


        :param identifier_value: The identifier_value of this CustomEntityIdResponse.  # noqa: E501
        :type identifier_value: str
        """
        if self.local_vars_configuration.client_side_validation and identifier_value is None:  # noqa: E501
            raise ValueError("Invalid value for `identifier_value`, must not be `None`")  # noqa: E501

        self._identifier_value = identifier_value

    @property
    def effective_range(self):
        """Gets the effective_range of this CustomEntityIdResponse.  # noqa: E501


        :return: The effective_range of this CustomEntityIdResponse.  # noqa: E501
        :rtype: lusid.DateRange
        """
        return self._effective_range

    @effective_range.setter
    def effective_range(self, effective_range):
        """Sets the effective_range of this CustomEntityIdResponse.


        :param effective_range: The effective_range of this CustomEntityIdResponse.  # noqa: E501
        :type effective_range: lusid.DateRange
        """
        if self.local_vars_configuration.client_side_validation and effective_range is None:  # noqa: E501
            raise ValueError("Invalid value for `effective_range`, must not be `None`")  # noqa: E501

        self._effective_range = effective_range

    @property
    def as_at_range(self):
        """Gets the as_at_range of this CustomEntityIdResponse.  # noqa: E501


        :return: The as_at_range of this CustomEntityIdResponse.  # noqa: E501
        :rtype: lusid.DateRange
        """
        return self._as_at_range

    @as_at_range.setter
    def as_at_range(self, as_at_range):
        """Sets the as_at_range of this CustomEntityIdResponse.


        :param as_at_range: The as_at_range of this CustomEntityIdResponse.  # noqa: E501
        :type as_at_range: lusid.DateRange
        """
        if self.local_vars_configuration.client_side_validation and as_at_range is None:  # noqa: E501
            raise ValueError("Invalid value for `as_at_range`, must not be `None`")  # noqa: E501

        self._as_at_range = as_at_range

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, CustomEntityIdResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CustomEntityIdResponse):
            return True

        return self.to_dict() != other.to_dict()
