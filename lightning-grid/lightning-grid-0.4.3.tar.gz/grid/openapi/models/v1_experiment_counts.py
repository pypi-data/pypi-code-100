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


class V1ExperimentCounts(object):
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
        'cancelled': 'int',
        'deleted': 'int',
        'failed': 'int',
        'pending': 'int',
        'running': 'int',
        'succeeded': 'int'
    }

    attribute_map = {
        'cancelled': 'cancelled',
        'deleted': 'deleted',
        'failed': 'failed',
        'pending': 'pending',
        'running': 'running',
        'succeeded': 'succeeded'
    }

    def __init__(self, cancelled=None, deleted=None, failed=None, pending=None, running=None, succeeded=None, _configuration=None):  # noqa: E501
        """V1ExperimentCounts - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._cancelled = None
        self._deleted = None
        self._failed = None
        self._pending = None
        self._running = None
        self._succeeded = None
        self.discriminator = None

        if cancelled is not None:
            self.cancelled = cancelled
        if deleted is not None:
            self.deleted = deleted
        if failed is not None:
            self.failed = failed
        if pending is not None:
            self.pending = pending
        if running is not None:
            self.running = running
        if succeeded is not None:
            self.succeeded = succeeded

    @property
    def cancelled(self):
        """Gets the cancelled of this V1ExperimentCounts.  # noqa: E501


        :return: The cancelled of this V1ExperimentCounts.  # noqa: E501
        :rtype: int
        """
        return self._cancelled

    @cancelled.setter
    def cancelled(self, cancelled):
        """Sets the cancelled of this V1ExperimentCounts.


        :param cancelled: The cancelled of this V1ExperimentCounts.  # noqa: E501
        :type: int
        """

        self._cancelled = cancelled

    @property
    def deleted(self):
        """Gets the deleted of this V1ExperimentCounts.  # noqa: E501


        :return: The deleted of this V1ExperimentCounts.  # noqa: E501
        :rtype: int
        """
        return self._deleted

    @deleted.setter
    def deleted(self, deleted):
        """Sets the deleted of this V1ExperimentCounts.


        :param deleted: The deleted of this V1ExperimentCounts.  # noqa: E501
        :type: int
        """

        self._deleted = deleted

    @property
    def failed(self):
        """Gets the failed of this V1ExperimentCounts.  # noqa: E501


        :return: The failed of this V1ExperimentCounts.  # noqa: E501
        :rtype: int
        """
        return self._failed

    @failed.setter
    def failed(self, failed):
        """Sets the failed of this V1ExperimentCounts.


        :param failed: The failed of this V1ExperimentCounts.  # noqa: E501
        :type: int
        """

        self._failed = failed

    @property
    def pending(self):
        """Gets the pending of this V1ExperimentCounts.  # noqa: E501


        :return: The pending of this V1ExperimentCounts.  # noqa: E501
        :rtype: int
        """
        return self._pending

    @pending.setter
    def pending(self, pending):
        """Sets the pending of this V1ExperimentCounts.


        :param pending: The pending of this V1ExperimentCounts.  # noqa: E501
        :type: int
        """

        self._pending = pending

    @property
    def running(self):
        """Gets the running of this V1ExperimentCounts.  # noqa: E501


        :return: The running of this V1ExperimentCounts.  # noqa: E501
        :rtype: int
        """
        return self._running

    @running.setter
    def running(self, running):
        """Sets the running of this V1ExperimentCounts.


        :param running: The running of this V1ExperimentCounts.  # noqa: E501
        :type: int
        """

        self._running = running

    @property
    def succeeded(self):
        """Gets the succeeded of this V1ExperimentCounts.  # noqa: E501


        :return: The succeeded of this V1ExperimentCounts.  # noqa: E501
        :rtype: int
        """
        return self._succeeded

    @succeeded.setter
    def succeeded(self, succeeded):
        """Sets the succeeded of this V1ExperimentCounts.


        :param succeeded: The succeeded of this V1ExperimentCounts.  # noqa: E501
        :type: int
        """

        self._succeeded = succeeded

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
        if issubclass(V1ExperimentCounts, dict):
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
        if not isinstance(other, V1ExperimentCounts):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1ExperimentCounts):
            return True

        return self.to_dict() != other.to_dict()
