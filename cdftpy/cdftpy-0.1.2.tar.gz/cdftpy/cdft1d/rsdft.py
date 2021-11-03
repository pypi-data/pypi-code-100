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
from cdftpy.cdft1d.potential import compute_lj_potential_mod
from cdftpy.cdft1d.rdf import analyze_rdf_peaks_sim
from cdftpy.cdft1d.rdf import write_rdf_sim
from cdftpy.cdft1d.solvent import Solvent, solvent_model_locate
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


def rsdft_1d(solute, solvent, params=None):

    qs = solute["charge"]
    sig_s = solute["sigma"]
    eps_s = solute["eps"]

    rho_0 = solvent.density
    sig_v = solvent.sigma
    eps_v = solvent.eps
    qv = solvent.charge
    hbar = solvent.hbar_k


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

    zeta = solvent.zeta(beta)

    # initialize fft
    ifft = solvent.ifft
    rgrid = ifft.rgrid
    kgrid = ifft.kgrid

    # calculate lj potential
    vlj_r = beta * compute_lj_potential_mod(sig_s, eps_s, sig_v, eps_v, rgrid)

    # coulomb long and short range
    vl_k = beta * compute_long_range_coul_pot_kspace(qs, qv, kgrid)
    vl_r = beta * compute_long_range_coul_pot_rspace(qs, qv, rgrid)
    vcs_r = beta * compute_short_range_coul_pot_rspace(qs, qv, rgrid)

    # total short range potential
    vs_r = vcs_r + vlj_r

    # molecular structure factor
    sm = solvent.sm_k(kgrid)

    gl_r, gl_k = compute_gamma_long_range(ifft, hbar, sm, vl_k, vl_r, zeta)

    g_r = np.zeros(hbar[0].shape)

    print("")
    print_banner("   Self-consistent cycle     ")

    converged = False

    diis_update = diis_session()

    for it in range(max_iter):

        f_r, f_k = compute_mayer_function(ifft, vs_r, gl_r, gl_k, g_r)

        delta_h_r = compute_delta_h(ifft, sm, f_r, f_k)

        hm_r = compute_h_mol(f_r)

        h_r = hm_r + delta_h_r

        cs_k = compute_c_k(ifft, sm, h_r, g_r)

        gn_r = compute_g_r(ifft, hbar, cs_k, gl_r)

        # compute error
        dg_r = gn_r - g_r
        err = np.sum(dg_r ** 2)
        err = np.sqrt(err / gn_r.size)

        converged = err < tol

        if it % output_rate == 0 or converged:
            fe_tot = compute_free_energy(
                beta, rho_0, ifft, sm, vl_r, g_r, h_r, cs_k, vl_k
            )
            if it == 0:
                print(f"{'iter':<5} {DG_STRING:<12}{'Free Energy':<10} ")
            print(f"{it:<5} {err:>.2e}   {fe_tot:<.7f}")

        if converged:
            print(f"\nReached convergence, {DG_STRING} < {tol}")
            break

        g_r = diis_update(ndiis, gn_r, dg_r)

    if not converged:
        print(
            f"Could not reach specified convergence criteria after {max_iter} iterations"
        )
        sys.exit(1)

    # simple_2_plot(ifft.rgrid,h_r[0,:]+1,hm_r+1, xrange=[1, 8])
    # simple_2_plot(ifft.rgrid,h_r[1,:]+1,hm_r+1, xrange=[1, 8])

    print("\n")
    print(f"{'Total Free Energy ':<30} {fe_tot:>12.6f}")

    compute_free_energy(beta, rho_0, ifft, sm, vl_r, g_r, h_r, cs_k, vl_k)

    return SimpleNamespace(
        solute=SimpleNamespace(**solute),
        solvent=solvent,
        ifft=ifft,
        sm=sm,
        f_k=f_k,
        f_r=f_r,
        gl_r=gl_r,
        gl_k=gl_k,
        vl_r=vl_r,
        vl_k=vl_k,
        vcs_r=vcs_r,
        h_r=h_r,
        g_r=g_r,
        fe_tot=fe_tot,
    )


def compute_mayer_function(ifft, vs_r, gl_r, gl_k, g_r):
    f_r = np.exp(-vs_r + g_r) - 1.0

    delta_f_r = f_r - gl_r

    delta_f_k = np.apply_along_axis(ifft.to_kspace, 1, delta_f_r)

    f_k = delta_f_k + gl_k

    return f_r, f_k


def compute_h_mol(f_r):
    f1 = f_r + 1.0
    hm_r = np.prod(f1, axis=0) - 1

    return hm_r


def compute_delta_h(ifft, sm, f_r, f_k):
    dd = sm - 1.0

    dd_fk = np.einsum("abn,bn->an", dd, f_k)

    dd_fr = np.apply_along_axis(ifft.to_rspace, 1, dd_fk)

    dh_r = dd_fr * (1.0 + f_r)

    return dh_r


def compute_c_k(ifft, sm, h_r, g_r):
    h_k = np.apply_along_axis(ifft.to_kspace, 1, h_r)
    g_k = np.apply_along_axis(ifft.to_kspace, 1, g_r)

    c_k = h_k - np.einsum("abn,bn->an", sm, g_k)

    return c_k


def compute_g_r(ifft, hb, c_k, gl_r):
    hb_c_k = np.einsum("abn,bn->an", hb, c_k)

    hb_c_r = np.apply_along_axis(ifft.to_rspace, 1, hb_c_k)

    g_r = gl_r + hb_c_r

    return g_r


def compute_corr_pot(beta, vl_r, g_r):
    return -(g_r + vl_r) / beta


def compute_gamma_long_range(ifft, hb, sm, vl_k, vl_r, zeta):
    """

    Args:
        ifft: FFT instance
        hb: renormalized correlation function
        sm: molecular structure factor
        vl_k: long range coulomb potential in k-space
        vl_r: long range coulomb potential in k-space
        zeta: long range coulomb potential in k-space

    Returns:

    """

    hb_sm = np.einsum("abn,bcn->acn", hb, sm)

    gl_k = -np.einsum("abn,bn->an", hb_sm, vl_k) - vl_k

    delta_gl_k = gl_k + zeta * vl_k

    gl_r = np.apply_along_axis(ifft.to_rspace, 1, delta_gl_k)

    gl_r = gl_r - zeta * vl_r

    return gl_r, gl_k


def compute_free_energy(beta, rho_0, ifft, sm, vl_r, g_r, h_r, c_k, vl_k) -> float:
    phi_r = compute_corr_pot(beta, vl_r, g_r)

    ctot_k = c_k - np.einsum("abn,bn->an", sm, vl_k)

    fe0 = -rho_0 * np.sum(ctot_k[:, 0]) / 2 / beta
    fe1 = -0.5 * ifft.integrate_rspace(rho_0 * phi_r * h_r)
    return fe0 + fe1


if __name__ == "__main__":

    # load solvent model
    solvent_name = "s2"
    filename = solvent_model_locate(solvent_name)
    solvent = Solvent.from_file(filename)

    solute = dict(name="Cl", charge=-1.0, sigma=4.83, eps=0.05349244)
    params = dict(diis_iterations=2, tol=1.0e-7, max_iter=200)

    sim = rsdft_1d(solute, solvent, params=params)

    analyze_rdf_peaks_sim(sim)

    write_rdf_sim(sim)
