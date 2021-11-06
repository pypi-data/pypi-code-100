#!/usr/bin/env python
""" Collection of tools to coarsen model data """

__all__ = ["regrid_lat_lon_dataset"]

import warnings

from mdtf_test_data.synthetic.horizontal import construct_rect_grid

try:
    import xesmf as xe
except Exception as e:
    warnings.warn("Unable to load `xesmf`. Regridding functionality will not work.")


def regrid_lat_lon_dataset(dset, dlon=10.0, dlat=10.0, method="bilinear"):
    """Regrids xarray dataset to a standard lat-lon grid

    Parameters
    ----------
    dset : xarray.Dataset
        Input dataset.  Must have horizonatal dimensions of "lat" and "lon"
    dlon : float, optional
        Grid spacing in the x-dimension (longitude)
    dlat : float, optional
        Grid spacing in the y-dimension (latitude)
    method : str, optional
        xESMF regridding option, by default "bilinear"

    Returns
    -------
    xarray.Dataset
        Regridded data set
    """

    # Define output grid.
    dset_out = construct_rect_grid(dlon=dlon, dlat=dlat)

    # Create xESMF regridder object
    regridder = xe.Regridder(dset, dset_out, method)

    # Loop over variables
    for var in list(dset.variables):
        _dim = list(dset[var].dims)
        if "lat" in _dim and "lon" in _dim:
            _regridded = regridder(dset[var])
            dset_out[var] = _regridded.astype(dset[var].dtype)
            dset_out[var].attrs = dset[var].attrs
        elif var not in ["lat", "lon"]:
            dset_out[var] = dset[var]

    # Copy coordinate metadata
    dset_out["lat"].attrs = dset["lat"].attrs
    dset_out["lon"].attrs = dset["lon"].attrs

    # Copy dataset metadata
    dset_out.attrs = dset.attrs
    dset_out.attrs["coarsen_method"] = f"xESMF {method}"

    return dset_out
