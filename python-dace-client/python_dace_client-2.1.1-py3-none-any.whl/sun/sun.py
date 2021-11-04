import logging
import json
import os
from os.path import expanduser

from dace.dace import NoDataException

from dace import Dace
from dace.spectroscopy import Spectroscopy

SUN_DEFAULT_LIMIT = 200000


class SunClass:

    def __init__(self, dace_instance=None):
        # Logging configuration
        self.log = logging.getLogger("Sun")
        self.log.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.log.addHandler(ch)

        if dace_instance is None:
            self.dace = Dace
        else:
            self.dace = dace_instance

    def query_database(self, limit=SUN_DEFAULT_LIMIT, filters=None, sort=None, output_format=None):
        """
        Query Sun database

        :param limit: the max number of rows to retrieve
        :param filters: A dict to apply filters on columns (see example below)
        :param sort: A dict describing the sorting results (see example below)
        :param output_format: (optional) the format you want for result data : numpy, pandas, astropy_table (default (None) dict)
        :return: A dict containing lists of values related to filters, limit and sort

        .. code-block:: python

            from dace.sun import Sun

            # Query the database
            sun_data = Sun.query_database(limit=10)
        """
        if filters is None:
            filters = {}
        if sort is None:
            sort = {}

        return self.dace.transform_to_format(
            self.dace.get(self.dace._OBS_API + 'sun' + '/search' + '?limit=' + str(
                limit) + '&filters=' + self.dace.transform_dict_to_encoded_json(
                filters) + '&sort=' + self.dace.transform_dict_to_encoded_json(sort)), output_format=output_format)

    def get_timeseries(self, output_format=None):
        """
        Get all sun timeseries

        :param output_format: (optional) the format you want for result data : numpy, pandas, astropy_table (default (None) dict)
        :return: A dict containing sun timeseries

        .. code-block:: python

            from dace.sun import Sun

            # Query the database
            sun_data = Sun.get_timeseries()
        """
        return self.dace.transform_to_format(self.dace.get(self.dace._OBS_API + 'sun/radialVelocities'),
                                             output_format=output_format)

    def download(self, file_type, filters=None, output_directory=None, output_filename=None):
        """
        Download Sun Spectroscopy products related to filters

        :param file_type: The type of files to download : 's1d', 's2d', 'ccf', 'bis', 'all'
        :param filters: A dict filters to apply (see example below)
        :param output_directory: (optional) the target directory where you want to download the file
        :param output_filename: (optional) the target filename where you want to download the file

        .. code-block:: python

            from dace.sun import Sun
            Sun.download('s1d',filters={'file_rootpath':{'contains':'r.HARPN.2016-01-03T15:36:20.496.fits'}},
                                  output_directory='/tmp', output_filename='sun_spectroscopy_data.tar.gz')
        """
        if file_type not in Spectroscopy.ACCEPTED_FILE_TYPES:
            raise ValueError('file_type must be one of these values : ' + ','.join(Spectroscopy.ACCEPTED_FILE_TYPES))
        if filters is None:
            filters = {}

        sun_spectroscopy_data = self.query_database(filters=filters)
        files = sun_spectroscopy_data['file_rootpath']
        download_id = self.dace.post(self.dace._OBS_API + 'download/prepare',
                                     data=json.dumps({'fileType': file_type, 'files': files}))['values'][0]
        self.dace.persist_file_on_disk('sun', download_id, output_directory=output_directory,
                                       output_filename=output_filename)

    def download_files(self, file_type='s1d', files=None, output_directory=None, output_filename=None):
        """
        Download reduction products for the list of raw files of requested file types
        at the requested output_full_file_path

        Example:

            .. code-block:: python

                from dace.sun import Sun

                Sun..download_files(file_type='s1d', files=['r.HARPN.2016-01-03T15:36:20.496',
                                                            'r.HARPN.2016-01-03T13:26:05.796'],
                                                output_directory='/tmp', output_filename='sun_spectroscopy_data.tar.gz')

        :param file_type: ccf/s1d/e2ds (s1d by default). The types of file you need
        :param files: list of raw files you need
        :param output_directory: (optional) the target directory where you want to download the file
        :param output_filename: (optional) the target filename where you want to download the file
        """
        if files is None:
            raise NoDataException

        files = [file + '.fits' for file in files if '.fits' not in file]

        download_id = self.dace.post(self.dace._OBS_API + 'download/prepare',
                                     data=json.dumps({'fileType': file_type, 'files': files}))['values'][0]
        self.dace.persist_file_on_disk('sun', download_id, output_directory=output_directory,
                                       output_filename=output_filename)

    def download_public_release_all(self, year, month, output_directory=None, output_filename=None):
        """
        Download public sun data of year and month gave in parameter

        Example:

            .. code-block:: python

                from dace.sun import Sun
                Sun.download_public_release_all('2015','12', output_directory='/tmp', output_filename='release_all_2015-12.tar.gz')


        :param year: the year you want sun data for
        :param month: the month you want sun data for
        :param output_directory: (optional) the target directory where you want to download the file
        :param output_filename: (optional) the target filename where you want to download the file
        """
        year_and_month = str(year) + '-' + str(month)

        self.dace.download_file(self.dace._OBS_API + 'sun/download/release/all/' + year_and_month,
                                output_directory=output_directory, output_filename=output_filename)

    def download_public_release_ccf(self, year, output_directory=None, output_filename=None):
        """
        Download public release ccf data of year specified as parameter

        Example:

            .. code-block:: python

                from dace.sun import Sun
                Sun.download_public_release_ccf('2015', output_directory='/tmp', output_filename='cff.tar.gz')

        :param year: the year you want data for
        :param output_directory: (optional) the target directory where you want to download the file
        :param output_filename: (optional) the target filename where you want to download the file
        """

        self.dace.download_file(self.dace._OBS_API + 'sun/download/release/ccf/' + year,
                                output_directory=output_directory, output_filename=output_filename)

    def download_public_release_timeseries(self, period='2015-2018', output_directory=None, output_filename=None):
        """
        Download public release timeseries data on a defined period : '2015-2018' by default

        Example:

            .. code-block:: python

                from dace.sun import Sun

                Sun.download_public_timeseries(output_directory='/tmp' , output_filename='public_release_timeseries.rdb')

        :param period: the period you want data for. Today there is only '2015-2018'
        :param output_directory: (optional) the target directory where you want to download the file
        :param output_filename: (optional) the target filename where you want to download the file
        """
        self.dace.download_file(self.dace._OBS_API + 'sun/download/release/timeseries/' + period,
                                output_directory=output_directory, output_filename=output_filename)


Sun = SunClass()
