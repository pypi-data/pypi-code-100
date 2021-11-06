""" Module for generating synthetic datasets """

___all__ = [
    "mom6_rho2_coord",
]

import xarray as xr


def mom6_rho2_coord():
    """Generates GFDL AM4 pressure coordinate

    Returns
    -------
    xarray.DataArray
        GFDL AM4 pressure levels and half levels
    """

    rho2_l = [
        1013.75,
        1028.5,
        1029.2421875,
        1029.71875,
        1030.1796875,
        1030.625,
        1031.0546875,
        1031.46875,
        1031.8671875,
        1032.25,
        1032.6171875,
        1032.96875,
        1033.3046875,
        1033.625,
        1033.9296875,
        1034.21875,
        1034.4921875,
        1034.75,
        1034.9921875,
        1035.21875,
        1035.4296875,
        1035.625,
        1035.8046875,
        1035.96875,
        1036.1171875,
        1036.25,
        1036.375,
        1036.5,
        1036.625,
        1036.75,
        1036.875,
        1037,
        1037.125,
        1037.25,
        1037.65625,
    ]

    rho2_i = [
        999.5,
        1028,
        1029,
        1029.484375,
        1029.953125,
        1030.40625,
        1030.84375,
        1031.265625,
        1031.671875,
        1032.0625,
        1032.4375,
        1032.796875,
        1033.140625,
        1033.46875,
        1033.78125,
        1034.078125,
        1034.359375,
        1034.625,
        1034.875,
        1035.109375,
        1035.328125,
        1035.53125,
        1035.71875,
        1035.890625,
        1036.046875,
        1036.1875,
        1036.3125,
        1036.4375,
        1036.5625,
        1036.6875,
        1036.8125,
        1036.9375,
        1037.0625,
        1037.1875,
        1037.3125,
        1038,
    ]

    rho2_i_attrs = {
        "long_name": "Target Potential Density at interface",
        "units": "kg m-3",
        "axis": "Z",
        "positive": "down",
    }

    rho2_l_attrs = {
        "long_name": "Target Potential Density at cell center",
        "units": "kg m-3",
        "axis": "Z",
        "positive": "down",
        "edges": "rho2_i",
    }

    dset_out = xr.Dataset()
    dset_out["rho2_l"] = xr.DataArray(
        rho2_l, dims={"rho2_l": rho2_l}, coords={"rho2_l": rho2_l}, attrs=rho2_l_attrs
    )
    dset_out["rho2_i"] = xr.DataArray(
        rho2_i, dims={"rho2_i": rho2_i}, coords={"rho2_i": rho2_i}, attrs=rho2_i_attrs
    )

    return dset_out
