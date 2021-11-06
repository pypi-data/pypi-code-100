import pytest

import numpy as np
import xarray as xr

from mdtf_test_data.synthetic.horizontal import construct_rect_grid


@pytest.mark.parametrize("dlon,dlat,nx,ny", [(5, 5, 72, 36), (20, 20, 18, 9)])
def test_construct_rect_grid_1(dlon, dlat, nx, ny):
    result = construct_rect_grid(dlon, dlat)
    assert len(result.lon) == nx
    assert len(result.lat) == ny


@pytest.mark.parametrize("dlon,dlat,xbndsum", [(5, 5, 25920.0), (20, 20, 6480.0)])
def test_construct_rect_grid_2(dlon, dlat, xbndsum):
    result = construct_rect_grid(dlon, dlat, bounds=True)
    assert sorted(list(result.variables)) == ["lat", "lat_bnds", "lon", "lon_bnds"]
    assert result.lat_bnds.sum() == 0.0
    assert result.lon_bnds.sum() == xbndsum


@pytest.mark.parametrize("add_attrs", [(True), (False)])
def test_construct_rect_grid_3(add_attrs):
    result = construct_rect_grid(
        20, 20, add_attrs=add_attrs, bounds=True, attr_fmt="gfdl"
    )
    if add_attrs:
        assert len(result.lat.attrs) != 0
        assert len(result.lat_bnds.attrs) != 0
        assert len(result.lon.attrs) != 0
        assert len(result.lon_bnds.attrs) != 0
    else:
        assert len(result.lat.attrs) == 1
        assert len(result.lat_bnds.attrs) == 0
        assert len(result.lon.attrs) == 1
        assert len(result.lon_bnds.attrs) == 0
