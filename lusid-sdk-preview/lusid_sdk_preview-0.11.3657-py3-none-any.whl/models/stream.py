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


class Stream(object):
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
        'can_read': 'bool',
        'can_seek': 'bool',
        'can_timeout': 'bool',
        'can_write': 'bool',
        'length': 'int',
        'position': 'int',
        'read_timeout': 'int',
        'write_timeout': 'int'
    }

    attribute_map = {
        'can_read': 'canRead',
        'can_seek': 'canSeek',
        'can_timeout': 'canTimeout',
        'can_write': 'canWrite',
        'length': 'length',
        'position': 'position',
        'read_timeout': 'readTimeout',
        'write_timeout': 'writeTimeout'
    }

    required_map = {
        'can_read': 'optional',
        'can_seek': 'optional',
        'can_timeout': 'optional',
        'can_write': 'optional',
        'length': 'optional',
        'position': 'optional',
        'read_timeout': 'optional',
        'write_timeout': 'optional'
    }

    def __init__(self, can_read=None, can_seek=None, can_timeout=None, can_write=None, length=None, position=None, read_timeout=None, write_timeout=None, local_vars_configuration=None):  # noqa: E501
        """Stream - a model defined in OpenAPI"
        
        :param can_read: 
        :type can_read: bool
        :param can_seek: 
        :type can_seek: bool
        :param can_timeout: 
        :type can_timeout: bool
        :param can_write: 
        :type can_write: bool
        :param length: 
        :type length: int
        :param position: 
        :type position: int
        :param read_timeout: 
        :type read_timeout: int
        :param write_timeout: 
        :type write_timeout: int

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._can_read = None
        self._can_seek = None
        self._can_timeout = None
        self._can_write = None
        self._length = None
        self._position = None
        self._read_timeout = None
        self._write_timeout = None
        self.discriminator = None

        if can_read is not None:
            self.can_read = can_read
        if can_seek is not None:
            self.can_seek = can_seek
        if can_timeout is not None:
            self.can_timeout = can_timeout
        if can_write is not None:
            self.can_write = can_write
        if length is not None:
            self.length = length
        if position is not None:
            self.position = position
        if read_timeout is not None:
            self.read_timeout = read_timeout
        if write_timeout is not None:
            self.write_timeout = write_timeout

    @property
    def can_read(self):
        """Gets the can_read of this Stream.  # noqa: E501


        :return: The can_read of this Stream.  # noqa: E501
        :rtype: bool
        """
        return self._can_read

    @can_read.setter
    def can_read(self, can_read):
        """Sets the can_read of this Stream.


        :param can_read: The can_read of this Stream.  # noqa: E501
        :type can_read: bool
        """

        self._can_read = can_read

    @property
    def can_seek(self):
        """Gets the can_seek of this Stream.  # noqa: E501


        :return: The can_seek of this Stream.  # noqa: E501
        :rtype: bool
        """
        return self._can_seek

    @can_seek.setter
    def can_seek(self, can_seek):
        """Sets the can_seek of this Stream.


        :param can_seek: The can_seek of this Stream.  # noqa: E501
        :type can_seek: bool
        """

        self._can_seek = can_seek

    @property
    def can_timeout(self):
        """Gets the can_timeout of this Stream.  # noqa: E501


        :return: The can_timeout of this Stream.  # noqa: E501
        :rtype: bool
        """
        return self._can_timeout

    @can_timeout.setter
    def can_timeout(self, can_timeout):
        """Sets the can_timeout of this Stream.


        :param can_timeout: The can_timeout of this Stream.  # noqa: E501
        :type can_timeout: bool
        """

        self._can_timeout = can_timeout

    @property
    def can_write(self):
        """Gets the can_write of this Stream.  # noqa: E501


        :return: The can_write of this Stream.  # noqa: E501
        :rtype: bool
        """
        return self._can_write

    @can_write.setter
    def can_write(self, can_write):
        """Sets the can_write of this Stream.


        :param can_write: The can_write of this Stream.  # noqa: E501
        :type can_write: bool
        """

        self._can_write = can_write

    @property
    def length(self):
        """Gets the length of this Stream.  # noqa: E501


        :return: The length of this Stream.  # noqa: E501
        :rtype: int
        """
        return self._length

    @length.setter
    def length(self, length):
        """Sets the length of this Stream.


        :param length: The length of this Stream.  # noqa: E501
        :type length: int
        """

        self._length = length

    @property
    def position(self):
        """Gets the position of this Stream.  # noqa: E501


        :return: The position of this Stream.  # noqa: E501
        :rtype: int
        """
        return self._position

    @position.setter
    def position(self, position):
        """Sets the position of this Stream.


        :param position: The position of this Stream.  # noqa: E501
        :type position: int
        """

        self._position = position

    @property
    def read_timeout(self):
        """Gets the read_timeout of this Stream.  # noqa: E501


        :return: The read_timeout of this Stream.  # noqa: E501
        :rtype: int
        """
        return self._read_timeout

    @read_timeout.setter
    def read_timeout(self, read_timeout):
        """Sets the read_timeout of this Stream.


        :param read_timeout: The read_timeout of this Stream.  # noqa: E501
        :type read_timeout: int
        """

        self._read_timeout = read_timeout

    @property
    def write_timeout(self):
        """Gets the write_timeout of this Stream.  # noqa: E501


        :return: The write_timeout of this Stream.  # noqa: E501
        :rtype: int
        """
        return self._write_timeout

    @write_timeout.setter
    def write_timeout(self, write_timeout):
        """Sets the write_timeout of this Stream.


        :param write_timeout: The write_timeout of this Stream.  # noqa: E501
        :type write_timeout: int
        """

        self._write_timeout = write_timeout

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
        if not isinstance(other, Stream):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Stream):
            return True

        return self.to_dict() != other.to_dict()
