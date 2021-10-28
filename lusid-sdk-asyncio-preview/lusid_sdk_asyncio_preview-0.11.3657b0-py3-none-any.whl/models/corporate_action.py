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


class CorporateAction(object):
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
        'corporate_action_code': 'str',
        'description': 'str',
        'announcement_date': 'datetime',
        'ex_date': 'datetime',
        'record_date': 'datetime',
        'payment_date': 'datetime',
        'transitions': 'list[CorporateActionTransition]'
    }

    attribute_map = {
        'corporate_action_code': 'corporateActionCode',
        'description': 'description',
        'announcement_date': 'announcementDate',
        'ex_date': 'exDate',
        'record_date': 'recordDate',
        'payment_date': 'paymentDate',
        'transitions': 'transitions'
    }

    required_map = {
        'corporate_action_code': 'required',
        'description': 'optional',
        'announcement_date': 'optional',
        'ex_date': 'optional',
        'record_date': 'optional',
        'payment_date': 'optional',
        'transitions': 'optional'
    }

    def __init__(self, corporate_action_code=None, description=None, announcement_date=None, ex_date=None, record_date=None, payment_date=None, transitions=None, local_vars_configuration=None):  # noqa: E501
        """CorporateAction - a model defined in OpenAPI"
        
        :param corporate_action_code:  The unique identifier of this corporate action (required)
        :type corporate_action_code: str
        :param description: 
        :type description: str
        :param announcement_date:  The announcement date of the corporate action
        :type announcement_date: datetime
        :param ex_date:  The ex date of the corporate action
        :type ex_date: datetime
        :param record_date:  The record date of the corporate action
        :type record_date: datetime
        :param payment_date:  The payment date of the corporate action
        :type payment_date: datetime
        :param transitions:  The transitions that result from this corporate action
        :type transitions: list[lusid_asyncio.CorporateActionTransition]

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._corporate_action_code = None
        self._description = None
        self._announcement_date = None
        self._ex_date = None
        self._record_date = None
        self._payment_date = None
        self._transitions = None
        self.discriminator = None

        self.corporate_action_code = corporate_action_code
        self.description = description
        if announcement_date is not None:
            self.announcement_date = announcement_date
        if ex_date is not None:
            self.ex_date = ex_date
        if record_date is not None:
            self.record_date = record_date
        if payment_date is not None:
            self.payment_date = payment_date
        self.transitions = transitions

    @property
    def corporate_action_code(self):
        """Gets the corporate_action_code of this CorporateAction.  # noqa: E501

        The unique identifier of this corporate action  # noqa: E501

        :return: The corporate_action_code of this CorporateAction.  # noqa: E501
        :rtype: str
        """
        return self._corporate_action_code

    @corporate_action_code.setter
    def corporate_action_code(self, corporate_action_code):
        """Sets the corporate_action_code of this CorporateAction.

        The unique identifier of this corporate action  # noqa: E501

        :param corporate_action_code: The corporate_action_code of this CorporateAction.  # noqa: E501
        :type corporate_action_code: str
        """
        if self.local_vars_configuration.client_side_validation and corporate_action_code is None:  # noqa: E501
            raise ValueError("Invalid value for `corporate_action_code`, must not be `None`")  # noqa: E501

        self._corporate_action_code = corporate_action_code

    @property
    def description(self):
        """Gets the description of this CorporateAction.  # noqa: E501


        :return: The description of this CorporateAction.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this CorporateAction.


        :param description: The description of this CorporateAction.  # noqa: E501
        :type description: str
        """

        self._description = description

    @property
    def announcement_date(self):
        """Gets the announcement_date of this CorporateAction.  # noqa: E501

        The announcement date of the corporate action  # noqa: E501

        :return: The announcement_date of this CorporateAction.  # noqa: E501
        :rtype: datetime
        """
        return self._announcement_date

    @announcement_date.setter
    def announcement_date(self, announcement_date):
        """Sets the announcement_date of this CorporateAction.

        The announcement date of the corporate action  # noqa: E501

        :param announcement_date: The announcement_date of this CorporateAction.  # noqa: E501
        :type announcement_date: datetime
        """

        self._announcement_date = announcement_date

    @property
    def ex_date(self):
        """Gets the ex_date of this CorporateAction.  # noqa: E501

        The ex date of the corporate action  # noqa: E501

        :return: The ex_date of this CorporateAction.  # noqa: E501
        :rtype: datetime
        """
        return self._ex_date

    @ex_date.setter
    def ex_date(self, ex_date):
        """Sets the ex_date of this CorporateAction.

        The ex date of the corporate action  # noqa: E501

        :param ex_date: The ex_date of this CorporateAction.  # noqa: E501
        :type ex_date: datetime
        """

        self._ex_date = ex_date

    @property
    def record_date(self):
        """Gets the record_date of this CorporateAction.  # noqa: E501

        The record date of the corporate action  # noqa: E501

        :return: The record_date of this CorporateAction.  # noqa: E501
        :rtype: datetime
        """
        return self._record_date

    @record_date.setter
    def record_date(self, record_date):
        """Sets the record_date of this CorporateAction.

        The record date of the corporate action  # noqa: E501

        :param record_date: The record_date of this CorporateAction.  # noqa: E501
        :type record_date: datetime
        """

        self._record_date = record_date

    @property
    def payment_date(self):
        """Gets the payment_date of this CorporateAction.  # noqa: E501

        The payment date of the corporate action  # noqa: E501

        :return: The payment_date of this CorporateAction.  # noqa: E501
        :rtype: datetime
        """
        return self._payment_date

    @payment_date.setter
    def payment_date(self, payment_date):
        """Sets the payment_date of this CorporateAction.

        The payment date of the corporate action  # noqa: E501

        :param payment_date: The payment_date of this CorporateAction.  # noqa: E501
        :type payment_date: datetime
        """

        self._payment_date = payment_date

    @property
    def transitions(self):
        """Gets the transitions of this CorporateAction.  # noqa: E501

        The transitions that result from this corporate action  # noqa: E501

        :return: The transitions of this CorporateAction.  # noqa: E501
        :rtype: list[lusid_asyncio.CorporateActionTransition]
        """
        return self._transitions

    @transitions.setter
    def transitions(self, transitions):
        """Sets the transitions of this CorporateAction.

        The transitions that result from this corporate action  # noqa: E501

        :param transitions: The transitions of this CorporateAction.  # noqa: E501
        :type transitions: list[lusid_asyncio.CorporateActionTransition]
        """

        self._transitions = transitions

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
        if not isinstance(other, CorporateAction):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CorporateAction):
            return True

        return self.to_dict() != other.to_dict()
