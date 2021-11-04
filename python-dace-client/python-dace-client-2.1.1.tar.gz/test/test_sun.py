import os
import pytest
from pathlib2 import Path
from dace import DaceClass
from dace.sun import SunClass


@pytest.fixture(scope='module')
def sun_without_dace_authentication():
    dace = DaceClass(config_path=Path(str(Path(__file__).parent) + os.sep + 'config.ini'))
    return SunClass(dace_instance=dace)


@pytest.fixture(scope='module')
def sun_with_dace_authentication():
    dace = DaceClass(dace_rc_config_path=Path(str(Path(__file__).parent) + os.sep + 'resources' + os.sep + 'dacerc'),
                     config_path=Path(str(Path(__file__).parent) + os.sep + 'config.ini'))
    return SunClass(dace_instance=dace)


def test_should_query_sun_database(sun_with_dace_authentication):
    sun_data = sun_with_dace_authentication.query_database(limit=10)
    assert 'file_rootpath' in sun_data


def test_should_get_public_sun_data(sun_without_dace_authentication):
    sun_data = sun_without_dace_authentication.query_database(limit=10)
    assert 'file_rootpath' in sun_data


def test_should_get_timeseries_in_sun_database(sun_with_dace_authentication):
    sun_data = sun_with_dace_authentication.get_timeseries()
    assert 'filename' in sun_data


def test_should_download_multiple_sun_spectroscopy_files(sun_with_dace_authentication):
    expected_directory = '/tmp'
    expected_filename = 'test_sun_spectroscopy_multiple.tar.gz'
    expected_file = expected_directory + os.sep + expected_filename
    sun_with_dace_authentication.download('s1d',
                                          filters={'file_rootpath':
                                                       {'contains':
                                                            'r.HARPN.2016-01-03T15:36:20.496.fits'}},
                                          output_directory=expected_directory, output_filename=expected_filename)

    expected_file_path = Path(expected_file)
    assert expected_file_path.exists() is True


def test_should_download_sun_spectroscopy_files(sun_with_dace_authentication):
    expected_directory = '/tmp'
    expected_filename = 'test_download_sun_spectroscopy_files.tar.gz'
    expected_file = expected_directory + os.sep + expected_filename
    sun_with_dace_authentication.download_files(file_type='s1d', files=['r.HARPN.2016-01-03T15:36:20.496',
                                                                        'r.HARPN.2016-01-03T13:26:05.796'],
                                                output_directory=expected_directory, output_filename=expected_filename)

    expected_file_path = Path(expected_file)
    assert expected_file_path.exists() is True


@pytest.mark.skip(reason="File downloaded is way too big. Can be used just during development process")
def test_should_download_sun_public_release_all(sun_without_dace_authentication):
    expected_directory = '/tmp'
    expected_filename = 'sun_public_release_all.tar.gz'
    expected_full_file_path = expected_directory + os.sep + expected_filename
    sun_without_dace_authentication.download_public_release_all('2015', '12',
                                                                output_directory=expected_directory,
                                                                output_filename=expected_filename)

    expected_file_path = Path(expected_full_file_path)
    assert expected_file_path.exists() is True


@pytest.mark.skip(reason="File downloaded is way too big. Can be used just during development process")
def test_should_download_sun_public_release_ccf(sun_without_dace_authentication):
    expected_directory = '/tmp'
    expected_filename = 'sun_public_release_ccf.tar.gz'
    expected_file = expected_directory + os.sep + expected_filename
    sun_without_dace_authentication.download_public_release_ccf('2015', output_directory=expected_directory,
                                                                output_filename=expected_filename)

    expected_file_path = Path(expected_file)
    assert expected_file_path.exists() is True


# @pytest.mark.skip(reason="File downloaded is way too big. Can be used just during development process")
def test_should_download_sun_public_release_timeseries(sun_without_dace_authentication):
    expected_directory = '/tmp'
    expected_filename = 'sun_public_release_timeseries.tar.gz'
    expected_file = expected_directory + os.sep + expected_filename
    sun_without_dace_authentication.download_public_release_timeseries(output_directory=expected_directory,
                                                                       output_filename=expected_filename)

    expected_file_path = Path(expected_file)
    assert expected_file_path.exists() is True
