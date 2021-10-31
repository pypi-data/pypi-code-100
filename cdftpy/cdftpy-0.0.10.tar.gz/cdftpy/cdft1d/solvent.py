#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This module provides collection
of routines related to solvent
"""
import logging
import os
import pathlib
import sys
from types import SimpleNamespace

import numpy as np

from cdftpy.cdft1d.config import DATA_DIR
from cdftpy.cdft1d.io_utils import read_array
from cdftpy.cdft1d.io_utils import read_key_value
from cdftpy.cdft1d.io_utils import read_system
from cdftpy.utils.rad_fft import RadFFT

logging.basicConfig(level=logging.INFO)


def solvent_model_locate(solvent_name):
    solvent = solvent_name + ".smdl"
    cwd = pathlib.Path.cwd()
    for path in [pathlib.Path.cwd(), DATA_DIR]:
        solvent_file = path / solvent
        if solvent_file.exists():
            break
    else:
        # print(f"Cannot find {solvent=}" in {str(cwd)} or {str(DATA_DIR)})
        print(f"Cannot find {solvent=} in ", cwd, DATA_DIR)
        print("Searched in ", cwd, DATA_DIR)
        sys.exit(1)
    print("SOLVENT FILE:", solvent_file)
    return solvent_file


def load_solvent_model(solvent_name, rism_patch=False):

    filename = solvent_model_locate(solvent_name)
    system = read_system(filename, rism_patch=rism_patch)
    solvent_model = SimpleNamespace(**system)
    solvent_model.nv = len(solvent_model.aname)
    solvent_model.filename = os.path.abspath(filename)
    solvent_model.file_location = os.path.split(solvent_model.filename)[0]

    grid = read_key_value(filename, "grid")
    solvent_model.ifft = RadFFT(grid["dr"], grid["ngrid"])

    # structure factors
    nv = solvent_model.nv
    ngrid = solvent_model.ifft.ngrid
    hbar, kgrid = read_array(nv, ngrid, filename, "hbar")
    s_k, kgrid = read_array(nv, ngrid, filename, "structure_factor")
    solvent_model.s_k = s_k
    solvent_model.hbar = hbar
    solvent_model.kgrid = kgrid

    # state variables
    state = read_key_value(filename, "state")
    solvent_model.density = state["density"]
    solvent_model.temp = state["temp"]
    solvent_model.dielectric = state["dielectric"]

    return solvent_model


def sik(x):
    if x < 1e-22:
        y = 1.0
    else:
        y = np.sin(x) / x
    return y


def compute_sm_rigid_bond(xv, yv, zv, kgrid):
    """
    Args:
        xv, yv, zv : x,y,z coordinates
        kgrid: reciprocal grid
    Returns:
        structure factor matrix (nv x nv x ngrid)
    """
    # form distance matrix
    d = (
        np.subtract.outer(xv, xv) ** 2
        + np.subtract.outer(yv, yv) ** 2
        + np.subtract.outer(zv, zv) ** 2
    )
    d = np.sqrt(d)

    d2 = np.multiply.outer(d, kgrid)
    sik_array = np.vectorize(sik)
    d2 = sik_array(d2)

    return d2


def comp_dipole_moment(solvent_model):
    x = solvent_model.x
    y = solvent_model.y
    z = solvent_model.z
    q = solvent_model.charge

    mu2 = np.dot(x, q) ** 2 + np.dot(y, q) ** 2 + np.dot(z, q) ** 2
    return np.sqrt(mu2)


if __name__ == "__main__":
    pass
