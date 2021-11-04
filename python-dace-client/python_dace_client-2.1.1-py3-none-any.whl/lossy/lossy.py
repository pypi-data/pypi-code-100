import logging

from dace import Dace

LOSSY_DEFAULT_LIMIT = 10000


class LossyClass:
    """
    Use this class to query Lossy module on DACE

    .. versionadded:: 1.3.0
    """

    __LOSSY_API = 'LossyAPI/'

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

    def query_database(self, filters=None, sort=None, limit=LOSSY_DEFAULT_LIMIT, output_format=None):
        """
        Retrieve lossy samples

        :param filters: dictionary containing filters based on the column names
        :param sort: Dictionary describing how to sort data based on the column name
        :param limit: maximum number of results
        :param output_format: the format you want for result data : numpy, pandas, astropy_table (default (None) dict)
        :return: A dictionary of list containing the sample meta data

        .. code-block:: python

            from dace.lossy import Lossy

            # Query the database
            samples = Lossy.query_database(filters={'sample_id': {'contains': 'SPIPA'}}, sort={'sample_id': 'asc'})

            # Print the 2 first elements of each column
            for param in samples:
                print(param, ':', samples[param][:2])

            # Output:
            sample_id: [...],
            publication: [...],
            experimentalist: [...],
            date: [...],
            visibility: [...],
            temperature: [...]

        """
        if filters is None:
            filters = {}
        if sort is None:
            sort = {}

        return self.dace.transform_to_format(self.dace.get(self.__LOSSY_API + 'sample/search' + '?limit=' + str(
            limit) + '&filters=' + self.dace.transform_dict_to_encoded_json(
            filters) + '&sort=' + self.dace.transform_dict_to_encoded_json(sort)), output_format=output_format)

    def get_sample(self, sample_id, output_format=None):
        """
        Get the data for a specific sample

        :param sample_id: the sample_id for which we want to retrieve data
        :param output_format: the format you want for result data : numpy, pandas, astropy_table (default (None) dict)
        :return: A dict of list containing the sample values

        .. code-block:: python

            from dace.lossy import Lossy

            # Query sample
            sample = Lossy.get_sample('SAMPLE_millbillillie_20110525_000')

            # Print the 2 first elements of each column
            for param in sample:
                print(param, ':', sample[param][:2])

            # Output
            sample_id: [...],
            azimuth: [...]
            quality_flag: [...],
            absolute_time: [...],
            air_temperature: [...],
            relative_time: [...],
            reflectance_factor: [...],
            phase: [...],
            bandpass_fwhm: [...],
            counter: [...],
            incidence: [...],
            air_humidity: [...],
            bandpass_central: [...],
            standard_deviation: [...],
            emission: [...],
            sample_temperature: [...],
            error_estimate: [...]
        """

        return self.dace.transform_to_format(self.dace.get(self.__LOSSY_API + 'sample/' + sample_id),
                                             output_format=output_format)


Lossy = LossyClass()
