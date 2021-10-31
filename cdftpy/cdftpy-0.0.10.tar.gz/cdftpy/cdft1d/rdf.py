#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
RDF analysis module
"""
import os

import numpy as np
from scipy.signal import argrelmax
from scipy.signal import argrelmin

from cdftpy.cdft1d.io_utils import print_banner


def analyze_rdf_peaks_sim(sim):
    analyze_rdf_peaks(sim.ifft, sim.solvent.aname, sim.h_r)


def write_rdf_sim(sim, dir="./"):
    write_rdf(sim.ifft, sim.solute.name, sim.solvent.aname, sim.h_r, dir=dir)


def analyze_rdf_peaks(ifft, nametag, h_r):

    rgrid = ifft.rgrid

    print_banner("RDF Analysis")
    for i, name in enumerate(nametag):
        imax0 = np.argmax(h_r[i, :])
        imax = argrelmax(h_r[i, :], order=5)[0]
        # imax0 = imax[0]
        imax1 = imax[imax > imax0][0]

        imin = argrelmin(h_r[i, :], order=5)[0]
        imin_filter = imin > imax0
        imin0 = imin[imin_filter][0]

        print(
            f"{name} first  max height/position: {rgrid[imax0]:<.2f} {h_r[i, imax0] + 1:<.2f}  "
        )
        print(
            f"{name} second max height/position: {rgrid[imax1]:<.2f} {h_r[i, imax1] + 1:<.2f}  "
        )
        print(
            f"{name} first  min height/position: {rgrid[imin0]:<.2f} {h_r[i, imin0] + 1:<.2f}  "
        )
        print("  ")


def write_rdf(ifft, solute_name, solvent_name, h_r, dir="./"):

    rgrid = ifft.rgrid
    print("\nGenerating RDFs")
    for i in range(len(solvent_name)):
        filename = os.path.join(dir, f"{solute_name}{solvent_name[i]}.rdf")
        print(f"Generating {os.path.abspath(filename)}")
        with open(filename, "w") as fp:
            fp.write(f"{'# r':<10} {'g(r)':<10}\n")

            for j in range(len(rgrid)):
                r = rgrid[j]
                rdf = h_r[i, j] - h_r[i, 0]
                fp.write(f"{r:<10.4} {rdf:<10.4}\n")
