import logging
import json
import os
from os.path import expanduser

from dace import Dace

IMAGING_DEFAULT_LIMIT = 100000


class ImagingClass:
    __ACCEPTED_FILE_TYPES = ['ns', 'snr', 'dl', 'hc', 'pa', 'master', 'all']
    __IMAGING_FILENAMES = {'NS': 'ns.fits',
                           'SNR': 'snr.fits',
                           'DL': 'dl.rdb',
                           'PA': 'PA.rdb',
                           'MASTER': 'master.fits',
                           'HC': 'hc.fits'}
    __OBS_API = 'ObsAPI/'
    __OBSERVATION_ENDPOINT = __OBS_API + 'observation/'

    def __init__(self, dace_instance=None):
        self.log = logging.getLogger("Imaging")
        self.log.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.log.addHandler(ch)

        if dace_instance is None:
            self.dace = Dace
        else:
            self.dace = dace_instance

    def query_database(self, limit=IMAGING_DEFAULT_LIMIT, filters=None, sort=None, output_format=None):
        """
        Query cheops database to retrieve available visits

        :param limit: the max number of rows to retrieve
        :param filters: A dict to apply filters on columns (see example below)
        :param sort: A dict describing the sorting results (see example below)
        :param output_format: the format you want for result data : numpy, pandas, astropy_table (default (None) dict)
        :return: A dict containing lists of values for each image

         .. code-block:: python

            from dace.imaging import Imaging

            # Query the database
            imaging_data = Imaging.query_database(limit=10, filters={'obj_id_catname': {'contains': 'HD4113'}},
            sort={'obj_id_catname': 'asc'})

            # Print the 2 first elements of each column
            for param in imaging_data:
                print(param, ':', imaging_data[param][:2])

            # Output:
            obj_id_catname : [...]
            obj_pos_ra_deg : [...]
            obj_pos_dec_deg : [...]
            ins_name : [...]
            file_rootpath : [...]
            prog_id : [...]
            obj_date_bjd : [...]
            date_night : [...]
            ins_drs_name : [...]
            img_filter : [...]
            img_mode : [...]
            public : [...]
            obj_id_daceid : [...]
        """
        if filters is None:
            filters = {}
        if sort is None:
            sort = {}

        return self.dace.transform_to_format(
            self.dace.get(self.dace._OBS_API + 'observation/search/imaging' + '?limit=' + str(
                limit) + '&filters=' + self.dace.transform_dict_to_encoded_json(
                filters) + '&sort=' + self.dace.transform_dict_to_encoded_json(sort)), output_format=output_format)

    def query_region(self, sky_coord, angle, filters=None, output_format=None):
        """
        Query a region in imaging data based on SkyCoord and Angle objects
        :param sky_coord: the SkyCoord object containing the searched region ra, dec
        :param angle: the angle object containing the searched region radius
        :param filters: optional added filters you want to search for
        :param output_format: the format you want for result data : numpy, pandas, astropy_table (default (None) dict)
        :return: a dict containing imaging data based on the geospatial search

        .. code-block:: python

            from dace.imaging import Imaging

            # Query the database with HD4113 coordinates
            imaging_data = Imaging.query_region(SkyCoord('00:43:12.59', '-37:58:57.479', unit=(u.hourangle, u.deg)),
                                                Angle('0.045d'))

            # Print the 2 first elements of each column
            for param in imaging_data:
                print(param, ':', imaging_data[param][:2])

            # Output:
            obj_id_catname : [...]
            obj_pos_ra_deg : [...]
            obj_pos_dec_deg : [...]
            ins_name : [...]
            file_rootpath : [...]
            prog_id : [...]
            obj_date_bjd : [...]
            date_night : [...]
            ins_drs_name : [...]
            img_filter : [...]
            img_mode : [...]
            public : [...]
            obj_id_daceid : [...]
        """
        coordinate_filter_dict = self.dace.transform_coordinates_to_dict(sky_coord, angle)
        filters_with_coordinates = {}
        if filters is not None:
            filters_with_coordinates.update(filters)
        filters_with_coordinates.update(coordinate_filter_dict)
        return self.query_database(filters=filters_with_coordinates, output_format=output_format)

    def download(self, file_type, filters=None, output_directory=None, output_filename=None):
        """
        Download imaging data

        :param file_type: the type of file you want to download : ns(non-saturated), snr (signal to noise ratio),
                            dl (detection limit), hc (high contrast), pa (Parallactic Angle), master, all
        :param filters: A dict filters to apply (see example below)
        :param output_full_file_path: the full path to store downloaded files
        :param output_directory: (optional) the target directory where you want to download the file
        :param output_filename: (optional) the target filename where you want to download the file

        .. code-block:: python

            from dace.imaging import Imaging

            Imaging.download('ns', filters={'file_rootpath':
                                            {'contains': '2016-05-02/NACO.2016-05-03T05:57:05.611_cadi.fits'}},
                                              output_directory='/tmp', output_filename='imaging.tar.gz')
        """
        if file_type not in self.__ACCEPTED_FILE_TYPES:
            raise ValueError('file_type must be one of these values : ' + ','.join(self.__ACCEPTED_FILE_TYPES))
        if filters is None:
            filters = {}

        imaging_data = self.query_database(filters=filters)
        files = imaging_data['file_rootpath']
        download_id = self.dace.post(self.dace._OBS_API + 'download/prepare',
                                     data=json.dumps({'fileType': file_type, 'files': files}))['values'][0]
        self.dace.persist_file_on_disk('imaging', download_id, output_directory=output_directory,
                                       output_filename=output_filename)

    def get_image(self, fits_file, file_type, output_directory=None, output_filename=None):
        """
        Download imaging data file related to fits_file and file_type arguments (all mandatory)

        Example:

            .. code-block:: python

                from dace.imaging import Imaging

                Imaging.get_image('SPHERE.2016-07-20T08:26:19.6113_eclipse.fits', 'HC',
                output_full_file_path='/tmp/high_contrast.fits')

                # OR

                # Will store it in your home directory with sane filename as stored on DACE server
                Imaging.get_image('SPHERE.2016-07-20T08:26:19.6113_eclipse.fits', 'HC')


        :param fits_file: the root fits file you want data for
        :param file_type: the type of file you want. File types availables :
            'ns': ns.fits (non saturated)
            'snr': snr.fits (signal to noise ratio)
            'dl': dl.rdb (detection limit)
            'hc': hc.fits (high contrast)
            'pa': PA.rdb (Parallactic Angle)
            'master': master.fits
            anything else : hc.fits
        :param output_directory: (optional) the target directory where you want to download the file
        :param output_filename: (optional) the target filename where you want to download the file
        """
        file_type = str(file_type).upper()
        self.dace.download_file(
            self.__OBSERVATION_ENDPOINT + 'imaging/' + '/'.join([fits_file, file_type]),
            output_directory=output_directory, output_filename=output_filename)


Imaging = ImagingClass()
