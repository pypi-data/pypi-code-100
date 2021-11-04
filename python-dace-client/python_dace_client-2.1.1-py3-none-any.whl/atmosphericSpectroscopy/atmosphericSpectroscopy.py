import logging

from dace import Dace

ATMOSPHERIC_DEFAULT_LIMIT = 10000


class AtmosphericSpectroscopyClass:
    __OBSERVATION_ENDPOINT = 'ObsAPI/observation/'

    def __init__(self, dace_instance=None):
        # Logging configuration
        self.log = logging.getLogger("AtmosphericSpectroscopy")
        self.log.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.log.addHandler(ch)

        if dace_instance is None:
            self.dace = Dace
        else:
            self.dace = dace_instance

    def query_database(self, limit=ATMOSPHERIC_DEFAULT_LIMIT, filters=None, sort=None, output_format=None):
        """
        Return atmospheric spectroscopy data based on filters, sort and limit
        :param filters: JSON filters you want to apply following this format : '{"obj_id_catname":{"contains":"GJ436"}
        :param sort: JSON sorting filed to describe how sort with data must be done : '{"obj_id_catname":"ASC"}'
        :param limit: the number of rows you want to receive
        :param output_format: (optional) the format you want for result data : numpy, pandas, astropy_table (default (None) dict)

        :return: dict with atmospheric spectroscopy data

        .. code-block:: python

            from dace.atmosphericSpectroscopy import AtmosphericSpectroscopy

            # Query the database
            atmosphericSpectroscopy_data = AtmosphericSpectroscopy.query_database()

            # Print the 2 first elements of each column
            for param in atmosphericSpectroscopy_data:
                print(param, ':', atmosphericSpectroscopy_data[param][:2])

            # Output:
            obj_id_catname : [...]
            obj_id_name : [...]
            spectral_domains : [...]
            ins_name : [...]
            spectral_transitions : [...]
            pub_bibcode : [...]
            description : [...]
            prog_id : [...]
            obs_type : [...]
            file_rootpath : [...]

        """
        if filters is None:
            filters = {}
        if sort is None:
            sort = {}

        return self.dace.transform_to_format(
            self.dace.get(self.__OBSERVATION_ENDPOINT + 'atmosphericSpectroscopy' + '?limit=' + str(
                limit) + '&filters=' + self.dace.transform_dict_to_encoded_json(
                filters) + '&sort=' + self.dace.transform_dict_to_encoded_json(sort)), output_format=output_format)


AtmosphericSpectroscopy = AtmosphericSpectroscopyClass()
