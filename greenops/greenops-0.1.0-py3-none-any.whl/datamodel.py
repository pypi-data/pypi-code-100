"""
greenops
--------

Software to measure the footprints of deep learning models at training,
testing and evaluating to reduce energy consumption and carbon footprints.

Copyright rixel 2021
Distributed under the MIT License.
See accompanying file LICENSE.

File: submodule datamodel
"""


from abc import ABC, abstractmethod

from .functions import percentify


class DictInterface(ABC):
    """
    Interface to serialize and deserialize
    ======================================
    """


    @property
    @abstractmethod
    def as_dict(self) -> dict:
        """
        Serialize the object to dict
        ============================

        Returns
        -------
        dict
            Object's data.
        """


    @staticmethod
    @abstractmethod
    def from_dict(data : dict, throw_error : bool = False) -> any:
        """
        Deserialize the object from a dict
        ==================================

        Parameters
        ----------
        data : dict
            Data to deserialize the object from.
        throw_error : bool, optional (False if omitted)
            Whether to throw error or not.
        """


class DeviceData(DictInterface):
    """
    Represent data of a device
    ==========================
    """


    def __init__(self, short_name : str, long_name : str, consumption : float):
        """
        Initialize the object
        =====================

        Parameters
        ----------
        short_name : str
            Long name of the device.
        long_name : str
            Short name of the device.
        consumption : float
            Consuption of the device.
        """

        self.__short_name = short_name
        self.__long_name = long_name
        self.__consumption = float(consumption)


    @property
    def as_dict(self) -> dict:
        """
        Serialize the object to dict
        ============================

        Returns
        -------
        dict
            Object's data.
        """

        return {'ShortName' : self.__short_name,
                'LongName' : self.__long_name,
                'Consumption' : self.__consumption}


    @property
    def consumption(self) -> float:
        """
        Get the consumption of the device
        =================================

        Returns
        -------
        float
            Consuption of the device.
        """

        return self.__consumption


    @staticmethod
    def from_dict(data : dict, throw_error : bool = False) -> any:
        """
        Deserialize the object from a dict
        ==================================

        Parameters
        ----------
        data : dict
            Data to deserialize the object from.
        throw_error : bool, optional (False if omitted)
            Whether to throw error or not.

        Raises
        ------
        ValueError
            When the data doesn't satisfy the needs to restore the object from.
        """

        result = None
        if all(['Consumption' in data.keys(), 'LongName' in data.keys(),
                'ShortName' in data.keys()]):
            result = DeviceData(data['ShortName'], data['LongName'],
                                data['Consumption'])
        elif throw_error:
            raise ValueError('greenops.datamodel.DeviceData.from_dict(): ' +
                             'Cannot restore device from invalid data.')
        return result


    @property
    def long_name(self) -> str:
        """
        Get the long name of the device
        ===============================

        Returns
        -------
        str
            Long name of the device.
        """

        return self.__long_name


    @property
    def short_name(self) -> str:
        """
        Get the short name of the device
        ================================

        Returns
        -------
        str
            Short name of the device.
        """

        return self.__short_name


    def __repr__(self) -> str:
        """
        Represent the object
        ====================

        Returns
        -------
        str
            Code snippet to regenerate the object.
        """

        return 'DeviceData({}, {}, {})'.format(self.__short_name,
                self.__long_name, self.__consumption)


    def __str__(self) -> str:
        """
        Information about the object
        ============================

        Returns
        -------
        str
            Human readable description of the object.
        """

        return 'Device "{}" ("{}") consumes {} Watts.'.format(self.__long_name,
                self.__short_name, self.__consumption)


class PowerPriceData(DictInterface):
    """
    Represent power consumption data
    ================================
    """


    def __init__(self, country_code : str, country_name : str,
                 price : float):
        """
        Initialize the object
        =====================

        Parameters
        ----------
        country_code : str
            Two letters `ISO 3166-1 alpha-2` country code.
        country_name : str
            Name of the country.
        price : float
            Electricity price of the country (1 kWh in USD).
        """

        self.__country_code = country_code
        self.__country_name = country_name
        self.__price = float(price)


    @property
    def as_dict(self) -> dict:
        """
        Serialize the object to dict
        ============================

        Returns
        -------
        dict
            Object's data.
        """

        return {'CountryCode' : self.__country_code,
                'CountryName' : self.__country_name,
                'Price' : self.__price}


    @property
    def country_code(self) -> str:
        """
        Got country code
        ================

        Returns
        -------
        str
            Two letters `ISO 3166-1 alpha-2` country code.
        """

        return self.__country_code


    @property
    def country_name(self) -> str:
        """
        Get name of the country
        =======================

        Returns
        -------
        str
            Name of the country.
        """

        return self.__country_name


    @staticmethod
    def from_dict(data : dict, throw_error : bool = False) -> any:
        """
        Deserialize the object from a dict
        ==================================

        Parameters
        ----------
        data : dict
            Data to deserialize the object from.
        throw_error : bool, optional (False if omitted)
            Whether to throw error or not.

        Raises
        ------
        ValueError
            When the data doesn't satisfy the needs to restore the object from.
        """

        result = None
        if all(['CountryCode' in data.keys(), 'CountryName' in data.keys(),
                'Price' in data.keys()]):
            result = PowerPriceData(data['CountryCode'], data['CountryName'],
                                   data['Price'])
        elif throw_error:
            raise ValueError('greenops.datamodel.PowerPriceData.from_dict(): ' +
                             'Cannot restore device from invalid data.')
        return result


    @property
    def price(self) -> float:
        """
        Get electricity price
        =====================

        Returns
        -------
        str
            Electricity price of the country (1 kWh in USD).
        """

        return self.__price


    def __repr__(self) -> str:
        """
        Represent the object
        ====================

        Returns
        -------
        str
            Code snippet to regenerate the object.
        """

        return 'PowerPrice({}, {}, {})'.format(self.__country_code,
                self.__country_name, self.__price)

    def __str__(self) -> str:
        """
        Information about the object
        ============================

        Returns
        -------
        str
            Human readable description of the object.
        """

        return 'Electricity in {} [{}] costs {} '.format(self.__country_name,
                self.__country_code, self.__price
                ) + 'in USD per kilowatt-hour (kWh)'


class PowerSourcesData(DictInterface):
    """
    Represent power source rates in a country
    =========================================
    """

    # pylint: disable=too-many-instance-attributes
    #         It could be transformed to functions but wouldn't have sense.


    def __init__(self, country_code : str, country_name : str, coal : float,
                 gas : float, hydro : float, other_renewables : float,
                 solar : float, oil : float, wind : float, nuclear : float):
        """
        Initialize the object
        =====================

        Parameters
        ----------
        country_code : str
            Two letters `ISO 3166-1 alpha-2` country code.
        country_name : str
            Name of the country.
        coal : float
            Rate of coal in the electricity production.
        gas : float
            Rate of gas in the electricity production.
        hydro : float
            Rate of hydroelectric power in the electricity production.
        other_renewables : float
            Rate of other resources in the electricity production.
        solar : float
            Rate of solar power in the electricity production.
        oil : float
            Rate of oil in the electricity production.
        wind : float
            Rate of wind power in the electricity production.
        nuclear : float
            Rate of nuclear power in the electricity production.

        Notes
        -----
            Sum of resource types must be 1.0.
        """

        # pylint: disable=too-many-arguments
        #         Number of parameters accords to number of attributes.

        self.__country_code = country_code
        self.__country_name = country_name
        self.__coal = float(coal)
        self.__gas = float(gas)
        self.__hydro = float(hydro)
        self.__other_renewables = float(other_renewables)
        self.__solar = float(solar)
        self.__oil = float(oil)
        self.__wind = float(wind)
        self.__nuclear = float(nuclear)


    @property
    def as_dict(self) -> dict:
        """
        Serialize the object to dict
        ============================

        Returns
        -------
        dict
            Object's data.
        """

        return {'CountryCode' : self.__country_code,
                'CountryName' : self.__country_name,
                'Coal' : self.__coal, 'Gas' : self.__gas,
                'Hydro' : self.__hydro,
                'OtherRenewables' : self.__other_renewables,
                'Solar' : self.__solar, 'Oil' : self.__oil,
                'Wind' : self.__wind, 'Nuclear' : self.__nuclear}


    @property
    def coal(self) -> float:
        """
        Get coal rate
        =============

        Returns
        -------
        float
            Rate of coal in the electricity production.
        """

        return self.__coal


    @property
    def country_code(self) -> str:
        """
        Get country code
        ================

        Returns
        -------
        str
            Two letters `ISO 3166-1 alpha-2` country code.
        """

        return self.__country_code


    @property
    def country_name(self) -> str:
        """
        Get name of the country
        =======================

        Returns
        -------
        str
            Name of the country.
        """

        return self.__country_name


    @staticmethod
    def from_dict(data : dict, throw_error : bool = False) -> any:
        """
        Deserialize the object from a dict
        ==================================

        Parameters
        ----------
        data : dict
            Data to deserialize the object from.
        throw_error : bool, optional (False if omitted)
            Whether to throw error or not.

        Raises
        ------
        ValueError
            When the data doesn't satisfy the needs to restore the object from.
        """

        result = None
        if all(['CountryCode' in data.keys(), 'CountryName' in data.keys(),
                'Coal' in data.keys(), 'Gas' in data.keys(),
                'Hydro' in data.keys(), 'OtherRenewables' in data.keys(),
                'Solar' in data.keys(), 'Oil' in data.keys(),
                'Wind' in data.keys(), 'Nuclear' in data.keys()]):
            result = PowerSourcesData(data['CountryCode'], data['CountryName'],
                                      data['Coal'], data['Gas'], data['Hydro'],
                                      data['OtherRenewables'], data['Solar'],
                                      data['Oil'], data['Wind'],
                                      data['Nuclear'])
        elif throw_error:
            raise ValueError('greenops.datamodel.PowerSourcesData.from_dict():'
                             + ' Cannot restore device from invalid data.')
        return result


    @property
    def gas(self) -> float:
        """
        Get gas rate
        ============

        Returns
        -------
        float
            Rate of gas in the electricity production.
        """

        return self.__gas


    @property
    def hydro(self) -> float:
        """
        Get rate of hydroelectric power
        ===============================

        Returns
        -------
            Rate of hydroelectric power in the electricity production.
        """

        return self.__hydro


    @property
    def nuclear(self) -> float:
        """
        Get rate of nuclear power
        =========================

        Returns
        -------
            Rate of nuclear power in the electricity production.
        """

        return self.__nuclear


    @property
    def oil(self) -> float:
        """
        Get oil rate
        ============

        Returns
        -------
        float
            Rate of oil in the electricity production.
        """

        return self.__oil


    @property
    def other_renewables(self) -> float:
        """
        Get rate of other resources
        ===========================

        Returns
        -------
            Rate of other resources in the electricity production.
        """

        return self.__other_renewables


    @property
    def solar(self) -> float:
        """
        Get rate of solar power
        =======================

        Returns
        -------
            Rate of solar power in the electricity production.
        """

        return self.__solar


    @property
    def wind(self) -> float:
        """
        Get rate of wind power
        ======================

        Returns
        -------
            Rate of wind power in the electricity production.
        """

        return self.__wind


    def __repr__(self) -> str:
        """
        Represent the object
        ====================

        Returns
        -------
        str
            Code snippet to regenerate the object.
        """

        return 'PowerSources({}, {}, {}, {}, {}, {}, {}, {}, {}, {})'.format(
                self.__country_code, self.__country_name, self.__coal,
                self.__gas, self.__hydro, self.__other_renewables,
                self.__solar, self.__oil, self.__wind, self.__nuclear)

    def __str__(self) -> str:
        """
        Information about the object
        ============================

        Returns
        -------
        str
            Human readable description of the object.
        """

        return 'Electricity in {} [{}] is produced '.format(self.__country_name,
                self.__country_code) + 'from coal {}, oil {}, gas {}, '.format(
                percentify(self.__coal), percentify(self.__oil), percentify(
                self.__gas)) + 'nuclear power {}, hydroelectric power '.format(
                percentify(self.__nuclear)) + '{}, solar power {}, wind'.format(
                percentify(self.__hydro), percentify(self.__solar)
                ) + ' power {}, other renewable sources {}'.format(percentify(
                self.__wind), percentify(self.__other_renewables))


class Response:
    """
    Represent response data
    =======================
    """


    def __init__(self, query_str : str, error_str : str, result_equals : list,
                 result_contains : list):
        """
        Initialize the object
        =====================

        Parameters
        ----------
        query_str : str
            Query string returned from the API.
        error_str : str
            Error string sent by the API.
        result_equals : list
            List of results that fully match the query string.
        result_contains : list
            List of results that partially match the query string.
        """

        self.__query = query_str
        self.__error = error_str
        self.__strict_match = result_equals
        self.__partial_match = result_contains


    @property
    def error(self) -> str:
        """
        Get error string
        ================

        Returns
        -------
        str
            Error string sent by the API.
        """

        return self.__error


    @staticmethod
    def from_dict(data : dict, result_type : any) -> any:
        """
        Deserialize the object from a dict
        ==================================

        Parameters
        ----------
        data : dict
            Data to deserialize the object from.
        throw_error : bool, optional (False if omitted)
            Whether to throw error or not.
        """

        result = None
        if isinstance(data, dict):
            if all(['query' in data.keys(), 'error' in data.keys(),
                    'result' in data.keys()]):
                if isinstance(data['result'], dict):
                    if all(['equals' in data['result'].keys(),
                            'contains' in data['result'].keys(),]):
                        result = Response(data['query'], data['error'],
                                          [result_type.from_dict(e)
                                          for e in data['result']['equals']],
                                          [result_type.from_dict(e)
                                          for e in data['result']['contains']])
        return result


    @property
    def is_good(self) -> bool:
        """
        Get object's state
        ==================

        Returns
        -------
        bool
            True, if erros string is empty, False if not.
        """

        return len(self.__error) == 0


    @property
    def partial_match(self) -> list:
        """
        Get partial matches
        ===================

        Returns
        -------
        list
            List of results that partially match the query string.
        """

        return self.__partial_match


    @property
    def query(self) -> str:
        """
        Get query
        =========

        Returns
        -------
        str
            Query string returned from the API.
        """

        return self.__query


    @property
    def strict_match(self) -> list:
        """
        Get total matches
        =================

        Returns
        -------
        list
            List of results that fully match the query string.
        """

        return self.__strict_match
