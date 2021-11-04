import logging

from dace import Dace

ASTROMETRY_DEFAULT_LIMIT = 10000


class AstrometryClass:

    def __init__(self, dace_instance=None):
        # Logging configuration
        self.log = logging.getLogger("Astrometry")
        self.log.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.log.addHandler(ch)

        if dace_instance is None:
            self.dace = Dace
        else:
            self.dace = dace_instance

    def query_database(self, limit=ASTROMETRY_DEFAULT_LIMIT, filters=None, sort=None, output_format=None):
        """
        Query astrometry database to retrieve data related to filters, sort and limit

        :param limit: the max number of rows to retrieve
        :param filters: A dict to apply filters on columns (see example below)
        :param sort: A dict describing the sorting results (see example below)
        :param output_format: (optional) the format you want for result data : numpy, pandas, astropy_table (default (None) dict)
        :return: A dict containing lists of values

        .. code-block:: python

            # To be completed
        """
        if filters is None:
            filters = {}
        if sort is None:
            sort = {}

        return self.dace.transform_to_format(
            self.dace.get(self.dace._OBS_API + 'observation/search/astrometry' + '?limit=' + str(
                limit) + '&filters=' + self.dace.transform_dict_to_encoded_json(
                filters) + '&sort=' + self.dace.transform_dict_to_encoded_json(sort)), output_format=output_format)

    def get_gaia_timeseries(self, target, output_format=None):
        """
        Get timeseries from Gaia astrometry

        :param target: The target name to retrieve astrometry data
        :param output_format: (optional) the format you want for result data : numpy, pandas, astropy_table (default (None) dict)
        :return: a dict containing astrometry timeseries vectors

        .. code-block:: python

            from dace.astrometry import Astrometry

            # To be completed

        """
        return self.dace.transform_to_format(
            self.dace.get(
                self.dace._OBS_API + 'observation/astrometry/' + target), output_format=output_format)


Astrometry = AstrometryClass()
