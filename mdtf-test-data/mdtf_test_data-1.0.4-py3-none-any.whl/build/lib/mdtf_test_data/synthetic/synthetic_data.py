#!/usr/bin/env python
""" Module for generating synthetic datasets """

___all__ = [
    "dataset_stats",
    "generate_synthetic_dataset",
    "generate_random_array",
    "write_to_netcdf",
]

import xarray as xr
import numpy as np
from mdtf_test_data.synthetic.horizontal import construct_rect_grid
from mdtf_test_data.synthetic.horizontal import construct_tripolar_grid
import mdtf_test_data.generators as generators

from mdtf_test_data.synthetic.time import generate_monthly_time_axis
from mdtf_test_data.synthetic.time import generate_daily_time_axis
from mdtf_test_data.synthetic.time import generate_hourly_time_axis

from mdtf_test_data.synthetic.vertical import gfdl_plev19_vertical_coord
from mdtf_test_data.synthetic.vertical import gfdl_vertical_coord
from mdtf_test_data.synthetic.vertical import ncar_hybrid_coord
from mdtf_test_data.synthetic.vertical import mom6_z_coord


def dataset_stats(filename, var=None, limit=None):
    """Prints statistics and attributes for a NetCDF file

    Parameters
    ----------
    filename : str, path-like
        Path to NetCDF file to analyze
    var : str, optional
        Variable to analyze (None prints a list of variables), by default None
    """
    dset = xr.open_dataset(filename, use_cftime=True)
    dset = dset.isel(time=slice(0, limit)) if limit is not None else dset
    if var is None:
        raise ValueError(f"Please specify a variable from {list(dset.variables)}")
    else:
        means = dset[var].mean(axis=(0, -2, -1)).values
        stds = dset[var].std(axis=(0, -2, -1)).values

        means = [means] if means.shape == () else list(means)
        stds = [stds] if stds.shape == () else list(stds)

        means = [float(x) for x in means]
        stds = [float(x) for x in stds]

        print(dset[var].attrs)
        print(list(zip(means, stds)))

    dset.close()

    return list(zip(means, stds))


def generate_synthetic_dataset(
    dlon,
    dlat,
    startyear,
    nyears,
    varname,
    timeres="mon",
    attrs=None,
    fmt="ncar",
    coords=None,
    generator="normal",
    generator_kwargs=None,
    stats=None,
    static=False,
    data=None,
    grid="standard",
):
    """Generates xarray dataset of syntheic data in NCAR format

    Parameters
    ----------
    dlon : float, optional
        Grid spacing in the x-dimension (longitude)
    dlat : float, optional
        Grid spacing in the y-dimension (latitude)
    startyear : int
        Start year for requested time axis
    nyears : int
        Number of years in requested time axis
    varname : str
        Variable name in output dataset
    attrs : dict, optional
        Variable attributes, by default None
    attrs : dict, optional
        Variable attributes, by default None
    attrs : dict, optional
        Variable attributes, by default None
    stats : tuple or list of tuples
        Array statistics in the format of [(mean,stddev)]
    static : bool
        Flag denoting if variable is static
    grid : str
        Type of output grid, either "standard" or "tripolar",
        by default "standard"

    Returns
    -------
    xarray.Dataset
        Dataset of synthetic data
    """

    attrs = {} if attrs is None else attrs

    # some logical control flags
    do_bounds = True if fmt == "cmip" else False

    # Step 1: set up the horizontal grid
    if grid == "tripolar":
        dset = construct_tripolar_grid(attr_fmt=fmt, retain_coords=True, add_attrs=True)
        xyshape = dset["mask"].shape
        latvar = "nlat" if "nlat" in list(dset.variables) else "yh"
        lonvar = "nlon" if "nlon" in list(dset.variables) else "xh"
        lat = dset[latvar]
        lon = dset[lonvar]
    else:
        dset = construct_rect_grid(
            dlon, dlat, add_attrs=True, attr_fmt=fmt, bounds=do_bounds
        )
        lat = dset.lat
        lon = dset.lon
        xyshape = (len(dset["lat"]), len(dset["lon"]))

    # Step 2: set up the time axis
    if static is False:
        if timeres == "mon":
            ds_time = generate_monthly_time_axis(startyear, nyears, timefmt=fmt)
        elif timeres == "day":
            ds_time = generate_daily_time_axis(startyear, nyears, timefmt=fmt)
        elif timeres == "3hr":
            ds_time = generate_hourly_time_axis(startyear, nyears, 3, timefmt=fmt)
        elif timeres == "1hr":
            ds_time = generate_hourly_time_axis(startyear, nyears, 1, timefmt=fmt)
        else:
            print(timeres)
            raise ValueError("Unknown time resolution requested")

        dset = ds_time.merge(dset)
        time = dset["time"]
        ntimes = len(time)
    else:
        ntimes = 1

    # Step 3: generate the vertical coordinate
    if stats is not None:
        stats = [stats] if not isinstance(stats, list) else stats
        if len(stats) > 1:
            if fmt == "ncar":
                dset = dset.merge(ncar_hybrid_coord())
                lev = dset.lev
            elif fmt == "gfdl":
                if len(stats) == 19:
                    dset = dset.merge(gfdl_plev19_vertical_coord())
                    lev = dset.plev19
                else:
                    dset = dset.merge(gfdl_vertical_coord())
                    lev = dset.pfull
            elif fmt == "cmip" and grid == "tripolar":
                dset = dset.merge(mom6_z_coord())
                lev = dset.lev
                assert len(stats) == len(
                    lev
                ), f" Length of stats {data.shape[1]} must match number of levels {len(lev)}."

    # Step 4: define the synthetic data generator kernel
    generator_kwargs = {} if generator_kwargs is None else generator_kwargs
    if stats is not None:
        generator_kwargs["stats"] = stats

    assert generator in list(
        generators.__dict__.keys()
    ), f"Unknown generator method: {generator}"
    generator = generators.__dict__[generator]

    # Step 5: generate the synthetic data array
    data = (
        generators.generate_random_array(
            xyshape, ntimes, generator=generator, generator_kwargs=generator_kwargs
        )
        if data is None
        else data
    )
    data = data.squeeze()

    # Step 6: convert to Xarray DataArray by assigning coords
    mask = dset["mask"].values if "mask" in dset.variables else 1.0
    data = np.array(data * mask, dtype=np.float32)

    if static is True:
        if len(data.shape) == 4:
            assert data.shape[1] == len(
                lev
            ), f" Length of stats {data.shape[1]} must match number of levels {len(lev)}."
            dset[varname] = xr.DataArray(data, coords=(lev, lat, lon), attrs=attrs)
        else:
            dset[varname] = xr.DataArray(data, coords=(lat, lon), attrs=attrs)
    else:
        if len(data.shape) == 4:
            print(varname)
            assert data.shape[1] == len(
                lev
            ), f" Length of stats {data.shape[1]} must match number of levels {len(lev)}."
            dset[varname] = xr.DataArray(
                data, coords=(time, lev, lat, lon), attrs=attrs
            )
        else:
            dset[varname] = xr.DataArray(data, coords=(time, lat, lon), attrs=attrs)
        dset.set_coords(("lat", "lon"))

    if coords is not None:
        dset[coords["name"]] = xr.DataArray(coords["value"], attrs=coords["atts"])
        dset[varname].attrs = {**dset[varname].attrs, "coordinates": coords["name"]}

    dset.attrs["convention"] = fmt

    if fmt == "cmip":
        if "bnds" in dset.variables:
            dset["bnds"].attrs = {"long_name": "vertex number"}
        cmip_global_atts = [
            "external_variables",
            "history",
            "table_id",
            "activity_id",
            "branch_method",
            "branch_time_in_child",
            "branch_time_in_parent",
            "comment",
            "contact",
            "Conventions",
            "creation_date",
            "data_specs_version",
            "experiment",
            "experiment_id",
            "forcing_index",
            "frequency",
            "further_info_url",
            "grid",
            "grid_label",
            "initialization_index",
            "institution",
            "institution_id",
            "license",
            "mip_era",
            "nominal_resolution",
            "parent_activity_id",
            "parent_experiment_id",
            "parent_mip_era",
            "parent_source_id",
            "parent_time_units",
            "parent_variant_label",
            "physics_index",
            "product",
            "realization_index",
            "realm",
            "source",
            "source_id",
            "source_type",
            "sub_experiment",
            "sub_experiment_id",
            "title",
            "tracking_id",
            "variable_id",
            "variant_info",
            "references",
            "variant_label",
        ]

        cmip_global_atts = {x: "" for x in cmip_global_atts}
        dset.attrs = {**dset.attrs, **cmip_global_atts}

    # remove unused fields
    if grid == "tripolar":
        dset = dset.drop_vars(["mask", "wet", "depth"])

    return dset


def write_to_netcdf(dset_out, outfile, time_dtype="float"):
    """Writes xarray dataset to NetCDF with proper encodings

    Parameters
    ----------
    dset_out : xarray.Dataset
        xarray dataset to write to NetCDF
    outfile : str, path-like
        Path to output file
    """

    base_time_unit = (
        dset_out.attrs["base_time_unit"]
        if "base_time_unit" in list(dset_out.attrs.keys())
        else "days since 0001-01-01"
    )

    encoding = {}
    for var in list(dset_out.variables):
        if var in ["time", "time_bnds", "average_T1", "average_T2"]:
            dset_out[var].encoding["units"] = base_time_unit
            if time_dtype == "float":
                dset_out[var].encoding["dtype"] = "float64"
                dset_out[var].encoding["_FillValue"] = 1.0e20
            elif time_dtype == "int":
                dset_out[var].encoding["dtype"] = "i4"
        elif var == "date":
            dset_out[var].encoding["dtype"] = "i4"
        elif "float" in str(dset_out[var].dtype):
            dset_out[var].encoding["_FillValue"] = 1.0e20
        elif "int" in str(dset_out[var].dtype):
            dset_out[var].encoding["_FillValue"] = -999
        else:
            dset_out[var].encoding["_FillValue"] = None

    # encoding = {"lat_bnds": {"units": "degrees_north"}}
    dset_out.to_netcdf(outfile, encoding=encoding)
