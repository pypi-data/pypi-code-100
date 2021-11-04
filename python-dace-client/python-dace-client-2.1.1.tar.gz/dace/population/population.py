import logging
import urllib.parse

from dace import Dace


class PopulationClass:
    """
    Use this class to query Population/Evolution on from DACE

    .. versionadded:: 1.3.0
    """

    SNAPSHOTS_DEFAULT_COLUMN = ['system_id', 'planet_id', 'total_mass', 'semi_major_axis', 'total_radius', 'total_lum']
    SIMULATIONS_DEFAULT_COLUMN = ['total_mass', 'semi_major_axis', 'total_radius', 'total_lum']
    __POPULATION_API = 'PopulationAPI/'

    def __init__(self, dace_instance=None):
        # Logging configuration
        self.log = logging.getLogger("Population")
        self.log.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.log.addHandler(ch)

        if dace_instance is None:
            self.dace = Dace
        else:
            self.dace = dace_instance

    def query_database(self, output_format=None):
        """
        Query population database to get available population descriptions.

        :param output_format: (optional) the format you want for result data : numpy, pandas, astropy_table (default (None) dict)
        :return: A dictionary containing the list of populations with the name and descriptions

        .. code-block:: python

            from dace.population import Population

            # Query the database
            populations = Population.query_database()

            # Print the 2 population description
            for param in populations:
                print(param, ':', populations[param][:2])

            # Output:
            order: [...]
            population_id: [...]
            image: [...]
            description: [...]
            name: [...]
            visibility: [...]
        """
        return self.dace.transform_to_format(self.dace.get(self.__POPULATION_API + 'population/search'),
                                             output_format=output_format)

    def get_columns(self, population_id, output_format=None):
        """
        Get the available columns for the specified population

        :param population_id: the specific population to get columns
        :param output_format: (optional) the format you want for result data : numpy, pandas, astropy_table (default (None) dict)
        :return: a dict containing all column information (name, label,...)

        .. code-block:: python

            from dace.population import Population

            # Query the database
            columns = Population.get_columns('ng75')

            # Print the 2 population description
            for param in columns:
                print(param, ':', columns[param][:2])

            # Output:
            label [...]
            name [...]
            type [...]
            ordinal [...]
        """
        return self.dace.transform_to_format(
            self.dace.get(self.__POPULATION_API + 'population/' + population_id + '/variables'),
            output_format=output_format)

    def get_snapshots(self, population_id, years, columns=None, output_format=None):
        """
        Get snapshots data for a specific population and a specific age

        :param population_id: the population id to get snapshots
        :param years: the specific age of the snapshot (5Gyr, 6Gyr,...)
        :param columns: a list of specific columns to retrieve
        :param output_format: (optional) the format you want for result data : numpy, pandas, astropy_table (default (None) dict)
        :return: a dict containing a list of snapshots data for the specified population, age and columns. Note that an additional vector of boolean is sent corresponding to the 'valid' flag

        .. code-block:: python

            from dace.population import Population

            # Query the database
            snapshots = Population.get_snapshots('ng75', 5000000, columns=['system_id', 'planet_id', 'total_mass'])

            # Print the snapshots
            for param in columns:
                print(param, ':', columns[param][:2])

            # Output:
            planet_id: [...]
            system_id: [...]
            total_mass: [...]
            valid: [...]

        """
        if columns is None:
            columns = self.SNAPSHOTS_DEFAULT_COLUMN
        return self.dace.transform_to_format(
            self.dace.get(self.__POPULATION_API + 'population/' + population_id + '/snapshots/' + str(years) + '?' +
                          urllib.parse.urlencode({'col': columns}, True)), output_format=output_format)

    def get_snapshot_ages(self):
        """
        Use this method to get all snapshot ages
        :return: a list with all ages existing in population module
        """
        snapshot_ages = []
        for exp in range(5, 10):
            for base in range(1, 10):
                age = base * 10.0 ** exp
                snapshot_ages.append(age)
        snapshot_ages.append(1E10)
        return snapshot_ages

    def get_track(self, population_id, system_id, planet_id, columns=None, output_format=None):
        """
        Get the tracks for a specific population and a specific system ID and planet ID

        :param population_id: the population id to retrieve tracks
        :param system_id: the system ID (1,2,...)
        :param planet_id: the planet ID (1,2,...)
        :param columns: the list of columns to retrieve
        :param output_format: (optional) the format you want for result data : numpy, pandas, astropy_table (default (None) dict)
        :return: a dict with the tracks data for the specified population ID, system ID, planet ID and specified columns

        .. code-block:: python

            from dace.population import Population

            # Query the database
            tracks = Population.get_track('ng75', 1, 1, columns=['time_yr', 'total_mass'])

            # Print the tracks
            for param in columns:
                print(param, ':', columns[param][:2])

            # Output:
            time_yr: [...]
            total_mass: [...]

        """
        if columns is None:
            columns = self.SIMULATIONS_DEFAULT_COLUMN

        return self.dace.transform_to_format(self.dace.get(self.__POPULATION_API + 'population/' + population_id +
                                                           '/' + str(system_id) + '/' + str(planet_id) +
                                                           '/simulations?' +
                                                           urllib.parse.urlencode({'col': columns}, True)),
                                             output_format=output_format)


Population = PopulationClass()
