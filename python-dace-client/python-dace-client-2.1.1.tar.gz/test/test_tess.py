import os
import pytest
from pathlib2 import Path
from dace import DaceClass
from dace.tess import TessClass
from astropy.coordinates import SkyCoord, Angle, Galactic
import astropy.units as u

@pytest.fixture(scope='module')
def tess_without_dace_authentication():
    dace = DaceClass(config_path=Path(str(Path(__file__).parent) + os.sep + 'config.ini'))
    return TessClass(dace_instance=dace)

def test_should_query_tess_database(tess_without_dace_authentication):
    sectors = tess_without_dace_authentication.query_database(limit=10)
    assert 'file_rootpath' in sectors

def test_should_query_tess_region(tess_without_dace_authentication):
    tess_data = tess_without_dace_authentication.query_region(
        SkyCoord('03:24:53.6160', '-59:01:50.8800', unit=(u.hourangle, u.deg)), Angle('0.045d'))
    assert any(name == 'TIC197789536' for name in tess_data['obj_id_catname'])

def test_should_query_tess_database(tess_without_dace_authentication):
    sectors = tess_without_dace_authentication.query_database(limit=10)
    assert 'file_rootpath' in sectors

def test_should_retrieve_tess_photom_timeseries(tess_without_dace_authentication):
    ligthcurve_data = tess_without_dace_authentication.get_lightcurve('TIC421937540')
    lightcurve_data_keys = ligthcurve_data.keys()
    expected_keys = ['dataset_id','quality','corr_flux','corr_flux_err','raw_flux','raw_flux_err','time']
    assert all(key in lightcurve_data_keys for key in expected_keys)
    assert len(ligthcurve_data['raw_flux']) > 0
