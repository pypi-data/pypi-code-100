import logging

from dace import Dace

EXOPLANET_DEFAULT_LIMIT = 10000


class ExoplanetClass:
    """ Exoplanet let user query exoplanet database in DACE """
    __EXOPLANET_ENDPOINT = 'ExoplanetAPI/exoplanetDatabase'

    def __init__(self, dace_instance=None):
        # Logging configuration
        self.log = logging.getLogger("Exoplanet")
        self.log.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.log.addHandler(ch)

        if dace_instance is None:
            self.dace = Dace
        else:
            self.dace = dace_instance

    def query_database(self, limit=EXOPLANET_DEFAULT_LIMIT, filters=None, sort=None, output_format=None):
        """
        Get exoplanet data related to filters, sorting and limit of rows

        :Example:

            .. code-block:: python

                from dace.exoplanet import Exoplanet

                exoplanet_data = Exoplanet.query_database(filters={'db_info_name':{'contains':'Exoplanets.org'}}
                , sort={'db_info_name':'asc'})

                # List of db_info_names : "Exoplanets.org", "Exoplanet.eu", "Open Exoplanet Catalog" and
                # "Nasa Exoplanet Archive"

        :param filters: JSON filter following this format : '{"db_info_name":{"contains":"Exoplanets.org"},
                        "obj_id_catname":{"contains":"HD40307"}}'
        :param sort: JSON sorting filed to describe how sort with data must be done : '{"db_info_name":"asc"}'
        :param limit: the number of rows you would like to receive (after applying filters and sort).
                        If nothing is given, the default limit is 50000
        :param output_format: (optional) the format you want for result data : numpy, pandas, astropy_table (default (None) dict)

        :return: dict containing exoplanet data based on filters, sort and limit

        .. code-block:: python

            from dace.exoplanet import Exoplanet

            # Query the database
            exoplanet_data = Exoplanet.query_database()

            # Print the 2 first elements of each column
            for param in exoplanet_data:
                print(param, ':', exoplanet_data[param][:2])

            # Output:
            obj_id_catname : [...]
            db_info_name : [...]
            pub_info_detectiontype : [...]
            obj_phys_mass_mjup : [...]
            obj_phys_msini_mjup : [...]
            obj_phys_radius_rjup : [...]
            obj_orb_period_day : [...]
            obj_orb_a_au : [...]
            obj_orb_stardistance_pc_errmin : [...]
            obj_orb_tperi_day_errmin : [...]
            obj_stellar_magv : [...]
            obj_orb_k_mps_errmin : [...]
            obj_orb_k_mps_errmax : [...]
            obj_orb_omega_deg_errmin : [...]
            sys_nplanets : [...]
            obj_orb_ecc : [...]
            obj_parent_phys_mass_msun_errmax : [...]
            pub_info_updated : [...]
            obj_orb_a_au_errmin : [...]
            obj_orb_bigomega_deg_errmax : [...]
            obj_orb_angdist_arcsec_errmin : [...]
            obj_orb_angdist_arcsec : [...]
            obj_orb_inc_deg_errmin : [...]
            obj_orb_stardistance_pc : [...]
            obj_parent_phys_teff_k : [...]
            obj_orb_period_day_errmax : [...]
            obj_orb_inc_deg_errmax : [...]
            obj_orb_angdist_arcsec_errmax : [...]
            obj_orb_bigomega_deg_errmin : [...]
            obj_parent_phys_radius_rsun : [...]
            obj_parent_phys_mass_msun : [...]
            obj_orb_bigomega_deg : [...]
            obj_orb_period_day_errmin : [...]
            obj_parent_phys_feh : [...]
            obj_orb_a_au_errmax : [...]
            obj_parent_phys_feh_errmax : [...]
            pub_info_discovered_year : [...]
            pub_info_reference : [...]
            obj_parent_phys_teff_k_errmin : [...]
            obj_pos_alpha_deg : [...]
            obj_parent_phys_mass_msun_errmin : [...]
            obj_phys_mass_mjup_errmin : [...]
            obj_orb_tperi_day_errmax : [...]
            obj_stellar_rhk : [...]
            obj_orb_k_mps : [...]
            obj_pos_delta_deg : [...]
            obj_parent_phys_radius_rsun_errmax : [...]
            obj_phys_radius_rjup_errmin : [...]
            obj_parent_phys_radius_rsun_errmin : [...]
            obj_orb_tperi_day : [...]
            obj_orb_ecc_errmin : [...]
            obj_parent_phys_teff_k_errmax : [...]
            obj_orb_inc_deg : [...]
            obj_phys_radius_rjup_errmax : [...]
            obj_parent_phys_feh_errmin : [...]
            obj_phys_mass_mjup_errmax : [...]
            obj_orb_omega_deg : [...]
            obj_orb_angdist : [...]
            obj_phys_msini_mjup_errmin : [...]
            obj_orb_stardistance_pc_errmax : [...]
            obj_orb_ecc_errmax : [...]
            obj_phys_msini_mjup_errmax : [...]
            obj_orb_omega_deg_errmax : [...]

        """
        if filters is None:
            filters = {}
        if sort is None:
            sort = {}

        return self.dace.transform_to_format(
            self.dace.get(self.__EXOPLANET_ENDPOINT + '?limit=' + str(
                limit) + '&filters=' + self.dace.transform_dict_to_encoded_json(
                filters) + '&sort=' + self.dace.transform_dict_to_encoded_json(sort)), output_format=output_format)


Exoplanet = ExoplanetClass()
