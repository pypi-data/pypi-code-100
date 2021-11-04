import logging

from dace import Dace

TARGET_DEFAULT_LIMIT = 10000


class TargetClass:
    __OBS_API_ENDPOINT = 'ObsAPI/'

    def __init__(self, dace_instance=None):
        # Logging configuration
        self.log = logging.getLogger("Target")
        self.log.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.log.addHandler(ch)

        if dace_instance is None:
            self.dace = Dace
        else:
            self.dace = dace_instance

    def query_database(self, limit=TARGET_DEFAULT_LIMIT, filters=None, sort=None, output_format=None):
        """
        Return data from Target Database

        :param limit: the max number of rows to retrieve
        :param filters: A dict to apply filters on columns (see example below)
        :param sort: A dict describing the sorting results (see example below)
        :param output_format: (optional) the format you want for result data : numpy, pandas, astropy_table (default (None) dict)

        :return: dict containing data from Target Database based on filters, sort and limit parameters

        .. code-block:: python

            from dace.target import Target

            target_data = Target.query_database(limit=10)

            for param in target_data:
                print(param, ':', target_data[param][:2])

            obj_id_basename : ['...', '...']
            obj_id_catname : ['...', '...']
            obj_pos_coordinates_hms_dms : ['...', '...']
            ins_name : ['...', '...']
            prog_id : ['...', '...']
            obj_sptype : ['...', '...']
            obj_pos_plx_mas : ['...', '...']
            obj_pos_pmdec_maspyr : ['...', '...']
            obj_pos_pmra_maspyr : ['...', '...']
            obj_flux_mag_b : ['...', '...']
            obj_flux_mag_g : ['...', '...']
            obj_flux_mag_h : ['...', '...']
        """
        if filters is None:
            filters = {}
        if sort is None:
            sort = {}

        return self.dace.transform_to_format(self.dace.get(self.__OBS_API_ENDPOINT + 'target' + '?limit=' + str(
            limit) + '&filters=' + self.dace.transform_dict_to_encoded_json(
            filters) + '&sort=' + self.dace.transform_dict_to_encoded_json(sort)), output_format=output_format)


Target = TargetClass()
