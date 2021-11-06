""" Collection of tools to coarsen model data """

__all__ = ["construct_tripolar_grid"]


import numpy as np
import xarray as xr
import pkg_resources as pkgr


def construct_tripolar_grid(
    point_type="t", add_attrs=False, attr_fmt="gfdl", retain_coords=False
):
    """Generate a tripolar grid based on a real 5-degree MOM6 configuration

    Parameters
    ----------
    point_type : str, optional
        Grid type. Options are t, u, v, c. By default "t" (tracer)
    add_attrs : bool, optional
        Include lat and lon variable attributes, by default False
    attr_fmt : str, optional
        Modeling center attribute format, by default "gfdl"
    retain_coords : bool, optional
        Keep geolon, geolat, and wet in the dataset, by default False

    Returns
    -------
    xarray.Dataset
        Shell dataset with masked variable and ocean depth field
    """

    ds_in = pkgr.resource_filename("mdtf_test_data", "resources/ocean_static_5deg.nc")
    ds_in = xr.open_dataset(ds_in)

    if point_type == "t":
        lat = ds_in["geolat"]
        lon = ds_in["geolon"]
        wet = ds_in["wet"]
    elif point_type == "u":
        lat = ds_in["geolat_u"]
        lon = ds_in["geolon_u"]
        wet = ds_in["wet_u"]
    elif point_type == "v":
        lat = ds_in["geolat_v"]
        lon = ds_in["geolon_v"]
        wet = ds_in["wet_v"]
    elif point_type == "c":
        lat = ds_in["geolat_c"]
        lon = ds_in["geolon_c"]
        wet = ds_in["wet_c"]

    dset = xr.Dataset()
    dset["mask"] = xr.where(wet == 0.0, np.nan, 1.0)

    if point_type == "t":
        dset["depth"] = xr.DataArray(ds_in["depth_ocean"])

    if retain_coords is True:
        dset[lat.name] = lat
        dset[lon.name] = lon
        dset[wet.name] = wet

        if add_attrs is True:
            if attr_fmt == "gfdl":
                dset[lat.name].attrs = {}
                dset[lon.name].attrs = {}
                dset[wet.name].attrs = {}
            elif attr_fmt == "ncar":
                dset[lat.name].attrs = {
                    "axis": "Y",
                    "standard_name": "latitude",
                    "title": "Latitude",
                    "type": "double",
                    "units": "degrees_north",
                    "valid_max": 90.0,
                    "valid_min": -90.0,
                }
                dset[lon.name].attrs = {
                    "axis": "X",
                    "standard_name": "longitude",
                    "title": "Longitude",
                    "type": "double",
                    "units": "degrees_east",
                    "valid_max": 360.0,
                    "valid_min": 0.0,
                }
                dset[wet.name].attrs = {}
            else:
                raise ValueError("Unknown attribute format")

        else:
            dset[lat.name].attrs = {}
            dset[lon.name].attrs = {}
            dset[wet.name].attrs = {}

    if attr_fmt == "ncar":
        dset = dset.rename({"xh": "nlon", "yh": "nlat"})

        lat_range = np.array(np.arange(1, len(dset["nlat"]) + 1, dtype=np.intc))
        dset["nlat"] = xr.DataArray(lat_range, dims=("nlat"))
        dset["nlat"].attrs = {
            "long_name": "cell index along second dimension",
            "units": "1",
        }

        lon_range = np.array(np.arange(1, len(dset["nlon"]) + 1, dtype=np.intc))
        dset["nlon"] = xr.DataArray(lon_range, dims=("nlon"))
        dset["nlon"].attrs = {
            "long_name": "cell index along first dimension",
            "units": "1",
        }

        dset = dset.rename({lat.name: "lat", lon.name: "lon"})

    return dset
