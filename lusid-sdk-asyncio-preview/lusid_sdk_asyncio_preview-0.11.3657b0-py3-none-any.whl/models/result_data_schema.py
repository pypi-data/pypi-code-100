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

from lusid_asyncio.configuration import Configuration


class ResultDataSchema(object):
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
        'node_value_schema': 'dict(str, FieldSchema)',
        'property_schema': 'dict(str, FieldSchema)'
    }

    attribute_map = {
        'node_value_schema': 'nodeValueSchema',
        'property_schema': 'propertySchema'
    }

    required_map = {
        'node_value_schema': 'optional',
        'property_schema': 'optional'
    }

    def __init__(self, node_value_schema=None, property_schema=None, local_vars_configuration=None):  # noqa: E501
        """ResultDataSchema - a model defined in OpenAPI"
        
        :param node_value_schema: 
        :type node_value_schema: dict[str, lusid_asyncio.FieldSchema]
        :param property_schema: 
        :type property_schema: dict[str, lusid_asyncio.FieldSchema]

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._node_value_schema = None
        self._property_schema = None
        self.discriminator = None

        self.node_value_schema = node_value_schema
        self.property_schema = property_schema

    @property
    def node_value_schema(self):
        """Gets the node_value_schema of this ResultDataSchema.  # noqa: E501


        :return: The node_value_schema of this ResultDataSchema.  # noqa: E501
        :rtype: dict[str, lusid_asyncio.FieldSchema]
        """
        return self._node_value_schema

    @node_value_schema.setter
    def node_value_schema(self, node_value_schema):
        """Sets the node_value_schema of this ResultDataSchema.


        :param node_value_schema: The node_value_schema of this ResultDataSchema.  # noqa: E501
        :type node_value_schema: dict[str, lusid_asyncio.FieldSchema]
        """

        self._node_value_schema = node_value_schema

    @property
    def property_schema(self):
        """Gets the property_schema of this ResultDataSchema.  # noqa: E501


        :return: The property_schema of this ResultDataSchema.  # noqa: E501
        :rtype: dict[str, lusid_asyncio.FieldSchema]
        """
        return self._property_schema

    @property_schema.setter
    def property_schema(self, property_schema):
        """Sets the property_schema of this ResultDataSchema.


        :param property_schema: The property_schema of this ResultDataSchema.  # noqa: E501
        :type property_schema: dict[str, lusid_asyncio.FieldSchema]
        """

        self._property_schema = property_schema

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
        if not isinstance(other, ResultDataSchema):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ResultDataSchema):
            return True

        return self.to_dict() != other.to_dict()
