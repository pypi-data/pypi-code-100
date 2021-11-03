#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Main CDFT module
"""
import sys
from types import SimpleNamespace

import numpy as np

from cdftpy.cdft1d.coulomb import compute_long_range_coul_pot_kspace
from cdftpy.cdft1d.coulomb import compute_long_range_coul_pot_rspace
from cdftpy.cdft1d.coulomb import compute_short_range_coul_pot_rspace
from cdftpy.cdft1d.diis import diis_session
from cdftpy.cdft1d.io_utils import print_banner
from cdftpy.cdft1d.io_utils import print_simulation
from cdftpy.cdft1d.potential import compute_lj_potential
from cdftpy.cdft1d.solvent import solvent_model_locate, Solvent
from cdftpy.utils.units import R

HEADER = """
==================================
1D RSDFT PROGRAM

Marat Valiev and Gennady Chuev
==================================
"""

kb = R
PI = np.pi

DEFAULT_PARAMS = dict(diis_iterations=2, tol=1.0e-9, output_rate=10, max_iter=400)

DG_STRING = "|\u0394\u03B3|"


def rism_1d(solute, solvent, params=None):

    qs = solute["charge"]
    sig_s = solute["sigma"]
    eps_s = solute["eps"]

    rho_0 = solvent.density
    sig_v = solvent.sigma
    eps_v = solvent.eps
    qv = solvent.charge
    s_k = solvent.s_k

    delta = np.diagflat(np.ones(s_k.shape[0]))
    hbar = s_k - np.expand_dims(delta, axis=2)

    if params is None:
        params = DEFAULT_PARAMS
    params = {**DEFAULT_PARAMS, **params}

    ndiis = int(params["diis_iterations"])
    tol = float(params["tol"])
    max_iter = int(params["max_iter"])
    output_rate = int(params["output_rate"])

    if "temp" not in params:
        params["temp"] = solvent.temp

    temp = float(params["temp"])
    beta = 1.0 / (kb * temp)

    print(HEADER)
    print_simulation(solute, solvent, params)

    # initialize fft
    ifft = solvent.ifft
    rgrid = ifft.rgrid
    kgrid = ifft.kgrid

    # calculate lj potential
    vlj_r = beta * compute_lj_potential(sig_s, eps_s, sig_v, eps_v, rgrid)

    # coulomb long and short range
    vl_k = beta * compute_long_range_coul_pot_kspace(qs, qv, kgrid)
    vl_r = beta * compute_long_range_coul_pot_rspace(qs, qv, rgrid)
    vcs_r = beta * compute_short_range_coul_pot_rspace(qs, qv, rgrid)

    # total short range potential
    vs_r = vcs_r + vlj_r

    # molecular structure factor
    # sm = compute_sm_rigid_bond(solvent_model)

    # compute long range part of h as -beta S*v_l
    gl_k = -np.einsum("abn,bn->an", s_k, vl_k)
    gl_r = np.apply_along_axis(ifft.to_rspace, 1, gl_k)

    g_r = np.zeros(hbar[0].shape)

    print("")
    print_banner("   Self-consistent cycle     ")

    converged = False

    diis_update = diis_session()

    for it in range(max_iter):

        # calculate h
        h_r = np.exp(-vs_r + g_r) - 1.0

        # calculate short range c
        cs_r = h_r - g_r
        cs_k = np.apply_along_axis(ifft.to_kspace, 1, cs_r)

        # calculate gamma
        hbar_cs_k = np.einsum("abn,bn->an", hbar, cs_k)
        gn_r = np.apply_along_axis(ifft.to_rspace, 1, hbar_cs_k) + gl_r

        # compute error
        dg_r = gn_r - g_r
        err = np.sum(dg_r ** 2)
        err = np.sqrt(err / gn_r.size)

        converged = err < tol

        if it % output_rate == 0 or converged:
            fe = compute_free_energy(
                beta, rho_0, ifft, vl_r, g_r, h_r, cs_k, cs_r, vl_k
            )
            if it == 0:
                print(f"{'iter':<5} {DG_STRING:<12}{'Free Energy':<10} ")
            print(f"{it:<5} {err:>.2e}   {fe:<.7f}")

        if converged:
            print(f"\nReached convergence, {DG_STRING} < {tol}")
            break

        g_r = diis_update(ndiis, gn_r, dg_r)

    if not converged:
        print(
            f"Could not reach specified convergence criteria after {max_iter} iterations"
        )
        sys.exit(1)

    print("\n")
    print(f"{'Total Free Energy ':<30} {fe:>12.6f}")

    fe = compute_free_energy(beta, rho_0, ifft, vl_r, g_r, h_r, cs_k, cs_r, vl_k)

    return SimpleNamespace(
        solute=SimpleNamespace(**solute),
        solvent=solvent,
        ifft=ifft,
        gl_r=gl_r,
        gl_k=gl_k,
        vl_r=vl_r,
        vl_k=vl_k,
        vcs_r=vcs_r,
        h_r=h_r,
        g_r=g_r,
        fe_tot=fe,
    )


def compute_free_energy(beta, rho_0, ifft, vl_r, g_r, h_r, c_k, c_r, vl_k) -> float:

    phi_r = -(g_r + vl_r) / beta

    fe0 = -rho_0 * ifft.integrate_rspace(c_r) / beta
    fe1 = -0.5 * ifft.integrate_rspace(rho_0 * phi_r * h_r)
    return fe0 + fe1


if __name__ == "__main__":

    # load solvent model
    solvent_name = "s2"

    filename = solvent_model_locate(solvent_name)

    solvent = Solvent.from_file(filename, rism_patch=True)

    solute = dict(name="Na", charge=1.0, sigma=2.16, eps=1.4755)
    params = dict(diis_iterations=2, tol=1.0e-7, max_iter=200)

    sim = rism_1d(solute, solvent, params=params)

    print(abs(sim.fe_tot - -315.656312))
