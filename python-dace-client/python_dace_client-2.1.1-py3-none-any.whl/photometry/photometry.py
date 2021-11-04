import logging

from dace import Dace

PHOTOMETRY_DEFAULT_LIMIT = 10000


class PhotometryClass:
    __ACCEPTED_FILE_TYPES = ['s1d', 's2d', 'ccf', 'bis', 'all']
    __OBS_API = 'ObsAPI/'
    __OBSERVATION_ENDPOINT = __OBS_API + 'observation/'
    __PHOTOMETRY_ENDPOINT = __OBSERVATION_ENDPOINT + 'photometry/'

    def __init__(self, dace_instance=None):
        # Logging configuration
        self.log = logging.getLogger("Photometry")
        self.log.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.log.addHandler(ch)

        if dace_instance is None:
            self.dace = Dace
        else:
            self.dace = dace_instance

    def query_database(self, limit=PHOTOMETRY_DEFAULT_LIMIT, filters=None, sort=None, output_format=None):
        """
        Query photometry database to retrieve data related to filters, sort and limit

        :param limit: the max number of rows to retrieve
        :param filters: A dict to apply filters on columns (see example below)
        :param sort: A dict describing the sorting results (see example below)
        :param output_format: the format you want for result data : numpy, pandas, astropy_table (default (None) dict)
        :return: A dict containing lists of values for each visit

        .. code-block:: python

            from dace.photometry import Photometry

            # Query the database
            photometry_data = Photometry.query_database(limit=10, filters={'obj_id_catname': {'contains': 'EPIC246985284'}}, sort={'obj_id_catname': 'asc'})

            # Print the 2 first elements of each column
            for param in photometry_data:
                print(param, ':', photometry_data[param][:2])

            # Output:
            obj_id_catname : [...]
            ins_name : [...]
            file_rootpath : [...]
            prog_id : [...]
            obj_date_bjd : [...]
            pub_ref : [...]
            status_published : [...]
            obj_id_daceid : [...]
            pub_bibcode : [...]
        """
        if filters is None:
            filters = {}
        if sort is None:
            sort = {}

        return self.dace.transform_to_format(
            self.dace.get(self.dace._OBS_API + 'observation/search/photometry' + '?limit=' + str(
                limit) + '&filters=' + self.dace.transform_dict_to_encoded_json(
                filters) + '&sort=' + self.dace.transform_dict_to_encoded_json(sort)), output_format=output_format)

    def query_region(self, sky_coord, angle, limit=PHOTOMETRY_DEFAULT_LIMIT, filters=None, output_format=None):
        """
        Query a region in photometry data based on SkyCoord and Angle objects
        :param sky_coord: the SkyCoord object containing the searched region ra, dec
        :param angle: the angle object containing the searched region radius
        :param filters: optional added filters you want to search for
        :param output_format: the format you want for result data : numpy, pandas, astropy_table (default (None) dict)
        :return: a dict containing photometry data based on the geospatial search

        .. code-block:: python

            from dace.photometry import Photometry

            # Query the database with TIC350821761 coordinates
            photometry_data = Photometry.query_region(SkyCoord(89.52458333333333, -57.31019444444445, unit='deg'))

            # Print the 2 first elements of each column
            for param in photometry_data:
                print(param, ':', photometry_data[param][:2])

            # Output:
            obj_id_catname : [...]
            ins_name : [...]
            file_rootpath : [...]
            prog_id : [...]
            obj_date_bjd : [...]
            pub_ref : [...]
            status_published : [...]
            obj_id_daceid : [...]
            pub_bibcode : [...]
        """
        coordinate_filter_dict = self.dace.transform_coordinates_to_dict(sky_coord, angle)
        filters_with_coordinates = {}
        if filters is not None:
            filters_with_coordinates.update(filters)
        filters_with_coordinates.update(coordinate_filter_dict)
        return self.query_database(limit=limit, filters=filters_with_coordinates, output_format=output_format)

    def get_timeseries(self, target):
        """
        Get photometry timeseries for target and return it as a list of dict with different instruments

        Example:

            .. code-block:: python

                from dace.photometry import Photometry

                photom_timeseries = Photometry.get_timeseries('WASP-47')

        :param target: the target you want photometry timeseries

        :return: photometry timeseries vectors
        """
        return self.dace.get(self.__PHOTOMETRY_ENDPOINT + target)['observations']


Photometry = PhotometryClass()
