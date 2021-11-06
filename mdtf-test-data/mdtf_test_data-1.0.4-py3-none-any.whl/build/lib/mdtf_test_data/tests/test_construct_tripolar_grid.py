import pytest

import numpy as np
import xarray as xr

from mdtf_test_data.synthetic.horizontal import construct_tripolar_grid


@pytest.mark.parametrize("retain_coords", [(False), (True)])
def test_construct_tripolar_grid_t(retain_coords):
    result = construct_tripolar_grid(retain_coords=retain_coords)
    assert isinstance(result, xr.Dataset)
    assert sorted(list(result.coords)) == ["xh", "yh"]
    assert sorted(list(result.dims)) == ["xh", "yh"]
    varlist = (
        ["depth", "geolat", "geolon", "mask", "wet", "xh", "yh"]
        if retain_coords
        else ["depth", "mask", "xh", "yh"]
    )
    assert sorted(list(result.variables)) == varlist
    assert result.depth.sum() == 5558217.0
    assert result.mask.sum() == 1640.0
    assert result.xh.sum() == -7200.0
    assert np.allclose(result.yh.sum(), 1.42108547e-14)
    assert result.yh.min() == -87.5
    if retain_coords:
        assert np.allclose(result.geolon.sum(), -259200.0)
        assert np.allclose(result.geolat.sum(), -1679.41633401)
        assert result.wet.sum() == 1640.0
        pytest.tripolar_t = result


@pytest.mark.parametrize("retain_coords", [(False), (True)])
def test_construct_tripolar_grid_u(retain_coords):
    result = construct_tripolar_grid(point_type="u", retain_coords=retain_coords)
    assert isinstance(result, xr.Dataset)
    assert sorted(list(result.coords)) == ["xq", "yh"]
    assert sorted(list(result.dims)) == ["xq", "yh"]
    varlist = (
        ["geolat_u", "geolon_u", "mask", "wet_u", "xq", "yh"]
        if retain_coords
        else ["mask", "xq", "yh"]
    )
    assert sorted(list(result.variables)) == varlist
    assert result.mask.sum() == 1561.0
    assert result.xq.sum() == -7300.0
    assert np.allclose(result.yh.sum(), 1.42108547e-14)
    assert result.yh.min() == -87.5
    if retain_coords:
        assert np.allclose(result.geolon_u.sum(), -262800.0)
        assert np.allclose(result.geolat_u.sum(), -1744.9609)
        assert result.wet_u.sum() == 1561.0


@pytest.mark.parametrize("retain_coords", [(False), (True)])
def test_construct_tripolar_grid_v(retain_coords):
    result = construct_tripolar_grid(point_type="v", retain_coords=retain_coords)
    assert isinstance(result, xr.Dataset)
    assert sorted(list(result.coords)) == ["xh", "yq"]
    assert sorted(list(result.dims)) == ["xh", "yq"]
    varlist = (
        ["geolat_v", "geolon_v", "mask", "wet_v", "xh", "yq"]
        if retain_coords
        else ["mask", "xh", "yq"]
    )
    assert sorted(list(result.variables)) == varlist
    assert result.mask.sum() == 1512.0
    assert result.xh.sum() == -7200.0
    assert np.allclose(result.yq.sum(), 1.42108547e-14)
    assert result.yq.min() == -90.0
    if retain_coords:
        assert np.allclose(result.geolon_v.sum(), -266400.0)
        assert np.allclose(result.geolat_v.sum(), -2106.3906)
        assert result.wet_v.sum() == 1512.0


@pytest.mark.parametrize("retain_coords", [(False), (True)])
def test_construct_tripolar_grid_c(retain_coords):
    result = construct_tripolar_grid(point_type="c", retain_coords=retain_coords)
    assert isinstance(result, xr.Dataset)
    assert sorted(list(result.coords)) == ["xq", "yq"]
    assert sorted(list(result.dims)) == ["xq", "yq"]
    varlist = (
        ["geolat_c", "geolon_c", "mask", "wet_c", "xq", "yq"]
        if retain_coords
        else ["mask", "xq", "yq"]
    )
    assert sorted(list(result.variables)) == varlist
    assert result.mask.sum() == 1426.0
    assert result.xq.sum() == -7300.0
    assert np.allclose(result.yq.sum(), 1.42108547e-14)
    assert result.yq.min() == -90.0
    if retain_coords:
        assert np.allclose(result.geolon_c.sum(), -270100.0)
        assert np.allclose(result.geolat_c.sum(), -2184.3828)
        assert result.wet_c.sum() == 1426.0


def test_construct_tripolar_grid_ncar():
    result = construct_tripolar_grid(
        attr_fmt="ncar", add_attrs=True, retain_coords=True
    )
    assert sorted(list(result.coords)) == ["nlat", "nlon"]
    assert sorted(list(result.dims)) == ["nlat", "nlon"]
    varlist = ["depth", "lat", "lon", "mask", "nlat", "nlon", "wet"]
    assert sorted(list(result.variables)) == varlist
    assert result.nlat.sum() == 666
    assert result.nlon.sum() == 2628
    assert np.allclose(
        result.depth.to_masked_array(), pytest.tripolar_t.depth.to_masked_array()
    )
    assert np.allclose(
        result.mask.to_masked_array(), pytest.tripolar_t.mask.to_masked_array()
    )
    assert np.allclose(
        result.wet.to_masked_array(), pytest.tripolar_t.wet.to_masked_array()
    )
