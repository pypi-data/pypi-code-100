#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This module provides collection
of routines related to solvent
"""
import logging
import math
import os
import pathlib
import sys
from dataclasses import dataclass, field
from types import SimpleNamespace
from pprint import pprint
import numpy as np

from cdftpy.cdft1d.config import DATA_DIR
from cdftpy.cdft1d.io_utils import read_array, read_geom
from cdftpy.cdft1d.io_utils import read_key_value
from cdftpy.cdft1d.io_utils import read_system
from cdftpy.utils.rad_fft import RadFFT
from cdftpy.utils.units import hartree_2_kjmol, bohr_2_ang

logging.basicConfig(level=logging.INFO)

@dataclass
class Molecule:

    nv: int
    x: list[float]
    y: list[float]
    z: list[float]

    sigma:  list[float]
    eps:    list[float]
    charge: list[float]

    aname: list[str]
    atype: list[str]

    dipole: float = field(init=False)

    def __post_init__(self):
        q = self.charge
        mu2 = np.dot(self.x, q) ** 2 + np.dot(self.y, q) ** 2 + np.dot(self.z, q) ** 2
        self.dipole = np.sqrt(mu2)

    @classmethod
    def from_file(cls, filename):
        solvent = read_system(filename)
        solvent["nv"] = len(solvent["aname"])

        return cls(**solvent)

    def sm_k(self, kgrid):
        return compute_sm_rigid_bond(self.x, self.y, self.z, kgrid)

    def comp_dipole_moment(solvent_model):
        x = solvent_model.x
        y = solvent_model.y
        z = solvent_model.z
        q = solvent_model.charge

@dataclass
class Solvent(Molecule):
    filename: str
    file_location: str

    density: float
    temp: float

    dielectric: float=None

    ifft: object = None
    s_k: np.ndarray = None
    hbar_k: np.ndarray = None
    kgrid: np.ndarray = None

    @classmethod
    def from_file(cls, filename, rism_patch=False):
        solvent = read_system(filename,rism_patch=rism_patch)
        nv = len(solvent["aname"])
        solvent["nv"] = nv
        solvent["filename"] = os.path.abspath(filename)
        solvent["file_location"] = os.path.split(solvent["filename"][0])

        state = read_key_value(filename, "state")
        # grid = read_key_value(filename, "grid")
        # ngrid = grid["ngrid"]
        # solvent["ifft"] = RadFFT(grid["dr"], grid["ngrid"])

        # structure factors
        hbar, kgrid = read_array(filename, "hbar_k")
        s_k, kgrid = read_array(filename, "s_k")
        solvent["s_k"] = s_k
        solvent["hbar_k"] = hbar
        solvent["kgrid"] = kgrid
        if kgrid is not None:
            solvent["ifft"] = RadFFT.from_kgrid(kgrid)
        return cls(**solvent,**state)

    def zeta(self, beta):
        mu2 = self.dipole**2
        rho = self.density
        y3 = (hartree_2_kjmol / bohr_2_ang) * beta * 4 * np.pi * mu2 * rho / 3
        y3m = 1.0 - 1.0 / self.dielectric
        zeta = y3m / y3
        return zeta

    def to_smdl_file(self,filename, structure_factor):
        with open(filename,"w") as fp:
            fp.write("<geometry>\n")
            fp.write("# site   type   x     y     z\n")
            for i in range(self.nv):
                fp.write(F"{self.aname[i]}   {self.atype[i]}    {self.x[i]}     {self.y[i]}     {self.z[i]}\n" )

            fp.write("<interactions>\n")
            # fp.write("# type   sigma    eps(kj/mol)   charge(e)\n")
            fp.write(f"#{'type' : <10}{'sigma' : ^10}{'eps' : ^10}{'charge' : >10}\n")
            for i in range(self.nv):
                fp.write(F" {self.atype[i]: <10}{self.sigma[i]: ^10}{self.eps[i]: ^10}{self.charge[i]: >10}\n" )

            fp.write("<state>\n")
            fp.write(F"density {self.density}\n")
            fp.write(F"temp {self.temp}\n")
            fp.write(F"dielectric {self.dielectric}\n")

            s_k = structure_factor["s_k"]
            kgrid  = structure_factor["kgrid"]
            tag = structure_factor["tag"]
            ngrid = s_k.shape[-1]
            nv = s_k.shape[0]

            fp.write(F"<{tag}>\n")
            fp.write(F"{nv}   {ngrid}\n")
            for k in range(ngrid):
                fp.write(F"{kgrid[k]}   ")
                for i in range(nv):
                    for j in range(i, nv):
                        fp.write(F"{s_k[i,j,k]}  ")
                fp.write("\n")
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


if __name__ == "__main__":
    geom = read_geom("../data/s2.smdl")
    params = dict(density=1.0)
    # solvent = Solvent(**params,**geom)
    solvent = Solvent.from_file("../data/s2.smdl", rism_patch=True)

    structure_factor = dict (
        tag="s_k",
        kgrid = solvent.ifft.kgrid,
        s_k = solvent.s_k
    )
    solvent.to_smdl_file("test1.dat", structure_factor)
