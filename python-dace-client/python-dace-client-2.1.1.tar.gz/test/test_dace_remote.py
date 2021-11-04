import os
from pathlib import Path
import pytest
from astropy.coordinates import SkyCoord, Angle, Galactic
import astropy.units as u

from dace import DaceClass
from dace.atmosphericSpectroscopy import AtmosphericSpectroscopyClass
from dace.catalog import CatalogClass
from dace.cheops import CheopsClass
from dace.exoplanet import ExoplanetClass
from dace.imaging import ImagingClass
from dace.lossy import LossyClass
from dace.opendata import OpenDataClass
from dace.photometry import PhotometryClass
from dace.astrometry import AstrometryClass
from dace.population import PopulationClass
from dace.spectroscopy import SpectroscopyClass
from dace.sun import SunClass
from dace.target import TargetClass


@pytest.fixture(scope='module')
def dace_without_authentication():
    return DaceClass(config_path=Path(str(Path(__file__).parent) + os.sep + 'config.ini'))


@pytest.fixture(scope='module')
def dace_with_authentication():
    return DaceClass(dace_rc_config_path=Path(str(Path(__file__).parent) + os.sep + 'resources' + os.sep + 'dacerc'),
                     config_path=Path(str(Path(__file__).parent) + os.sep + 'config.ini'))


@pytest.fixture(scope='module')
def cheops_with_dace_authentication():
    dace = DaceClass(dace_rc_config_path=Path(str(Path(__file__).parent) + os.sep + 'resources' + os.sep + 'dacerc'),
                     config_path=Path(str(Path(__file__).parent) + os.sep + 'config.ini'))
    return CheopsClass(dace_instance=dace)


@pytest.fixture(scope='module')
def population_with_dace_authentication():
    dace = DaceClass(dace_rc_config_path=Path(str(Path(__file__).parent) + os.sep + 'resources' + os.sep + 'dacerc'),
                     config_path=Path(str(Path(__file__).parent) + os.sep + 'config.ini'))
    return PopulationClass(dace_instance=dace)


@pytest.fixture(scope='module')
def lossy_with_dace_authentication():
    dace = DaceClass(dace_rc_config_path=Path(str(Path(__file__).parent) + os.sep + 'resources' + os.sep + 'dacerc'),
                     config_path=Path(str(Path(__file__).parent) + os.sep + 'config.ini'))
    return LossyClass(dace_instance=dace)


@pytest.fixture(scope='module')
def imaging_with_dace_authentication():
    dace = DaceClass(dace_rc_config_path=Path(str(Path(__file__).parent) + os.sep + 'resources' + os.sep + 'dacerc'),
                     config_path=Path(str(Path(__file__).parent) + os.sep + 'config.ini'))
    return ImagingClass(dace_instance=dace)


@pytest.fixture(scope='module')
def imaging_without_dace_authentication():
    dace = DaceClass(config_path=Path(str(Path(__file__).parent) + os.sep + 'config.ini'))
    return ImagingClass(dace_instance=dace)


@pytest.fixture(scope='module')
def spectroscopy_with_dace_authentication():
    dace = DaceClass(dace_rc_config_path=Path(str(Path(__file__).parent) + os.sep + 'resources' + os.sep + 'dacerc'),
                     config_path=Path(str(Path(__file__).parent) + os.sep + 'config.ini'))
    return SpectroscopyClass(dace_instance=dace)


@pytest.fixture(scope='module')
def spectroscopy_without_dace_authentication():
    dace = DaceClass(config_path=Path(str(Path(__file__).parent) + os.sep + 'config.ini'))
    return SpectroscopyClass(dace_instance=dace)


@pytest.fixture(scope='module')
def photometry_with_dace_authentication():
    dace = DaceClass(dace_rc_config_path=Path(str(Path(__file__).parent) + os.sep + 'resources' + os.sep + 'dacerc'),
                     config_path=Path(str(Path(__file__).parent) + os.sep + 'config.ini'))
    return PhotometryClass(dace_instance=dace)


@pytest.fixture(scope='module')
def gaia_astrometry_with_dace_authentication():
    dace = DaceClass(dace_rc_config_path=Path(str(Path(__file__).parent) + os.sep + 'resources' + os.sep + 'dacerc'),
                     config_path=Path(str(Path(__file__).parent) + os.sep + 'config.ini'))
    return AstrometryClass(dace_instance=dace)


@pytest.fixture(scope='module')
def target_with_authentication():
    dace = DaceClass(dace_rc_config_path=Path(str(Path(__file__).parent) + os.sep + 'resources' + os.sep + 'dacerc'),
                     config_path=Path(str(Path(__file__).parent) + os.sep + 'config.ini'))
    return TargetClass(dace_instance=dace)


@pytest.fixture(scope='module')
def photometry_without_dace_authentication():
    dace = DaceClass(config_path=Path(str(Path(__file__).parent) + os.sep + 'config.ini'))
    return PhotometryClass(dace_instance=dace)


@pytest.fixture(scope='module')
def exoplanet_without_dace_authentication():
    dace = DaceClass(config_path=Path(str(Path(__file__).parent) + os.sep + 'config.ini'))
    return ExoplanetClass(dace_instance=dace)


@pytest.fixture(scope='module')
def atmospheric_spectroscopy_without_dace_authentication():
    dace = DaceClass(config_path=Path(str(Path(__file__).parent) + os.sep + 'config.ini'))
    return AtmosphericSpectroscopyClass(dace_instance=dace)


@pytest.fixture(scope='module')
def catalog_without_authentication():
    dace = DaceClass(config_path=Path(str(Path(__file__).parent) + os.sep + 'config.ini'))
    return CatalogClass(dace_instance=dace)


@pytest.fixture(scope='module')
def catalog_with_dace_authentication():
    dace = DaceClass(dace_rc_config_path=Path(str(Path(__file__).parent) + os.sep + 'resources' + os.sep + 'dacerc'),
                     config_path=Path(str(Path(__file__).parent) + os.sep + 'config.ini'))
    return CatalogClass(dace_instance=dace)


@pytest.fixture(scope='module')
def target_without_authentication():
    dace = DaceClass(config_path=Path(str(Path(__file__).parent) + os.sep + 'config.ini'))
    return TargetClass(dace_instance=dace)


def test_should_download_files(spectroscopy_without_dace_authentication):
    expected_directory = '/tmp'
    expected_filename = 'toto.tar.gz'
    expected_file = expected_directory + os.sep + expected_filename
    spectroscopy_without_dace_authentication.download_files(file_type='all', files=['HARPS.2010-04-04T03:38:51.386',
                                                                                    'HARPS.2009-08-03T23:51:05.543.fits',
                                                                                    'HARPS.2007-05-12T23:14:49.500'],
                                                            output_directory=expected_directory,
                                                            output_filename=expected_filename)

    expected_file_path = Path(expected_file)
    assert expected_file_path.exists() is True


def test_should_get_spectro_time_series(spectroscopy_without_dace_authentication):
    spectro_time_series = spectroscopy_without_dace_authentication.get_timeseries('hd40307', sorted_by_instrument=False)
    assert 'ccf_noise' in spectro_time_series
    assert 'ccf_noise_err' in spectro_time_series
    assert 'ins_name' in spectro_time_series
    assert 'CORALIE98' in spectro_time_series['ins_name']


def test_should_get_spectro_time_series_by_instrument(spectroscopy_without_dace_authentication):
    sp_data_by_instrument = spectroscopy_without_dace_authentication.get_timeseries('hd40307')
    assert 'CORALIE98' in sp_data_by_instrument
    assert '3.3' in sp_data_by_instrument['CORALIE98']
    assert 'CORALIE' in sp_data_by_instrument['CORALIE98']['3.3']
    assert 'HARPS' in sp_data_by_instrument
    assert '2009A&A...493..639M' in sp_data_by_instrument['HARPS']
    assert 'default' in sp_data_by_instrument['HARPS']['2009A&A...493..639M']


def test_should_retrieve_photom_timeseries(photometry_without_dace_authentication):
    photom_timeseries = photometry_without_dace_authentication.get_timeseries('WASP-47')
    photometry_data_keys = photom_timeseries[0].keys()
    expected_keys = ['instrument', 'pubBibcode', 'pubRef', 'objDateRjdVect', 'photomFluxVect', 'photomFluxVectErr']
    assert all(key in photometry_data_keys for key in expected_keys)


def test_should_retrieve_astrometry_timeseries(gaia_astrometry_with_dace_authentication):
    gaia_astrometry_timeseries = gaia_astrometry_with_dace_authentication.get_gaia_timeseries('HD000905')
    gaia_astrometry_data_keys = gaia_astrometry_timeseries.keys()
    expected_keys = ['obj_id_catname', 'cpsi_obs']
    assert all(key in gaia_astrometry_data_keys for key in expected_keys)
    assert len(gaia_astrometry_timeseries['cpsi_obs']) > 10


def test_should_query_astrometry_database(gaia_astrometry_with_dace_authentication):
    gaia_astrometry_data = gaia_astrometry_with_dace_authentication.query_database()
    assert 'transit_id' in gaia_astrometry_data


def test_should_query_gaia_task_force_catalog(catalog_with_dace_authentication):
    catalog_data = catalog_with_dace_authentication.query_database('gaiataskforce')
    assert 'target' in catalog_data
    assert 'dr2_source_id' in catalog_data
    assert 'dr3_source_id' in catalog_data


def test_should_retrieve_exoplanet_data(exoplanet_without_dace_authentication):
    exoplanet_data = exoplanet_without_dace_authentication.query_database(
        filters={'db_info_name': {'contains': 'exoplanets.org'}})
    expected_keys = ['obj_id_catname', 'db_info_name', 'pub_info_detectiontype', 'obj_phys_mass_mjup',
                     'obj_phys_mass_mjup_errmin', 'obj_phys_mass_mjup_errmax', 'obj_phys_msini_mjup',
                     'obj_phys_msini_mjup_errmin', 'obj_phys_msini_mjup_errmax', 'obj_phys_radius_rjup',
                     'obj_phys_radius_rjup_errmin', 'obj_phys_radius_rjup_errmax', 'obj_orb_period_day',
                     'obj_orb_period_day_errmin', 'obj_orb_period_day_errmax', 'obj_orb_a_au',
                     'obj_orb_a_au_errmin', 'obj_orb_a_au_errmax', 'obj_orb_ecc', 'obj_orb_ecc_errmin',
                     'obj_orb_ecc_errmax', 'obj_orb_inc_deg',
                     'obj_orb_inc_deg_errmin', 'obj_orb_inc_deg_errmax',
                     'obj_orb_angdist_arcsec', 'obj_orb_angdist_arcsec_errmin', 'obj_orb_angdist_arcsec_errmax',
                     'pub_info_discovered_year', 'pub_info_updated',
                     'obj_orb_omega_deg', 'obj_orb_omega_deg_errmin', 'obj_orb_omega_deg_errmax',
                     'obj_orb_bigomega_deg', 'obj_orb_bigomega_deg_errmin', 'obj_orb_bigomega_deg_errmax',
                     'obj_orb_tperi_day', 'obj_orb_tperi_day_errmin', 'obj_orb_tperi_day_errmax',
                     'obj_orb_k_mps', 'obj_orb_k_mps_errmin', 'obj_orb_k_mps_errmax', 'obj_pos_alpha_deg',
                     'obj_pos_delta_deg', 'obj_stellar_magv',
                     'obj_stellar_rhk', 'obj_parent_phys_mass_msun',
                     'obj_parent_phys_mass_msun_errmin', 'obj_parent_phys_mass_msun_errmax',
                     'obj_parent_phys_radius_rsun', 'obj_parent_phys_radius_rsun_errmin',
                     'obj_parent_phys_radius_rsun_errmax',
                     'obj_parent_phys_feh', 'obj_parent_phys_feh_errmin', 'obj_parent_phys_feh_errmax',
                     'obj_parent_phys_teff_k',
                     'obj_parent_phys_teff_k_errmin', 'obj_parent_phys_teff_k_errmax', 'obj_orb_stardistance_pc',
                     'obj_orb_stardistance_pc_errmin', 'obj_orb_stardistance_pc_errmax']
    assert all(key in exoplanet_data for key in expected_keys)


def test_should_retrieve_exoplanet_data_with_multicontains_filters(exoplanet_without_dace_authentication):
    exoplanet_data = exoplanet_without_dace_authentication.query_database(
        filters={'db_info_name': {'contains': ['exoplanets.org', 'Exoplanet.eu']}})
    assert 'exoplanets.org', 'Exoplanet.eu' in exoplanet_data


def test_should_retrieve_target_database_informations(target_with_authentication):
    # Works only when logged in
    limit = 10
    target_database_data = target_with_authentication.query_database(limit=limit)
    expected_keys = ['obj_id_basename', 'obj_id_catname', 'obj_pos_coordinates_hms_dms',
                     'prog_id', 'ins_name',
                     'obj_pos_pmra_maspyr', 'obj_pos_pmdec_maspyr', 'obj_pos_plx_mas',
                     'obj_sptype']
    assert all(key in target_database_data for key in expected_keys)
    assert len(target_database_data['obj_id_basename']) == limit


def test_should_block_to_retrieve_stellar_informations_from_target_database(target_without_authentication):
    data = target_without_authentication.query_database()
    assert not data  # Ensure that retrieving target_database is blocked without authentication


def test_should_get_imaging_infos(imaging_without_dace_authentication):
    expected_imaging_dataset = {'ins_name': ['SPHERE'], 'prog_id': ['097.C-0893'], 'obj_date_bjd': [57589.85],
                                'img_filter': ['DB_H23'], 'img_mode': ['Saturated PSF'],
                                'file_rootpath': ['SPHERE.2016-07-20T08:26:19.6113_eclipse.fits'],
                                'date_night': ['2016-07-19'],
                                'ins_drs_name': ['ECLIPSE'],
                                'obj_id_catname': ['HD4113'],
                                'obj_id_daceid': ['1197161'],
                                'public': [True],
                                'obj_pos_coordinates_hms_dms': ['00:43:12.54 / -37:59:00.13']}
    imaging_dataset = imaging_without_dace_authentication.query_database(
        filters={'obj_id_catname': {'contains': 'HD4113'}})
    assert imaging_dataset == expected_imaging_dataset


def test_should_download_imaging_files(imaging_without_dace_authentication):
    expected_directory = '/tmp'
    expected_filename = 'imaging.fits'
    expected_file = expected_directory + os.sep + expected_filename
    imaging_without_dace_authentication.get_image('SPHERE.2016-07-20T08:26:19.6113_eclipse.fits', 'HC',
                                                  output_directory=expected_directory,
                                                  output_filename=expected_filename)
    expected_file_path = Path(expected_file)
    assert expected_file_path.exists() is True


def test_should_query_catalog_database(catalog_without_authentication):
    catalog_data = catalog_without_authentication.query_database('tess')
    assert 'obj_id_tic' in catalog_data
    assert 'obj_id_toi' in catalog_data
    assert 'obj_id_hip' in catalog_data


def test_should_query_cheops_database(cheops_with_dace_authentication):
    cheops_data = cheops_with_dace_authentication.query_database()
    assert 'file_rootpath' in cheops_data


def test_should_query_cheops_catalog(cheops_with_dace_authentication):
    cheops_data = cheops_with_dace_authentication.query_catalog('planet')
    assert 'obj_id_planet_catname' in cheops_data
    cheops_data = cheops_with_dace_authentication.query_catalog('stellar')
    assert 'obj_mag_b' in cheops_data


def test_should_raise_value_error_for_unknown_catalog(cheops_with_dace_authentication):
    with pytest.raises(ValueError):
        cheops_with_dace_authentication.query_catalog('unknown')


def test_should_query_cheops_region(cheops_with_dace_authentication):
    cheops_data = cheops_with_dace_authentication.query_region(
        SkyCoord('15:19:26.8271336166', '-07:43:20.190958776', unit=(u.hourangle, u.deg)), Angle('0.045d'))
    assert all(
        key in cheops_data.keys() for key in ['obj_id_catname', 'file_rootpath', 'obj_mag_cheops'])
    assert any(name == 'GJ 581' for name in cheops_data['obj_id_catname'])


def test_should_retrieve_cheops_photom_timeseries(cheops_with_dace_authentication):
    ligthcurve_data = cheops_with_dace_authentication.get_lightcurve('GJ 536')
    lightcurve_data_keys = ligthcurve_data.keys()
    expected_keys = ['obj_date_bjd_vect', 'photom_flux_vect', 'photom_flux_vect_err']
    assert all(key in lightcurve_data_keys for key in expected_keys)


def test_should_retrieve_cheops_photom_timeseries_with_filters(cheops_with_dace_authentication):
    ligthcurve_data = cheops_with_dace_authentication.get_lightcurve('HD 136352', filters={
        'file_key': {'contains': 'CH_PR100041_TG000902_V0100'}})
    lightcurve_data_keys = ligthcurve_data.keys()
    expected_keys = ['obj_date_bjd_vect', 'photom_flux_vect', 'photom_flux_vect_err']
    assert all(key in lightcurve_data_keys for key in expected_keys)
    assert 'CH_PR100041_TG000902_V0100' in ligthcurve_data['file_key']


def test_should_download_cheops_file(cheops_with_dace_authentication):
    expected_directory = '/tmp'
    expected_filename = 'cheopstestapi.tar.gz'
    expected_file = expected_directory + os.sep + expected_filename
    cheops_with_dace_authentication.download('reports',
                                             filters={'file_rootpath':
                                                          {'contains':
                                                               'PR300003_TG000302_V0100'}},
                                             output_directory=expected_directory, output_filename=expected_filename)

    expected_file_path = Path(expected_file)
    assert expected_file_path.exists() is True


def test_should_download_cheops_movie_file(cheops_with_dace_authentication):
    expected_directory = '/tmp'
    expected_filename = 'cheops_movie.mp4'
    expected_file = expected_directory + os.sep + expected_filename
    cheops_with_dace_authentication.download_diagnostic_movie('CH_PR300001_TG000301_V0100',
                                                              output_directory=expected_directory,
                                                              output_filename=expected_filename)
    expected_file_path = Path(expected_file)
    assert expected_file_path.exists() is True


def test_should_get_atmospheric_data(atmospheric_spectroscopy_without_dace_authentication):
    atmospheric_data = atmospheric_spectroscopy_without_dace_authentication.query_database()
    expected_keys = ['file_rootpath', 'spectral_domains', 'prog_id']
    assert all(key in atmospheric_data.keys() for key in expected_keys)


def test_should_get_samples(lossy_with_dace_authentication):
    samples = lossy_with_dace_authentication.query_database()
    expected_keys = ['sample_id', 'date', 'experimentalist']
    assert all(key in samples.keys() for key in expected_keys)


def test_should_get_sample_data(lossy_with_dace_authentication):
    samples = lossy_with_dace_authentication.get_sample('SAMPLE_Microgrit_WCA_1_20170807_000')
    assert all(key in samples.keys() for key in ['sample_id', 'phase', 'sample_temperature', 'relative_time'])


def test_should_get_all_populations(population_with_dace_authentication):
    populations = population_with_dace_authentication.query_database()
    assert all(key in populations.keys() for key in ['population_id', 'description', 'visibility', 'order', 'image'])


def test_should_get_columns_for_a_population(population_with_dace_authentication):
    columns = population_with_dace_authentication.get_columns('cd2133')
    assert all(key in columns.keys() for key in ['name', 'label', 'type', 'ordinal'])


def test_should_get_snapshots_for_a_population(population_with_dace_authentication):
    snapshots = population_with_dace_authentication.get_snapshots('cd2133', 5000000000)
    assert all(key in snapshots.keys() for key in population_with_dace_authentication.SNAPSHOTS_DEFAULT_COLUMN)


def test_should_get_simulations_for_a_population(population_with_dace_authentication):
    snapshots = population_with_dace_authentication.get_track('cd2133', 1, 1)
    assert all(key in snapshots.keys() for key in population_with_dace_authentication.SIMULATIONS_DEFAULT_COLUMN)


def test_should_get_snapshots_ages(population_with_dace_authentication):
    snapshot_ages = population_with_dace_authentication.get_snapshot_ages()
    assert all(age in snapshot_ages for age in
               [100000.0, 200000.0, 300000.0, 400000.0, 500000.0, 600000.0, 700000.0, 800000.0, 900000.0, 1000000.0,
                2000000.0,
                3000000.0, 4000000.0, 5000000.0, 6000000.0, 7000000.0, 8000000.0, 9000000.0, 10000000.0, 20000000.0,
                30000000.0,
                40000000.0, 50000000.0, 60000000.0, 70000000.0, 80000000.0, 90000000.0, 100000000.0, 200000000.0,
                300000000.0,
                400000000.0, 500000000.0, 600000000.0, 700000000.0, 800000000.0, 900000000.0, 1000000000.0,
                2000000000.0,
                3000000000.0, 4000000000.0, 5000000000.0, 6000000000.0, 7000000000.0, 8000000000.0, 9000000000.0,
                10000000000.0])


def test_should_query_imaging_database(imaging_with_dace_authentication):
    imaging = imaging_with_dace_authentication.query_database()
    assert all(
        key in imaging.keys() for key in ['file_rootpath', 'date_night', 'img_filter', 'img_mode', 'ins_drs_name'])


def test_should_download_multiple_imaging_files(imaging_with_dace_authentication):
    expected_directory = '/tmp'
    expected_filename = 'imaging_multiple.tar.gz'
    expected_file = expected_directory + os.sep + expected_filename
    imaging_with_dace_authentication.download('ns',
                                              filters={'file_rootpath':
                                                           {'contains':
                                                                '2016-05-02/NACO.2016-05-03T05:57:05.611_cadi.fits'}},
                                              output_directory=expected_directory, output_filename=expected_filename)

    expected_file_path = Path(expected_file)
    assert expected_file_path.exists() is True


def test_should_query_spectroscopy_database(spectroscopy_with_dace_authentication):
    spectroscopy = spectroscopy_with_dace_authentication.query_database(limit=10)
    assert all(
        key in spectroscopy.keys() for key in ['file_rootpath', 'ins_name', 'obj_date_bjd'])


def test_should_query_spectroscopy_region(spectroscopy_with_dace_authentication):
    spectroscopy_data = spectroscopy_with_dace_authentication.query_region(SkyCoord(88.5176, -60.023, unit='deg'),
                                                                           Angle('0.045d'))
    assert all(
        key in spectroscopy_data.keys() for key in ['file_rootpath', 'ins_name', 'obj_date_bjd'])
    assert any(name == 'HD40307' for name in spectroscopy_data['obj_id_catname'])


def test_should_download_multiple_spectroscopy_files(spectroscopy_with_dace_authentication):
    expected_directory = '/tmp'
    expected_filename = 'spectroscopy_multiple.tar.gz'
    expected_file = expected_directory + os.sep + expected_filename
    spectroscopy_with_dace_authentication.download('s1d',
                                                   filters={'file_rootpath':
                                                                {'contains': 'HARPS.2010-04-04T03:38:51.386.fits'}},
                                                   output_directory=expected_directory,
                                                   output_filename=expected_filename)

    expected_file_path = Path(expected_file)
    assert expected_file_path.exists() is True


def test_should_query_photometry_database(photometry_with_dace_authentication):
    photometry = photometry_with_dace_authentication.query_database(limit=10)
    assert all(
        key in photometry.keys() for key in
        ['file_rootpath', 'ins_name', 'obj_date_bjd', 'obj_id_catname', 'obj_id_daceid', 'prog_id'])


def test_should_query_photometry_region(photometry_without_dace_authentication):
    photometry_data = photometry_without_dace_authentication.query_region(
        SkyCoord(89.52458333333333, -57.31019444444445, unit='deg'),
        Angle('0.045d'))
    assert all(
        key in photometry_data.keys() for key in ['file_rootpath', 'ins_name', 'obj_pos_coordinates_hms_dms'])
    assert any(name == 'TIC350821761' for name in photometry_data['obj_id_catname'])


def test_should_query_imaging_region(imaging_without_dace_authentication):
    imaging_data = imaging_without_dace_authentication.query_region(
        SkyCoord('00:43:12.59', '-37:58:57.479', unit=(u.hourangle, u.deg)),
        Angle('0.045d'))
    assert all(
        key in imaging_data.keys() for key in ['file_rootpath', 'ins_name', 'obj_pos_coordinates_hms_dms'])
    assert any(name == 'HD4113' for name in imaging_data['obj_id_catname'])


def test_output_formats(spectroscopy_without_dace_authentication):
    numpy_data = spectroscopy_without_dace_authentication.get_timeseries('hd40307', sorted_by_instrument=False,
                                                                         output_format='numpy')
    for key in numpy_data.keys():
        assert 'numpy' in str(type(numpy_data[key]))

    pandas_data = spectroscopy_without_dace_authentication.get_timeseries('hd40307', sorted_by_instrument=False,
                                                                          output_format='pandas')
    assert 'DataFrame' in str(type(pandas_data))

    astropy_table_data = spectroscopy_without_dace_authentication.get_timeseries('hd40307', sorted_by_instrument=False,
                                                                                 output_format='astropy_table')
    assert 'Table' in str(type(astropy_table_data))

    dict_data = spectroscopy_without_dace_authentication.get_timeseries('hd40307', sorted_by_instrument=False)
    for key in dict_data.keys():
        assert 'list' in str(type(dict_data[key]))

    numpy_data_by_instrument = spectroscopy_without_dace_authentication.get_timeseries('hd40307', output_format='numpy')

    assert 'CORALIE98' in numpy_data_by_instrument
    assert '3.3' in numpy_data_by_instrument['CORALIE98']
    assert 'CORALIE' in numpy_data_by_instrument['CORALIE98']['3.3']
    for parameter in numpy_data_by_instrument['CORALIE98']['3.3']['CORALIE'].keys():
        assert 'numpy' in str(type(numpy_data_by_instrument['CORALIE98']['3.3']['CORALIE'][parameter]))
