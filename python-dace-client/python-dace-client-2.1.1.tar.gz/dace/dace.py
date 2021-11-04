import json
import logging
import re

import requests
import configparser
import os
import urllib.parse

from astropy.table import Table
from requests import RequestException, HTTPError
from collections import defaultdict
from os.path import expanduser, dirname, join, isfile
import numpy as np
import pandas as pa

from .__version__ import __version__, __title__

COORDINATES_DB_COLUMN = 'obj_pos_coordinates_hms_dms'

MB_SIZE = 1048576

EXOPLANET_DATABASE_MAX_LIMIT = 50000
MISSION_DATABASE_MAX_LIMIT = 10000
ATMOSPHERIC_MAX_LIMIT = 10000


class NoDataException(Exception):
    """Raised when no data are provided"""


class DaceClass:
    _OBS_API = 'ObsAPI/'
    __OBSERVATION_ENDPOINT = _OBS_API + 'observation/'
    _SPECTRO_TIME_SERIES = 'observation/radialVelocities/'
    __CORE_API = 'CoreAPI/'
    __MAX_ATTEMPTS = 10
    __DEFAULT_VALUE_WHEN_EMPTY = 'default'
    __PIPELINE_ENDPOINT = 'ObsAPI/pipeline/'
    __PHOTOMETRY_ENDPOINT = __OBSERVATION_ENDPOINT + 'photometry/'
    __EXOPLANET_ENDPOINT = 'ExoplanetAPI/exoplanetDatabase'
    __STELLAR_KEYS = {'ra': 'objPosRaHms',
                      'dec': 'objPosDecDms',
                      'parallax': 'objPosPlxMas',
                      'pmra': 'objPosPmraMaspyr',
                      'pmdec': 'objPosPmdecMaspyr',
                      'radvel': 'objRadialVelocity',
                      'mag_b': 'objFluxMagB',
                      'mag_v': 'objFluxMagV',
                      'sptype': 'objSptype'}
    __IMAGING_FILENAMES = {'NS': 'ns.fits',
                           'SNR': 'snr.fits',
                           'DL': 'dl.rdb',
                           'HC': 'hc.fits'}
    __dace_rc_config = None

    def __init__(self, dace_rc_config_path=None, config_path=None):
        # Logging configuration
        self.log = logging.getLogger("Dace")
        self.log.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.log.addHandler(ch)

        # Default dacerc file is in user home
        if dace_rc_config_path is None:
            dace_rc_config_path = expanduser('~') + os.sep + '.dacerc'

        if isfile(dace_rc_config_path):
            self.__dace_rc_config = configparser.ConfigParser()
            self.__dace_rc_config.read(dace_rc_config_path)
        else:
            self.log.warning(
                "No .dacerc file found. You are requesting data in public mode. If you need to be connected, " +
                "please create a .dacerc file in your home directory containing your api key. See README for details.")

        self.__cfg = configparser.ConfigParser()
        if config_path is None:
            self.__cfg.read(join(dirname(__file__)) + os.sep + 'config.ini')
        else:
            self.__cfg.read(config_path)

    @staticmethod
    def transform_dict_to_encoded_json(dict_to_transform):
        return urllib.parse.quote_plus(json.dumps(dict_to_transform))

    @staticmethod
    def transform_coordinates_to_dict(sky_coord, angle):
        return {COORDINATES_DB_COLUMN: {'ra': sky_coord.ra.degree, 'dec': sky_coord.dec.degree,
                                        'radius': angle.degree}}

    def transform_to_format(self, json_data, output_format=None):
        data = self.parse_parameters(json_data)
        return self.convert_to_format(data, output_format)

    def parse_parameters(self, json_data):
        """
        Internally DACE data are provided using protobuff. The format is a list of parameters. Here we parse
        these data to give to the user something more readable and ignore the internal stuff
        """
        data = defaultdict(list)
        if 'parameters' not in json_data:
            return data
        parameters = json_data.get('parameters')
        for parameter in parameters:
            variable_name = parameter.get('variableName')
            double_values = parameter.get('doubleValues')
            float_values = parameter.get('floatValues')
            int_values = parameter.get('intValues')
            string_values = parameter.get('stringValues')
            bool_values = parameter.get('boolValues')
            occurrences = parameter.get('occurrences')

            # Only one type of values can be present. So we look for the next occurence not None. Prevent not found
            # with an empty list to avoid having StopIteration exception
            values = next((values_list for values_list in [double_values, float_values, int_values, string_values, bool_values] if
                           values_list is not None), [])
            if occurrences:
                data[variable_name].extend(self.__transform_values_with_occurrences(values, occurrences))
            else:
                data[variable_name].extend(values)

            error_values = parameter.get('minErrorValues')  # min or max is symmetric
            if error_values is not None:
                if occurrences:
                    data[variable_name + '_err'].extend(
                        self.__transform_values_with_occurrences(error_values, occurrences))
                else:
                    data[variable_name + '_err'].extend(error_values)
        return data

    def convert_to_format(self, data, output_format):
        if output_format == 'numpy':
            numpy_data = {}
            for key, values in data.items():
                numpy_data[key] = np.array(values)
            return numpy_data
        elif output_format == 'pandas':
            return pa.DataFrame.from_dict(data)
        elif output_format == 'astropy_table':
            return Table(data)
        else:
            return data

    def persist_file_on_disk(self, obs_type, download_id, output_directory=None, output_filename=None):
        self.download_file(self._OBS_API + 'download/' + obs_type + '/' + download_id,
                           output_directory=output_directory, output_filename=output_filename)

    def order_data_by_instrument(self, json_data, output_format=None):
        data_dict = self.transform_to_format(json_data)
        ins_names = data_dict.pop('ins_name')
        ins_modes = data_dict.pop('ins_mode')
        drs_versions = data_dict.pop('drs_version')
        bib_codes = data_dict.pop('pub_bibcode')

        data_by_instrument = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))

        for i, instrument in enumerate(ins_names):
            for parameter in data_dict.keys():
                drs_version_or_bibcode = bib_codes[i] if bib_codes[i] else drs_versions[i] if drs_versions[
                    i] else self.__DEFAULT_VALUE_WHEN_EMPTY
                ins_mode = ins_modes[i] if ins_modes[i] else self.__DEFAULT_VALUE_WHEN_EMPTY
                data_by_instrument[instrument][drs_version_or_bibcode][ins_mode][parameter].append(
                    data_dict[parameter][i])

        if output_format == 'numpy':
            return self.__convert_to_numpy_data_by_instrument(data_by_instrument)
        else:
            return data_by_instrument

    def get(self, endpoint, raw_response=False):
        """
        This method does an HTTP get to DACE backend. If an apiKey has been found, it will be added in HTTP header
        :param endpoint: the DACE endpoint you want to query
        :return: the Json response containing data
        """
        headers = self.__prepare_request(raw_response)
        host = self.__cfg['api']['host'] + endpoint
        try:
            response = requests.get(host, headers=headers)
            response.raise_for_status()
            if response.ok:
                if raw_response:
                    return response.content
                else:
                    return response.json()
            else:
                self.log.error("Status code %s when calling %s", response.status_code, host)
                raise RequestException
        except HTTPError as errh:
            return self.__manage_http_errors(errh)
        except RequestException as e:
            raise RequestException('Problem when calling {}'.format(host)) from e

    def post(self, endpoint, data):
        headers = self.__prepare_request()
        host = self.__cfg['api']['host'] + endpoint
        try:
            response = requests.post(host, data=data, headers=headers)
            response.raise_for_status()
            if response.ok:
                return response.json()
            else:
                self.log.error("Status code %s when calling %s", response.status_code, host)
                raise RequestException
        except HTTPError as errh:
            return self.__manage_http_errors(errh)
        except RequestException as e:
            raise RequestException('Problem when calling {}'.format(host)) from e

    def download_file(self, url, output_directory=None, output_filename=None):
        try:
            if output_directory is None:
                output_directory = expanduser('~')
            with requests.get(self.__cfg['api']['host'] + url, headers=self.__prepare_request(True),
                              stream=True) as response:
                response.raise_for_status()
                if output_filename is None:
                    output_filename = re.sub("attachment;\\s*filename\\s*=\\s*", '',
                                             response.headers['content-disposition']).replace('"', '')
                    if output_filename is None:
                        raise ValueError('Missing content-disposition. Please contact DACE support')
                output_full_file_path = output_directory + os.sep + output_filename
                self.log.info("Downloading file on location : %s", output_full_file_path)
                self.write_stream(output_full_file_path, response)
                self.log.info('File downloaded on location : %s', output_full_file_path)
        except HTTPError as errh:
            if errh.response.status_code == 404:
                self.log.error('The file is not found on DACE')
            else:
                self.__manage_http_errors(errh)

    def write_stream(self, output_filename, response):
        with open(output_filename, 'wb') as f:
            chunck_total_size = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    chunck_total_size += 8192
                    if chunck_total_size % MB_SIZE == 0:
                        print("\r Download : " + str(chunck_total_size // MB_SIZE) + " MB", end="")
        print("\nDownload done")

    def __manage_http_errors(self, errh):
        status_code = errh.response.status_code
        if status_code == 404:
            return {}
        elif status_code == 401:
            self.log.error('Not authorized. You need to be logged on to access these data')
        elif status_code == 403:
            self.log.error('Forbidden. You do not have the permission to access these data')
        elif status_code == 405:
            self.log.error('Not Allowed. This method is deprecated. Please refer to documentation')
        else:
            self.log.error('Http error : ' + str(errh))
            self.log.error('Please contact DACE support')
        return {}

    def __prepare_request(self, raw_response=False):
        headers = {'Accept': 'application/octet-stream'} if raw_response else {'Accept': 'application/json'}
        if self.__dace_rc_config is not None:
            headers['Authorization'] = self.__dace_rc_config['user']['key']
        headers['User-Agent'] = '/'.join([__title__, __version__])
        return headers

    def __convert_to_numpy_data_by_instrument(self, data_by_instrument):
        numpy_data_by_instrument = defaultdict(
            lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: np.ndarray(0)))))
        for instrument in data_by_instrument.keys():
            for drs_version_or_bibcode in data_by_instrument[instrument].keys():
                for ins_mode in data_by_instrument[instrument][drs_version_or_bibcode].keys():
                    for parameter in data_by_instrument[instrument][drs_version_or_bibcode][ins_mode].keys():
                        numpy_data_by_instrument[instrument][drs_version_or_bibcode][ins_mode][
                            parameter] = np.array(
                            data_by_instrument[instrument][drs_version_or_bibcode][ins_mode][parameter])
        return numpy_data_by_instrument

    def __transform_values_with_occurrences(self, values, occurrences):
        full_vector = []
        for i, occurence in enumerate(occurrences):
            for j in range(0, occurence):
                full_vector.append(values[i])

        return full_vector


Dace = DaceClass()
