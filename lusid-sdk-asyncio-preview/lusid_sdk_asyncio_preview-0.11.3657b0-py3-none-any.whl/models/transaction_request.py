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


class TransactionRequest(object):
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
        'transaction_id': 'str',
        'type': 'str',
        'instrument_identifiers': 'dict(str, str)',
        'transaction_date': 'str',
        'settlement_date': 'str',
        'units': 'float',
        'transaction_price': 'TransactionPrice',
        'total_consideration': 'CurrencyAndAmount',
        'exchange_rate': 'float',
        'transaction_currency': 'str',
        'properties': 'dict(str, PerpetualProperty)',
        'counterparty_id': 'str',
        'source': 'str'
    }

    attribute_map = {
        'transaction_id': 'transactionId',
        'type': 'type',
        'instrument_identifiers': 'instrumentIdentifiers',
        'transaction_date': 'transactionDate',
        'settlement_date': 'settlementDate',
        'units': 'units',
        'transaction_price': 'transactionPrice',
        'total_consideration': 'totalConsideration',
        'exchange_rate': 'exchangeRate',
        'transaction_currency': 'transactionCurrency',
        'properties': 'properties',
        'counterparty_id': 'counterpartyId',
        'source': 'source'
    }

    required_map = {
        'transaction_id': 'required',
        'type': 'required',
        'instrument_identifiers': 'required',
        'transaction_date': 'required',
        'settlement_date': 'required',
        'units': 'required',
        'transaction_price': 'optional',
        'total_consideration': 'required',
        'exchange_rate': 'optional',
        'transaction_currency': 'optional',
        'properties': 'optional',
        'counterparty_id': 'optional',
        'source': 'optional'
    }

    def __init__(self, transaction_id=None, type=None, instrument_identifiers=None, transaction_date=None, settlement_date=None, units=None, transaction_price=None, total_consideration=None, exchange_rate=None, transaction_currency=None, properties=None, counterparty_id=None, source=None, local_vars_configuration=None):  # noqa: E501
        """TransactionRequest - a model defined in OpenAPI"
        
        :param transaction_id:  The unique identifier of the transaction. (required)
        :type transaction_id: str
        :param type:  The type of the transaction, for example 'Buy' or 'Sell'. The transaction type must have been pre-configured using the System Configuration API. If not, this operation will succeed but you are not able to calculate holdings for the portfolio that include this transaction. (required)
        :type type: str
        :param instrument_identifiers:  A set of instrument identifiers that can resolve the transaction to a unique instrument. (required)
        :type instrument_identifiers: dict(str, str)
        :param transaction_date:  The date of the transaction. (required)
        :type transaction_date: str
        :param settlement_date:  The settlement date of the transaction. (required)
        :type settlement_date: str
        :param units:  The number of units of the transacted instrument. (required)
        :type units: float
        :param transaction_price: 
        :type transaction_price: lusid_asyncio.TransactionPrice
        :param total_consideration:  (required)
        :type total_consideration: lusid_asyncio.CurrencyAndAmount
        :param exchange_rate:  The exchange rate between the transaction and settlement currency (settlement currency being represented by TotalConsideration.Currency). For example, if the transaction currency is USD and the settlement currency is GBP, this would be the appropriate USD/GBP rate.
        :type exchange_rate: float
        :param transaction_currency:  The transaction currency.
        :type transaction_currency: str
        :param properties:  A list of unique transaction properties and associated values to store for the transaction. Each property must be from the 'Transaction' domain.
        :type properties: dict[str, lusid_asyncio.PerpetualProperty]
        :param counterparty_id:  The identifier for the counterparty of the transaction.
        :type counterparty_id: str
        :param source:  The source of the transaction. This is used to look up the appropriate transaction group set in the transaction type configuration.
        :type source: str

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._transaction_id = None
        self._type = None
        self._instrument_identifiers = None
        self._transaction_date = None
        self._settlement_date = None
        self._units = None
        self._transaction_price = None
        self._total_consideration = None
        self._exchange_rate = None
        self._transaction_currency = None
        self._properties = None
        self._counterparty_id = None
        self._source = None
        self.discriminator = None

        self.transaction_id = transaction_id
        self.type = type
        self.instrument_identifiers = instrument_identifiers
        self.transaction_date = transaction_date
        self.settlement_date = settlement_date
        self.units = units
        if transaction_price is not None:
            self.transaction_price = transaction_price
        self.total_consideration = total_consideration
        self.exchange_rate = exchange_rate
        self.transaction_currency = transaction_currency
        self.properties = properties
        self.counterparty_id = counterparty_id
        self.source = source

    @property
    def transaction_id(self):
        """Gets the transaction_id of this TransactionRequest.  # noqa: E501

        The unique identifier of the transaction.  # noqa: E501

        :return: The transaction_id of this TransactionRequest.  # noqa: E501
        :rtype: str
        """
        return self._transaction_id

    @transaction_id.setter
    def transaction_id(self, transaction_id):
        """Sets the transaction_id of this TransactionRequest.

        The unique identifier of the transaction.  # noqa: E501

        :param transaction_id: The transaction_id of this TransactionRequest.  # noqa: E501
        :type transaction_id: str
        """
        if self.local_vars_configuration.client_side_validation and transaction_id is None:  # noqa: E501
            raise ValueError("Invalid value for `transaction_id`, must not be `None`")  # noqa: E501

        self._transaction_id = transaction_id

    @property
    def type(self):
        """Gets the type of this TransactionRequest.  # noqa: E501

        The type of the transaction, for example 'Buy' or 'Sell'. The transaction type must have been pre-configured using the System Configuration API. If not, this operation will succeed but you are not able to calculate holdings for the portfolio that include this transaction.  # noqa: E501

        :return: The type of this TransactionRequest.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this TransactionRequest.

        The type of the transaction, for example 'Buy' or 'Sell'. The transaction type must have been pre-configured using the System Configuration API. If not, this operation will succeed but you are not able to calculate holdings for the portfolio that include this transaction.  # noqa: E501

        :param type: The type of this TransactionRequest.  # noqa: E501
        :type type: str
        """
        if self.local_vars_configuration.client_side_validation and type is None:  # noqa: E501
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def instrument_identifiers(self):
        """Gets the instrument_identifiers of this TransactionRequest.  # noqa: E501

        A set of instrument identifiers that can resolve the transaction to a unique instrument.  # noqa: E501

        :return: The instrument_identifiers of this TransactionRequest.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._instrument_identifiers

    @instrument_identifiers.setter
    def instrument_identifiers(self, instrument_identifiers):
        """Sets the instrument_identifiers of this TransactionRequest.

        A set of instrument identifiers that can resolve the transaction to a unique instrument.  # noqa: E501

        :param instrument_identifiers: The instrument_identifiers of this TransactionRequest.  # noqa: E501
        :type instrument_identifiers: dict(str, str)
        """
        if self.local_vars_configuration.client_side_validation and instrument_identifiers is None:  # noqa: E501
            raise ValueError("Invalid value for `instrument_identifiers`, must not be `None`")  # noqa: E501

        self._instrument_identifiers = instrument_identifiers

    @property
    def transaction_date(self):
        """Gets the transaction_date of this TransactionRequest.  # noqa: E501

        The date of the transaction.  # noqa: E501

        :return: The transaction_date of this TransactionRequest.  # noqa: E501
        :rtype: str
        """
        return self._transaction_date

    @transaction_date.setter
    def transaction_date(self, transaction_date):
        """Sets the transaction_date of this TransactionRequest.

        The date of the transaction.  # noqa: E501

        :param transaction_date: The transaction_date of this TransactionRequest.  # noqa: E501
        :type transaction_date: str
        """
        if self.local_vars_configuration.client_side_validation and transaction_date is None:  # noqa: E501
            raise ValueError("Invalid value for `transaction_date`, must not be `None`")  # noqa: E501

        self._transaction_date = transaction_date

    @property
    def settlement_date(self):
        """Gets the settlement_date of this TransactionRequest.  # noqa: E501

        The settlement date of the transaction.  # noqa: E501

        :return: The settlement_date of this TransactionRequest.  # noqa: E501
        :rtype: str
        """
        return self._settlement_date

    @settlement_date.setter
    def settlement_date(self, settlement_date):
        """Sets the settlement_date of this TransactionRequest.

        The settlement date of the transaction.  # noqa: E501

        :param settlement_date: The settlement_date of this TransactionRequest.  # noqa: E501
        :type settlement_date: str
        """
        if self.local_vars_configuration.client_side_validation and settlement_date is None:  # noqa: E501
            raise ValueError("Invalid value for `settlement_date`, must not be `None`")  # noqa: E501

        self._settlement_date = settlement_date

    @property
    def units(self):
        """Gets the units of this TransactionRequest.  # noqa: E501

        The number of units of the transacted instrument.  # noqa: E501

        :return: The units of this TransactionRequest.  # noqa: E501
        :rtype: float
        """
        return self._units

    @units.setter
    def units(self, units):
        """Sets the units of this TransactionRequest.

        The number of units of the transacted instrument.  # noqa: E501

        :param units: The units of this TransactionRequest.  # noqa: E501
        :type units: float
        """
        if self.local_vars_configuration.client_side_validation and units is None:  # noqa: E501
            raise ValueError("Invalid value for `units`, must not be `None`")  # noqa: E501

        self._units = units

    @property
    def transaction_price(self):
        """Gets the transaction_price of this TransactionRequest.  # noqa: E501


        :return: The transaction_price of this TransactionRequest.  # noqa: E501
        :rtype: lusid_asyncio.TransactionPrice
        """
        return self._transaction_price

    @transaction_price.setter
    def transaction_price(self, transaction_price):
        """Sets the transaction_price of this TransactionRequest.


        :param transaction_price: The transaction_price of this TransactionRequest.  # noqa: E501
        :type transaction_price: lusid_asyncio.TransactionPrice
        """

        self._transaction_price = transaction_price

    @property
    def total_consideration(self):
        """Gets the total_consideration of this TransactionRequest.  # noqa: E501


        :return: The total_consideration of this TransactionRequest.  # noqa: E501
        :rtype: lusid_asyncio.CurrencyAndAmount
        """
        return self._total_consideration

    @total_consideration.setter
    def total_consideration(self, total_consideration):
        """Sets the total_consideration of this TransactionRequest.


        :param total_consideration: The total_consideration of this TransactionRequest.  # noqa: E501
        :type total_consideration: lusid_asyncio.CurrencyAndAmount
        """
        if self.local_vars_configuration.client_side_validation and total_consideration is None:  # noqa: E501
            raise ValueError("Invalid value for `total_consideration`, must not be `None`")  # noqa: E501

        self._total_consideration = total_consideration

    @property
    def exchange_rate(self):
        """Gets the exchange_rate of this TransactionRequest.  # noqa: E501

        The exchange rate between the transaction and settlement currency (settlement currency being represented by TotalConsideration.Currency). For example, if the transaction currency is USD and the settlement currency is GBP, this would be the appropriate USD/GBP rate.  # noqa: E501

        :return: The exchange_rate of this TransactionRequest.  # noqa: E501
        :rtype: float
        """
        return self._exchange_rate

    @exchange_rate.setter
    def exchange_rate(self, exchange_rate):
        """Sets the exchange_rate of this TransactionRequest.

        The exchange rate between the transaction and settlement currency (settlement currency being represented by TotalConsideration.Currency). For example, if the transaction currency is USD and the settlement currency is GBP, this would be the appropriate USD/GBP rate.  # noqa: E501

        :param exchange_rate: The exchange_rate of this TransactionRequest.  # noqa: E501
        :type exchange_rate: float
        """

        self._exchange_rate = exchange_rate

    @property
    def transaction_currency(self):
        """Gets the transaction_currency of this TransactionRequest.  # noqa: E501

        The transaction currency.  # noqa: E501

        :return: The transaction_currency of this TransactionRequest.  # noqa: E501
        :rtype: str
        """
        return self._transaction_currency

    @transaction_currency.setter
    def transaction_currency(self, transaction_currency):
        """Sets the transaction_currency of this TransactionRequest.

        The transaction currency.  # noqa: E501

        :param transaction_currency: The transaction_currency of this TransactionRequest.  # noqa: E501
        :type transaction_currency: str
        """

        self._transaction_currency = transaction_currency

    @property
    def properties(self):
        """Gets the properties of this TransactionRequest.  # noqa: E501

        A list of unique transaction properties and associated values to store for the transaction. Each property must be from the 'Transaction' domain.  # noqa: E501

        :return: The properties of this TransactionRequest.  # noqa: E501
        :rtype: dict[str, lusid_asyncio.PerpetualProperty]
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """Sets the properties of this TransactionRequest.

        A list of unique transaction properties and associated values to store for the transaction. Each property must be from the 'Transaction' domain.  # noqa: E501

        :param properties: The properties of this TransactionRequest.  # noqa: E501
        :type properties: dict[str, lusid_asyncio.PerpetualProperty]
        """

        self._properties = properties

    @property
    def counterparty_id(self):
        """Gets the counterparty_id of this TransactionRequest.  # noqa: E501

        The identifier for the counterparty of the transaction.  # noqa: E501

        :return: The counterparty_id of this TransactionRequest.  # noqa: E501
        :rtype: str
        """
        return self._counterparty_id

    @counterparty_id.setter
    def counterparty_id(self, counterparty_id):
        """Sets the counterparty_id of this TransactionRequest.

        The identifier for the counterparty of the transaction.  # noqa: E501

        :param counterparty_id: The counterparty_id of this TransactionRequest.  # noqa: E501
        :type counterparty_id: str
        """

        self._counterparty_id = counterparty_id

    @property
    def source(self):
        """Gets the source of this TransactionRequest.  # noqa: E501

        The source of the transaction. This is used to look up the appropriate transaction group set in the transaction type configuration.  # noqa: E501

        :return: The source of this TransactionRequest.  # noqa: E501
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this TransactionRequest.

        The source of the transaction. This is used to look up the appropriate transaction group set in the transaction type configuration.  # noqa: E501

        :param source: The source of this TransactionRequest.  # noqa: E501
        :type source: str
        """

        self._source = source

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
        if not isinstance(other, TransactionRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TransactionRequest):
            return True

        return self.to_dict() != other.to_dict()
