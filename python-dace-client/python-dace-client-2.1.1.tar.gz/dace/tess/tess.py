import logging
import json
import os
from os.path import expanduser

from dace import Dace

TESS_DEFAULT_LIMIT = 10000


class TessClass:

    def __init__(self, dace_instance=None):
        # Logging configuration
        self.log = logging.getLogger("Tess")
        self.log.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.log.addHandler(ch)

        if dace_instance is None:
            self.dace = Dace
        else:
            self.dace = dace_instance

    def query_database(self, limit=TESS_DEFAULT_LIMIT, filters=None, sort=None, output_format=None):
        """
        Query tess database to retrieve available existing sectors

        :param limit: the max number of rows to retrieve
        :param filters: A dict to apply filters on columns (see example below)
        :param sort: A dict describing the sorting results (see example below)
        :param output_format: (optional) the format you want for result data : numpy, pandas, astropy_table (default (None) dict)
        :return: A dict containing lists of values for each visit

        .. code-block:: python

            from dace.tess import Tess

            # Query the database
            sectors = Tess.query_database(limit=10, filters={'obj_id_catname': {'contains': 'TIC'}},
            sort={'obj_id_catname': 'asc'})

            # Print the 2 first elements of each column
            for param in sectors:
                print(param, ':', sectors[param][:2])

            # Output:
            obj_id_catname: [...]
            ins_drs_version: [...]
            sector: [...]
            obj_pos_coordinates_hms_dms: [...]
            file_rootpath: [...]
            obj_mag_tess: [...]
            obj_phys_mass_msun: [...]
            obj_phys_mh: [...]
            obj_phys_radius: [...]
            obj_phys_temp_k: [...]
            obj_phys_logg: [...]
            ins_name: [...]
            prog_id: [...]

        """
        if filters is None:
            filters = {}
        if sort is None:
            sort = {}

        return self.dace.transform_to_format(
            self.dace.get(self.dace._OBS_API + 'tess' + '/search' + '?limit=' + str(
                limit) + '&filters=' + self.dace.transform_dict_to_encoded_json(
                filters) + '&sort=' + self.dace.transform_dict_to_encoded_json(sort)), output_format=output_format)

    def query_region(self, sky_coord, angle, limit=TESS_DEFAULT_LIMIT, filters=None, output_format=None):
        """
        Query a region in tess database based on SkyCoord and Angle objects

        :param sky_coord: the SkyCoord object containing the searched region ra, dec
        :param angle: the angle object containing the searched region radius
        :param filters: optional added filters you want to search for
        :param output_format: (optional) the format you want for result data : numpy, pandas, astropy_table (default (None) dict)
        :return: a dict containing tess data based on the geospatial search

        .. code-block:: python

            from dace.tess import Tess
            from astropy.coordinates import SkyCoord, Angle
            import astropy.units as u
            tess_data = Tess.query_region(SkyCoord('10:00:00.0000', '-01:01:01.000', unit=(u.hourangle, u.deg)), Angle('0.045d'))
            for param in tess_data:
                print(param, ':', tess_data[param][:2])

            obj_id_catname: [...]
            ins_drs_version: [...]
            sector: [...]
            obj_pos_coordinates_hms_dms: [...]
            file_rootpath: [...]
            obj_mag_tess: [...]
            obj_phys_mass_msun: [...]
            obj_phys_mh: [...]
            obj_phys_radius: [...]
            obj_phys_temp_k: [...]
            obj_phys_logg: [...]
            ins_name: [...]
            prog_id: [...]
        """
        coordinate_filter_dict = self.dace.transform_coordinates_to_dict(sky_coord, angle)
        filters_with_coordinates = {}
        if filters is not None:
            filters_with_coordinates.update(filters)
        filters_with_coordinates.update(coordinate_filter_dict)
        return self.query_database(limit=limit, filters=filters_with_coordinates, output_format=output_format)

    def get_lightcurve(self, target, filters=None, sort=None, output_format=None):
        """
        Get photometry data from Tess

        :param target: The target name to retrieve photometry
        :param filters: A dict to apply filters on columns
        :param sort: A dict describing the sorting results
        :param output_format: (optional) the format you want for result data : numpy, pandas, astropy_table (default (None) dict)
        :return: a dict containing photometry timeseries vectors

        .. code-block:: python

            from dace.tess import Tess

            # Query the database
            data = Tess.get_lightcurve('TIC421937540')

            # Print the 2 first elements of each column
            for param in data:
                print(param, ':', data[param][:2])

            # Output:
            dataset_id: [...]
            quality: [...]
            corr_flux: [...]
            corr_flux_err: [...]
            raw_flux: [...]
            raw_flux_err: [...]
            time: [...]

        """
        if filters is None:
            filters = {}
        if sort is None:
            sort = {}
        return self.dace.transform_to_format(
            self.dace.get(
                self.dace._OBS_API + 'tess' + '/photometry/' + target + '?filters=' +
                self.dace.transform_dict_to_encoded_json(filters) + '&sort=' + self.dace.transform_dict_to_encoded_json(
                    sort)), output_format=output_format)

Tess = TessClass()
