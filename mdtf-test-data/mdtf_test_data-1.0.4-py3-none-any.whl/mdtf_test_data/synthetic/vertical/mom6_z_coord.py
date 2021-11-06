""" Module for generating synthetic datasets """

___all__ = [
    "mom6_z_coord",
]

import xarray as xr


def mom6_z_coord():
    """Generates GFDL AM4 pressure coordinate

    Returns
    -------
    xarray.DataArray
        GFDL AM4 pressure levels and half levels
    """

    z_l = [
        2.5,
        10,
        20,
        32.5,
        51.25,
        75,
        100,
        125,
        156.25,
        200,
        250,
        312.5,
        400,
        500,
        600,
        700,
        800,
        900,
        1000,
        1100,
        1200,
        1300,
        1400,
        1537.5,
        1750,
        2062.5,
        2500,
        3000,
        3500,
        4000,
        4500,
        5000,
        5500,
        6000,
        6500,
    ]

    z_i = [
        0,
        5,
        15,
        25,
        40,
        62.5,
        87.5,
        112.5,
        137.5,
        175,
        225,
        275,
        350,
        450,
        550,
        650,
        750,
        850,
        950,
        1050,
        1150,
        1250,
        1350,
        1450,
        1625,
        1875,
        2250,
        2750,
        3250,
        3750,
        4250,
        4750,
        5250,
        5750,
        6250,
        6750,
    ]

    z_i_attrs = {
        "standard_name": "depth_at_cell_interface",
        "long_name": "Depth at interface",
        "units": "meters",
        "axis": "Z",
        "positive": "down",
    }

    z_l_attrs = {
        "standard_name": "depth_at_cell_center",
        "long_name": "Depth at cell center",
        "units": "meters",
        "axis": "Z",
        "positive": "down",
        "edges": "z_i",
    }

    # duplicate of z_l with CMIP standard attributes
    lev_attrs = {
        "standard_name": "depth",
        "long_name": "depth",
        "units": "meters",
        "axis": "Z",
        "positive": "down",
    }

    dset_out = xr.Dataset()
    dset_out["z_l"] = xr.DataArray(
        z_l, dims={"z_l": z_l}, coords={"z_l": z_l}, attrs=z_l_attrs
    )
    dset_out["z_i"] = xr.DataArray(
        z_i, dims={"z_i": z_i}, coords={"z_i": z_i}, attrs=z_i_attrs
    )
    dset_out["lev"] = xr.DataArray(
        z_l, dims={"lev": z_l}, coords={"lev": z_l}, attrs=lev_attrs
    )

    return dset_out
