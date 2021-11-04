import logging
import json

from dace.dace import NoDataException

from dace import Dace

SPECTROSCOPY_DEFAULT_LIMIT = 10000


class SpectroscopyClass:
    ACCEPTED_FILE_TYPES = ['s1d', 's2d', 'ccf', 'bis', 'all']

    def __init__(self, dace_instance=None):
        # Logging configuration
        self.log = logging.getLogger("Spectroscopy")
        self.log.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.log.addHandler(ch)

        if dace_instance is None:
            self.dace = Dace
        else:
            self.dace = dace_instance

    def query_database(self, limit=SPECTROSCOPY_DEFAULT_LIMIT, filters=None, sort=None, output_format=None):
        """
        Query spectroscopy database to retrieve data related to filters, sort and limit

        :param limit: the max number of rows to retrieve
        :param filters: A dict to apply filters on columns (see example below)
        :param sort: A dict describing the sorting results (see example below)
        :param output_format: (optional) the format you want for result data : numpy, pandas, astropy_table (default (None) dict)
        :return: A dict containing lists of values for each visit

        .. code-block:: python

            from dace.spectroscopy import Spectroscopy

            # Query the database
            spectroscopy_data = Spectroscopy.query_database(limit=10, filters={'obj_id_catname': {'contains': 'HD'}}, sort={'obj_id_catname': 'asc'})

            # Print the 2 first elements of each column
            for param in spectroscopy_data:
                print(param, ':', spectroscopy_data[param][:2])

            # Output:
            obj_id_catname : [...]
            obj_pos_ra_hms : [...]
            obj_pos_dec_dms : [...]
            ins_name : [...]
            prog_id : [...]
            obj_date_bjd : [...]
            date_night : [...]
            ins_drs_version : [...]
            pub_bibcode : [...]
            file_rootpath : [...]
            public : [...]
            pub_ref : [...]
            ins_mode : [...]
        """
        if filters is None:
            filters = {}
        if sort is None:
            sort = {}

        return self.dace.transform_to_format(
            self.dace.get(self.dace._OBS_API + 'observation/search/spectroscopy' + '?limit=' + str(
                limit) + '&filters=' + self.dace.transform_dict_to_encoded_json(
                filters) + '&sort=' + self.dace.transform_dict_to_encoded_json(sort)), output_format=output_format)

    def query_region(self, sky_coord, angle, limit=SPECTROSCOPY_DEFAULT_LIMIT, filters=None, output_format=None):
        """
        Query a region in spectroscopy data based on SkyCoord and Angle objects
        :param sky_coord: the SkyCoord object containing the searched region ra, dec
        :param angle: the angle object containing the searched region radius
        :param filters: optional added filters you want to search for
        :param output_format: (optional) the format you want for result data : numpy, pandas, astropy_table (default (None) dict)
        :return: a dict containing spectroscopy data based on the geospatial search

        .. code-block:: python

            from dace.spectroscopy import Spectroscopy

            # Query the database with HD40307 coordinates
            spectroscopy_data = Spectroscopy.query_region(SkyCoord(88.5176, -60.023, unit='deg'), Angle('0.045d'))

            # Print the 2 first elements of each column
            for param in spectroscopy_data:
                print(param, ':', spectroscopy_data[param][:2])

            # Output:
            obj_id_catname : [...]
            obj_pos_ra_hms : [...]
            obj_pos_dec_dms : [...]
            ins_name : [...]
            prog_id : [...]
            obj_date_bjd : [...]
            date_night : [...]
            ins_drs_version : [...]
            pub_bibcode : [...]
            file_rootpath : [...]
            public : [...]
            pub_ref : [...]
            ins_mode : [...]
        """
        coordinate_filter_dict = self.dace.transform_coordinates_to_dict(sky_coord, angle)
        filters_with_coordinates = {}
        if filters is not None:
            filters_with_coordinates.update(filters)
        filters_with_coordinates.update(coordinate_filter_dict)
        return self.query_database(limit=limit, filters=filters_with_coordinates, output_format=output_format)

    def download(self, file_type, filters=None, output_directory=None, output_filename=None):
        """
        Download Spectroscopy products related to filters

        :param file_type: The type of files to download : 's1d', 's2d', 'ccf', 'bis', 'all'
        :param filters: A dict filters to apply (see example below)
        :param output_directory: (optional) the target directory where you want to download the file
        :param output_filename: (optional) the target filename where you want to download the file
        .. code-block:: python

            from dace.spectroscopy import Spectroscopy
            Spectroscopy.download('s1d',filters={'file_rootpath':{'contains':'HARPS.2010-04-04T03:38:51.386.fits'}},
                                  output_directory='/tmp', output_filename='spectroscopy_data.tar.gz')

            # OR
            from dace.spectroscopy import Spectroscopy
            Spectroscopy.download('all',filters={'date_night':{'contains':'2016-01-01'},
                                  'ins_name':{'contains':'HARPS15'}}, output_directory='/tmp', output_filename='spectroscopy_data.tar.gz')

        """
        if file_type not in self.ACCEPTED_FILE_TYPES:
            raise ValueError('file_type must be one of these values : ' + ','.join(self.ACCEPTED_FILE_TYPES))
        if filters is None:
            filters = {}

        spectroscopy_data = self.query_database(filters=filters)
        files = spectroscopy_data['file_rootpath']
        download_id = self.dace.post(self.dace._OBS_API + 'download/prepare',
                                     data=json.dumps({'fileType': file_type, 'files': files}))['values'][0]
        self.dace.persist_file_on_disk('spectro', download_id, output_directory=output_directory,
                                       output_filename=output_filename)

    def download_files(self, file_type='all', files=None, output_directory=None, output_filename=None):
        """
        Download reduction products for the list of raw files of requested file types
        at the requested output_full_file_path

        Example:

            .. code-block:: python

                from dace.spectroscopy import Spectroscopy

                Spectroscopy.download_files('all', ['HARPS.2010-04-04T03:38:51.386', 'HARPS.2009-08-03T23:51:05.543',
                'HARPS.2007-05-12T23:14:49.500'], output_directory='/tmp', output_filename='result.tar.gz')

        :param file_type: ccf/s1d/e2ds/bis/all (all by default). The types of file you need
        :param files: list of raw files you need
        :param output_directory: (optional) the target directory where you want to download the file
        :param output_filename: (optional) the target filename where you want to download the file
        """
        if files is None:
            raise NoDataException

        files = [file + '.fits' for file in files if '.fits' not in file]

        download_id = self.dace.post(self.dace._OBS_API + 'download/prepare',
                                     data=json.dumps({'fileType': file_type, 'files': files}))['values'][0]
        self.dace.persist_file_on_disk('spectro', download_id, output_directory=output_directory,
                                       output_filename=output_filename)

    def get_timeseries(self, target, sorted_by_instrument=True, output_format=None):
        """
        Get spectroscopy time series for a target in parameter and return it in a dictionary with sorting by instrument
        (True by default). In case of sorted_by_instrument=True, it will return a dictionary with
        [ins_name][drs_version][ins_mode]

        Example:

            .. code-block:: python

                from dace.spectroscopy import Spectroscopy

                spectro_time_series = Spectroscopy.get_timeseries('hd40307', sorted_by_instrument=False)


        :param target: the target you want spectroscopy time series
        :param sorted_by_instrument: by default True, sort data by [ins_name][drs_version][ins_mode]. If False,
            it will return vector of data
        :param output_format: (optional) the format you want for result data : numpy, pandas, astropy_table (default (None) dict)

        :return: a dictionary containing spectroscopy time series
        """
        sp_data = self.dace.get(self.dace._OBS_API + self.dace._SPECTRO_TIME_SERIES + target)
        if sorted_by_instrument:
            return self.dace.order_data_by_instrument(sp_data, output_format=output_format)
        else:
            return self.dace.transform_to_format(sp_data, output_format=output_format)


Spectroscopy = SpectroscopyClass()
