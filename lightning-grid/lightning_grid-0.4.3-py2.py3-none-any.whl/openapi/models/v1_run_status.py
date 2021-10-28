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


class V1RunStatus(object):
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
        'cost': 'float',
        'deleted_timestamp': 'datetime',
        'experiment_counts': 'V1ExperimentCounts',
        'experiment_ids': 'list[str]',
        'finish_timestamp': 'datetime',
        'hourly_cost': 'float',
        'message': 'str',
        'phase': 'V1RunState',
        'start_timestamp': 'datetime'
    }

    attribute_map = {
        'cost': 'cost',
        'deleted_timestamp': 'deletedTimestamp',
        'experiment_counts': 'experimentCounts',
        'experiment_ids': 'experimentIds',
        'finish_timestamp': 'finishTimestamp',
        'hourly_cost': 'hourlyCost',
        'message': 'message',
        'phase': 'phase',
        'start_timestamp': 'startTimestamp'
    }

    def __init__(self, cost=None, deleted_timestamp=None, experiment_counts=None, experiment_ids=None, finish_timestamp=None, hourly_cost=None, message=None, phase=None, start_timestamp=None, _configuration=None):  # noqa: E501
        """V1RunStatus - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._cost = None
        self._deleted_timestamp = None
        self._experiment_counts = None
        self._experiment_ids = None
        self._finish_timestamp = None
        self._hourly_cost = None
        self._message = None
        self._phase = None
        self._start_timestamp = None
        self.discriminator = None

        if cost is not None:
            self.cost = cost
        if deleted_timestamp is not None:
            self.deleted_timestamp = deleted_timestamp
        if experiment_counts is not None:
            self.experiment_counts = experiment_counts
        if experiment_ids is not None:
            self.experiment_ids = experiment_ids
        if finish_timestamp is not None:
            self.finish_timestamp = finish_timestamp
        if hourly_cost is not None:
            self.hourly_cost = hourly_cost
        if message is not None:
            self.message = message
        if phase is not None:
            self.phase = phase
        if start_timestamp is not None:
            self.start_timestamp = start_timestamp

    @property
    def cost(self):
        """Gets the cost of this V1RunStatus.  # noqa: E501


        :return: The cost of this V1RunStatus.  # noqa: E501
        :rtype: float
        """
        return self._cost

    @cost.setter
    def cost(self, cost):
        """Sets the cost of this V1RunStatus.


        :param cost: The cost of this V1RunStatus.  # noqa: E501
        :type: float
        """

        self._cost = cost

    @property
    def deleted_timestamp(self):
        """Gets the deleted_timestamp of this V1RunStatus.  # noqa: E501


        :return: The deleted_timestamp of this V1RunStatus.  # noqa: E501
        :rtype: datetime
        """
        return self._deleted_timestamp

    @deleted_timestamp.setter
    def deleted_timestamp(self, deleted_timestamp):
        """Sets the deleted_timestamp of this V1RunStatus.


        :param deleted_timestamp: The deleted_timestamp of this V1RunStatus.  # noqa: E501
        :type: datetime
        """

        self._deleted_timestamp = deleted_timestamp

    @property
    def experiment_counts(self):
        """Gets the experiment_counts of this V1RunStatus.  # noqa: E501


        :return: The experiment_counts of this V1RunStatus.  # noqa: E501
        :rtype: V1ExperimentCounts
        """
        return self._experiment_counts

    @experiment_counts.setter
    def experiment_counts(self, experiment_counts):
        """Sets the experiment_counts of this V1RunStatus.


        :param experiment_counts: The experiment_counts of this V1RunStatus.  # noqa: E501
        :type: V1ExperimentCounts
        """

        self._experiment_counts = experiment_counts

    @property
    def experiment_ids(self):
        """Gets the experiment_ids of this V1RunStatus.  # noqa: E501


        :return: The experiment_ids of this V1RunStatus.  # noqa: E501
        :rtype: list[str]
        """
        return self._experiment_ids

    @experiment_ids.setter
    def experiment_ids(self, experiment_ids):
        """Sets the experiment_ids of this V1RunStatus.


        :param experiment_ids: The experiment_ids of this V1RunStatus.  # noqa: E501
        :type: list[str]
        """

        self._experiment_ids = experiment_ids

    @property
    def finish_timestamp(self):
        """Gets the finish_timestamp of this V1RunStatus.  # noqa: E501


        :return: The finish_timestamp of this V1RunStatus.  # noqa: E501
        :rtype: datetime
        """
        return self._finish_timestamp

    @finish_timestamp.setter
    def finish_timestamp(self, finish_timestamp):
        """Sets the finish_timestamp of this V1RunStatus.


        :param finish_timestamp: The finish_timestamp of this V1RunStatus.  # noqa: E501
        :type: datetime
        """

        self._finish_timestamp = finish_timestamp

    @property
    def hourly_cost(self):
        """Gets the hourly_cost of this V1RunStatus.  # noqa: E501


        :return: The hourly_cost of this V1RunStatus.  # noqa: E501
        :rtype: float
        """
        return self._hourly_cost

    @hourly_cost.setter
    def hourly_cost(self, hourly_cost):
        """Sets the hourly_cost of this V1RunStatus.


        :param hourly_cost: The hourly_cost of this V1RunStatus.  # noqa: E501
        :type: float
        """

        self._hourly_cost = hourly_cost

    @property
    def message(self):
        """Gets the message of this V1RunStatus.  # noqa: E501


        :return: The message of this V1RunStatus.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this V1RunStatus.


        :param message: The message of this V1RunStatus.  # noqa: E501
        :type: str
        """

        self._message = message

    @property
    def phase(self):
        """Gets the phase of this V1RunStatus.  # noqa: E501


        :return: The phase of this V1RunStatus.  # noqa: E501
        :rtype: V1RunState
        """
        return self._phase

    @phase.setter
    def phase(self, phase):
        """Sets the phase of this V1RunStatus.


        :param phase: The phase of this V1RunStatus.  # noqa: E501
        :type: V1RunState
        """

        self._phase = phase

    @property
    def start_timestamp(self):
        """Gets the start_timestamp of this V1RunStatus.  # noqa: E501


        :return: The start_timestamp of this V1RunStatus.  # noqa: E501
        :rtype: datetime
        """
        return self._start_timestamp

    @start_timestamp.setter
    def start_timestamp(self, start_timestamp):
        """Sets the start_timestamp of this V1RunStatus.


        :param start_timestamp: The start_timestamp of this V1RunStatus.  # noqa: E501
        :type: datetime
        """

        self._start_timestamp = start_timestamp

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
        if issubclass(V1RunStatus, dict):
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
        if not isinstance(other, V1RunStatus):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1RunStatus):
            return True

        return self.to_dict() != other.to_dict()
