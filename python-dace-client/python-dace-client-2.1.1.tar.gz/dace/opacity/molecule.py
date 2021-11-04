import json
import logging

from dace import Dace

MOLECULE_DEFAULT_LIMIT = 10000


class MoleculeClass:

    def __init__(self, dace_instance=None):
        self.__OPACITY_API = 'OpacityAPI/'

        # Logging configuration
        self.log = logging.getLogger("Opacity")
        self.log.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.log.addHandler(ch)

        if dace_instance is None:
            self.dace = Dace
        else:
            self.dace = dace_instance

    def query_database(self, limit=MOLECULE_DEFAULT_LIMIT, filters=None, sort=None, output_format=None):
        """
        Query opacity.molecule database

        :param limit: the max number of rows to retrieve
        :param filters: A dict to apply filters on columns (see example below)
        :param sort: A dict describing the sorting results (see example below)
        :param output_format: (optional) the format you want for result data : numpy, pandas, astropy_table (default (None) dict)
        :return: A dict containing result based on parameters

        .. code-block:: python

            from dace.opacity import Molecule

            # Query the database
            data = Molecule.query_database(limit=10)

            # Print the 2 first elements of each column
            for param in data:
                print(param, ':', data[param][:2])

            # Output:
            ...

        """
        if filters is None:
            filters = {}
        if sort is None:
            sort = {}

        return self.dace.transform_to_format(
            self.dace.get(self.__OPACITY_API + 'molecule/search' + '?limit=' + str(
                limit) + '&filters=' + self.dace.transform_dict_to_encoded_json(
                filters) + '&sort=' + self.dace.transform_dict_to_encoded_json(sort)), output_format=output_format)

    def download(self, isotopologue, line_list, version, temperature_boundaries, pressure_boundaries,
                 output_directory=None, output_filename=None):
        """
        Download opacities molecules

        :param isotopologue: isotopologue you want data for
        :param line_list: molecule line_list you want data for
        :param version: isotopologue, line_list version you want data for
        :param temperature_boundaries: the min, max of temperature you want as a tuple. Example : (2500, 3000)
        :param pressure_boundaries: the min, max exponent of pressure you want as a tuple. Example : (2.5, 3)
        :param output_directory: (optional) the target directory where you want to download the file
        :param output_filename: (optional) the target filename where you want to download the file

        .. code-block:: python

            from dace.opacity import Molecule

            Molecule.download('1H2-16O', 'POKAZATEL', 1.0, (2500, 2600), (2.5, 3), output_directory='/tmp', output_filename='test_molecule.tar.gz')
        """
        self.dace.download_file(
            self.__OPACITY_API + 'molecule/download/' + isotopologue + '/' + line_list + '?tMin=' + str(
                temperature_boundaries[0]) + '&tMax=' + str(temperature_boundaries[1]) + '&pMinExp=' + str(
                pressure_boundaries[0]) + '&pMaxExp=' + str(pressure_boundaries[1]) + '&version=' + str(version),
            output_directory=output_directory, output_filename=output_filename)

    def get_data(self, isotopologue, line_list, version, temperature, pressure_exponent, output_format=None):
        """
              Get data of an isotopologue, line_list, version, temperature and pressure_exponent

              :param isotopologue: isotopologue you want data for
              :param line_list: opacity line_list you want data for
              :param version: isotopologue, line_list version you want data for
              :param temperature: temperature you want data for
              :param pressure_exponent: pressure exponent you want data for
              :param output_format: (optional) the format you want for result data : numpy, pandas, astropy_table (default (None) dict)
              :return: An object (dict by default. See output_format) containing result based on parameters

              .. code-block:: python

                  from dace.opacity import Molecule

                  # Query the database
                  data = Molecule.get_data('1H2-16O', 'POKAZATEL', 1.0, 300, -1.33)

                  # Print the 2 first elements of each column
                  for param in data:
                      print(param, ':', data[param][:2])

                  # Output:
                  ...

              """
        return self.dace.transform_to_format(
            self.dace.get(
                self.__OPACITY_API + 'molecule/data/' + isotopologue + '/' + line_list + '?temperature=' + str(
                    temperature) + '&pressureExp=' + str(pressure_exponent) + '&version=' + str(version)),
            output_format=output_format)

    def get_high_resolution_data(self, isotopologue, line_list, version, temperature, pressure_exponent,
                                 wavenumber_boundaries,
                                 output_format=None):
        """
              Get high resolution data from binary file based on isotopologue, line_list, temperature pressure_exponent and wavenumber_boundaries

              :param isotopologue: isotopologue you want data for
              :param line_list: opacity line_list you want data for
              :param version: isotopologue, line_list version you want data for
              :param temperature: temperature you want data for
              :param pressure_exponent: pressure exponent you want data for
              :param wavenumber_boundaries: the wavenumber min, max you want extracted from the binary high precision file. Example : (1.01, 3.02)
              :param output_format: (optional) the format you want for result data : numpy, pandas, astropy_table (default (None) dict)
              :return: An object (dict by default. See output_format) containing result based on parameters

              .. code-block:: python

                  from dace.opacity import Molecule

                  # Query the database
                  data = Molecule.get_high_resolution_data('1H2-16O', 'POKAZATEL', 1.0, 300, -1.33, (1.01, 3.02))

                  # Print the 2 first elements of each column
                  for param in data:
                      print(param, ':', data[param][:2])

                  # Output:
                  ...

              """
        return self.dace.transform_to_format(
            self.dace.get(
                self.__OPACITY_API + 'molecule/highresolutiondata/' + isotopologue + '/' + line_list + '?temperature='
                + str(temperature) + '&pressureExp=' + str(pressure_exponent) + '&wavenumberStart=' + str(
                    wavenumber_boundaries[0]) + '&wavenumberEnd=' + str(wavenumber_boundaries[1]) + '&version=' + str(
                    version)),
            output_format=output_format)

    def interpolate(self, isotopologue, line_list, version, interpol_temperatures, interpol_pressures,
                    output_directory=None, output_filename=None):
        """
              Compute interpolation for an isotopologue, line_list and lists of interpol_temperatures,
              interpol_pressures and return a file with the interpolated data (joined with refFile if it exsits)

              :param isotopologue: isotopologue you want data for
              :param line_list: opacity line_list you want data for
              :param version: isotopologue, line_list version you want data for
              :param interpol_temperatures: list of temperatures you want to interpolate
              :param interpol_pressures: list of pressures you want to interpolate

              .. code-block:: python

                  from dace.opacity import Molecule

                  # Query the database
                  Molecule.interpolate('1H2-16O', 'POKAZATEL', 1.0, [110], [0.4], output_directory='/tmp', output_filename='opacity_molecule_interpolate.tar.gz')

                  # Print the 2 first elements of each column
                  for param in data:
                      print(param, ':', data[param][:2])

                  # Output:
                  ...
        """
        download_id = \
            self.dace.post(
                self.__OPACITY_API + 'molecule/interpolate/' + isotopologue + '/' + line_list + '?version=' + str(
                    version),
                data=json.dumps({'interpol_temperatures': interpol_temperatures,
                                 'interpol_pressures': interpol_pressures}))['values'][0]
        self.dace.download_file(self.__OPACITY_API + 'molecule/interpolate/' + download_id,
                                output_directory=output_directory,
                                output_filename=output_filename)


Molecule = MoleculeClass()
