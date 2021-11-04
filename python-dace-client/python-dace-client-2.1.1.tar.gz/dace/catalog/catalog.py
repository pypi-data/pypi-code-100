import logging

from dace import Dace

CATALOG_DEFAULT_LIMIT = 10000


class CatalogClass:

    def __init__(self, dace_instance=None):
        # Logging configuration
        self.log = logging.getLogger("Catalog")
        self.log.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.log.addHandler(ch)

        if dace_instance is None:
            self.dace = Dace
        else:
            self.dace = dace_instance

    def query_database(self, catalog, limit=CATALOG_DEFAULT_LIMIT, filters=None, sort=None, output_format=None):
        """
        Return catalog data like tess, k2, naco-ispy or cheops

        :param catalog: the catalog you want data for. For example : tess, k2
        :param limit: the number of rows you want to receive (max is 10000)
        :param filters: JSON filters you want to apply following this format : '{"obj_id_twomass":{"contains":"111"}, "obj_id_hip":{"contains":"222"}}'
        :param sort: JSON sorting filed to describe how sort with data must be done : '{"obj_id_toi":"asc"}'
        :param output_format: (optional) the format you want for result data : numpy, pandas, astropy_table (default (None) dict)
        :return: dict containing vectors of data related to the mission, filter and sorting applied


        .. code-block:: python

            from dace.catalog import Catalog

            catalog_data = Catalog.query_database('tess')

            for param in catalog_data:
                print(param, ':', catalog_data[param][:2])

            obj_id_tic : [...]
            obj_pos_coordinates_hms_dms : [...]
            obj_id_toi : [...]
            obj_id_hip : [...]
            obj_id_twomass : [...]
            db_lc_available : [...]
            db_rv_available : [...]
            obj_prox : [...]
            obj_phys_rho_err : [...]
            obj_pos_gallat : [...]
            obj_pos_plx_mas : [...]
            obj_phys_rho : [...]
            obj_pos_pmdec_mas : [...]
            obj_phys_radius : [...]
            obj_pos_pmra_mas_err : [...]
            obj_pos_eclong : [...]
            obj_pos_pmdec_mas_err : [...]
        """
        if filters is None:
            filters = {}
        if sort is None:
            sort = {}

        return self.dace.transform_to_format(
            self.dace.get('ObsAPI/catalog/' + catalog + '?limit=' + str(
                limit) + '&filters=' + self.dace.transform_dict_to_encoded_json(
                filters) + '&sort=' + self.dace.transform_dict_to_encoded_json(sort)), output_format=output_format)


Catalog = CatalogClass()
