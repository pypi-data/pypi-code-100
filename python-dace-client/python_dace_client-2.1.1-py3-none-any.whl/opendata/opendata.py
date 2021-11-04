import logging
import json
import os
from os.path import expanduser

from dace import Dace

OPENDATA_DEFAULT_LIMIT = 10000


class OpenDataClass:

    def __init__(self, dace_instance=None):
        self.__OPEN_DATA_API = 'OpenDataAPI/'
        self.__OPENDATA_AVAILABLE_FILE_TYPES = ['readme', 'archive']
        self.__ADS_URL = 'https://ui.adsabs.harvard.edu/abs/'
        self.__DOI_URL = 'https://doi.org/'

        # Logging configuration
        self.log = logging.getLogger("OpenData")
        self.log.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.log.addHandler(ch)

        if dace_instance is None:
            self.dace = Dace
        else:
            self.dace = dace_instance

    def query_database(self, limit=OPENDATA_DEFAULT_LIMIT, filters=None, sort=None, output_format=None):
        """
        Query opendata database to retrieve available publications

        :param limit: the max number of rows to retrieve
        :param filters: A dict to apply filters on columns (see example below)
        :param sort: A dict describing the sorting results (see example below)
        :param output_format: (optional) the format you want for result data : numpy, pandas, astropy_table (default (None) dict)
        :return: A dict containing lists of publications based on parameters

        .. code-block:: python

            from dace.opendata import OpenData

            # Query the database
            publications = OpenData.query_database(limit=10)

            # Print the 2 first elements of each column
            for param in publications:
                print(param, ':', publications[param][:2])

            # Output:
            ...

        """
        if filters is None:
            filters = {}
        if sort is None:
            sort = {}

        data = self.dace.parse_parameters(
            self.dace.get(self.__OPEN_DATA_API + 'publication/search' + '?limit=' + str(
                limit) + '&filters=' + self.dace.transform_dict_to_encoded_json(
                filters) + '&sort=' + self.dace.transform_dict_to_encoded_json(sort)))

        data['ads_link'] = [self.__ADS_URL + bibcode for bibcode in data['pub_bibcode']]
        data['doi_link'] = [self.__DOI_URL + doi for doi in data['pub_doi']]
        data['data_external_repositories'] = [json.loads(data_external_repositories) for data_external_repositories in
                                              data['data_external_repositories']]
        pub_majors = []
        for pub_major in data['pub_major']:
            current_row = []
            for bool_value in pub_major.split(','):
                current_row.append(bool_value in ['true', 'True'])
            pub_majors.append(current_row)
        data['pub_major'] = pub_majors

        return self.dace.convert_to_format(data, output_format=output_format)

    def download(self, bibcode, file_type, output_directory=None, output_filename=None):
        """
        Download publications of a bibcode

        :param bibcode: bibcode you want get publications data
        :param file_type: the file_type you want to download : readme or archive
        :param output_directory: (optional) the target directory where you want to download the file
        :param output_filename: (optional) the target filename where you want to download the file

        .. code-block:: python

            from dace.opendata import OpenData

            OpenData.download('2019MNRAS.483.5534S', 'archive', output_directory='/tmp', output_filename='opendata.tar.gz')
        """
        if file_type not in self.__OPENDATA_AVAILABLE_FILE_TYPES:
            raise ValueError('file_type must be : ' + ','.join(self.__OPENDATA_AVAILABLE_FILE_TYPES))

        self.dace.download_file(self.__OPEN_DATA_API + 'publication/' + file_type + '/' + bibcode,
                                output_directory=output_directory, output_filename=output_filename)


OpenData = OpenDataClass()
