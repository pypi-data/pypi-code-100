import logging
import json
import os
from os.path import expanduser

from dace import Dace

CHEOPS_DEFAULT_LIMIT = 10000


class CheopsClass:
    __ACCEPTED_FILE_TYPES = ['lightcurves', 'images', 'reports', 'full', 'sub', 'all']
    __ACCEPTED_CATALOGS = ['planet', 'stellar']

    def __init__(self, dace_instance=None):
        # Logging configuration
        self.log = logging.getLogger("Cheops")
        self.log.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.log.addHandler(ch)

        if dace_instance is None:
            self.dace = Dace
        else:
            self.dace = dace_instance

    def query_database(self, limit=CHEOPS_DEFAULT_LIMIT, filters=None, sort=None, output_format=None):
        """
        Query cheops database to retrieve available visits

        :param limit: the max number of rows to retrieve
        :param filters: A dict to apply filters on columns (see example below)
        :param sort: A dict describing the sorting results (see example below)
        :param output_format: (optional) the format you want for result data : numpy, pandas, astropy_table (default (None) dict)
        :return: A dict containing lists of values for each visit

        .. code-block:: python

            from dace.cheops import Cheops

            # Query the database
            visits = Cheops.query_database(limit=10, filters={'obj_id_catname': {'contains': 'HD'}},
            sort={'obj_id_catname': 'asc'})

            # Print the 2 first elements of each column
            for param in visits:
                print(param, ':', visits[param][:2])

            # Output:
            file_key: [...]
            file_rootpath: [...]
            file_ext: [...]
            ins_name: [...]
            date_mjd_start: [...]
            date_mjd_end: [...]
            data_pipe_version [...]
            data_proc_num: [...]
            data_arch_rev: [...]
            prog_id: [...]
            prog_type: [...]
            req_id: [...]
            pi_uid: [...]
            pi_name: [...]
            status_published: [...]
            photom_ap_type: [...]
            photom_lc_dataname: [...]
            photom_ap_radius: [...]
            obj_mag_v_err: [...]
            obj_mag_cheops: [...]
            obj_sptype: [...]
            obj_id_catname: [...]
            obj_mag_v: [...]
            obj_pos_dec_deg: [...]
            obj_mag_cheops_err: [...]
            obj_pos_ra_deg: [...]
            obs_nexp: [...]
            obs_id: [...]
            obs_exptime: [...]
            obs_total_exptime: [...]

        """
        if filters is None:
            filters = {}
        if sort is None:
            sort = {}

        return self.dace.transform_to_format(
            self.dace.get(self.dace._OBS_API + 'cheops' + '/search' + '?limit=' + str(
                limit) + '&filters=' + self.dace.transform_dict_to_encoded_json(
                filters) + '&sort=' + self.dace.transform_dict_to_encoded_json(sort)), output_format=output_format)

    def query_catalog(self, catalog, limit=CHEOPS_DEFAULT_LIMIT, filters=None, sort=None, output_format=None):
        """
        Query cheops catalogs

        :param catalog: the catalog you are looking for. Can be 'planet' or 'stellar'
        :param limit: the max number of rows to retrieve
        :param filters: A dict to apply filters on columns (see example below)
        :param sort: A dict describing the sorting results (see example below)
        :param output_format: (optional) the format you want for result data : numpy, pandas, astropy_table (default (None) dict)
        :return: A dict containing lists of values for each visit

        .. code-block:: python

            from dace.cheops import Cheops
            catalog = Cheops.query_catalog('planet')
            for param in catalog:
                  print(param, ':', catalog[param][:2])

            obj_id_planet_catname : [...]
            obj_id_catname : [...]
            obj_id_gaiadr2 : [...]
            db_info_remarks : [...]
            db_info_reference : [...]
            obj_rv_k_mps : [...]
            obj_trans_depth_ppm : [...]
            obj_trans_duration_days : [...]
            obj_trans_ecosw : [...]
            obj_trans_esinw : [...]
            obj_trans_period_days : [...]
            obj_trans_t0_bjd : [..]

        """
        if catalog not in self.__ACCEPTED_CATALOGS:
            raise ValueError('catalog must be one of these values : ' + ','.join(self.__ACCEPTED_CATALOGS))

        if filters is None:
            filters = {}
        if sort is None:
            sort = {}

        return self.dace.transform_to_format(
            self.dace.get(self.dace._OBS_API + 'cheops/catalog/' + catalog + '?limit=' + str(
                limit) + '&filters=' + self.dace.transform_dict_to_encoded_json(
                filters) + '&sort=' + self.dace.transform_dict_to_encoded_json(sort)), output_format=output_format)

    def query_region(self, sky_coord, angle, limit=CHEOPS_DEFAULT_LIMIT, filters=None, output_format=None):
        """
        Query a region in cheops database based on SkyCoord and Angle objects

        :param sky_coord: the SkyCoord object containing the searched region ra, dec
        :param angle: the angle object containing the searched region radius
        :param filters: optional added filters you want to search for
        :param output_format: (optional) the format you want for result data : numpy, pandas, astropy_table (default (None) dict)
        :return: a dict containing cheops data based on the geospatial search

        .. code-block:: python

            from dace.cheops import Cheops
            from astropy.coordinates import SkyCoord, Angle
            import astropy.units as u
            cheops_data = Cheops.query_region(SkyCoord('10:00:00.0000', '-01:01:01.000', unit=(u.hourangle, u.deg)), Angle('0.045d'))
            for param in cheops_data:
                print(param, ':', cheops_data[param][:2])

            obj_id_catname : [...]
            obj_pos_coordinates_hms_dms : [...]
            date_mjd_start : [...]
            date_mjd_end : [...]
            obj_mag_v : [...]
            pi_name : [...]
            prog_id : [...]
            req_id : [...]
            status_published : [...]
            obs_exptime : [...]
            photom_ap_radius : [...]
            obs_id : [...]
            file_ext : [...]
            data_pipe_version : [...]
            obj_mag_v_err : [...]
            file_key : [...]
            photom_ap_type : [...]
            data_arch_rev : [...]
            pi_uid : [...]
            ins_name : [...]
            prog_type : [...]
            obj_mag_cheops : [...]
            obj_mag_cheops_err : [...]
            obj_sptype : [...]
            obs_nexp : [...]
            photom_lc_dataname : [...]
            obs_total_exptime : [...]
            data_proc_num : [...]
            db_lc_available : [...]
            file_rootpath : [...]
        """
        coordinate_filter_dict = self.dace.transform_coordinates_to_dict(sky_coord, angle)
        filters_with_coordinates = {}
        if filters is not None:
            filters_with_coordinates.update(filters)
        filters_with_coordinates.update(coordinate_filter_dict)
        return self.query_database(limit=limit, filters=filters_with_coordinates, output_format=output_format)

    def get_lightcurve(self, target, aperture='default', filters=None, sort=None, output_format=None):
        """
        Get photometry data from Cheops

        :param target: The target name to retrieve photometry
        :param aperture: Aperture type : 'default', 'optimal, 'rinf', 'rsup'
        :param filters: A dict to apply filters on columns
        :param sort: A dict describing the sorting results
        :param output_format: (optional) the format you want for result data : numpy, pandas, astropy_table (default (None) dict)
        :return: a dict containing photometry timeseries vectors

        .. code-block:: python

            from dace.cheops import Cheops

            # Query the database
            data = Cheops.get_lightcurve('HD72769', 'default')

            # Print the 2 first elements of each column
            for param in data:
                print(param, ':', data[param][:2])

            # Output:
            file_key: [...]
            obj_date_bjd_vect : [...]
            photom_flux_vect : [...]
            photom_flux_vect_err : [...]
            photom_centroid_x_vect: [...]
            photom_centroid_y_vect : [...]

        """
        if filters is None:
            filters = {}
        if sort is None:
            sort = {}
        return self.dace.transform_to_format(
            self.dace.get(
                self.dace._OBS_API + 'cheops' + '/photometry/' + target + '?aperture=' + aperture + '&filters=' +
                self.dace.transform_dict_to_encoded_json(filters) + '&sort=' + self.dace.transform_dict_to_encoded_json(
                    sort)), output_format=output_format)

    def download(self, file_type, filters=None, output_directory=None, output_filename=None):
        """
        Download CHEOPS products (FITS, PDF,...) for specific visits

        :param file_type: The type of files to download : 'lightcurves', 'images', 'reports', 'full', 'sub', 'all'
        :param filters: A dict filters to apply (see example below)
        :param output_directory: (optional) the target directory where you want to download the file
        :param output_filename: (optional) the target filename where you want to download the file

        .. code-block:: python

            from dace.cheops import Cheops

            Cheops.download('all', {'file_key': {'contains': 'CH_PR300001_TG000301_V0000'}},
            output_directory='/tmp', output_filename='cheops.tar.gz')

        """
        if file_type not in self.__ACCEPTED_FILE_TYPES:
            raise ValueError('file_type must be one of these values : ' + ','.join(self.__ACCEPTED_FILE_TYPES))
        if filters is None:
            filters = {}

        cheops_data = self.query_database(filters=filters)
        files = cheops_data['file_rootpath']
        download_id = self.dace.post(self.dace._OBS_API + 'download/prepare',
                                     data=json.dumps({'fileType': file_type, 'files': files}))['values'][0]
        self.dace.persist_file_on_disk('cheops', download_id, output_directory=output_directory,
                                       output_filename=output_filename)

    def download_diagnostic_movie(self, file_key, aperture='default', output_directory=None, output_filename=None):
        """
        Download diagnostic movie for a Cheops file_key

        :param file_key: Cheops visit file_key
        :param aperture: the type of aperture you want : 'default', 'optimal, 'rinf', 'rsup'
        :param output_directory: (optional) the target directory where you want to download the file
        :param output_filename: (optional) the target filename where you want to download the file

        :return: nothing but persist the movie file in output_full_file_path location or in user home if not specified
        """
        self.dace.download_file(
            self.dace._OBS_API + 'cheops/diagnosticMovie/' + file_key + '?aperture=' + aperture,
            output_directory=output_directory, output_filename=output_filename)


Cheops = CheopsClass()
