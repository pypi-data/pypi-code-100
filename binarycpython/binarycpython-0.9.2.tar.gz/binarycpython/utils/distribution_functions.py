"""
Module containing the predefined distribution functions

The user can use any of these distribution functions to
generate probability distributions for sampling populations

There are distributions for the following parameters:
    - mass
    - period
    - mass ratio
    - binary fraction

Tasks:
    - TODO: make some things globally present? rob does this in his module..i guess it saves
        calculations but not sure if I'm gonna do that now
    - TODO: add eccentricity distribution: thermal
    - TODO: Add SFH distributions depending on redshift
    - TODO: Add metallicity distributions depending on redshift
    - TODO: Add initial rotational velocity distributions
    - TODO: make an n-part power law that's general enough to fix the three part and the 4 part
"""

import functools
import math
import json

import traceback
import sys

from typing import Union

import numpy as np

from binarycpython.utils.useful_funcs import calc_period_from_sep, calc_sep_from_period
from binarycpython.utils.functions import verbose_print
from binarycpython.utils.grid_options_defaults import (
    _MOE2017_VERBOSITY_LEVEL,
    _MOE2017_VERBOSITY_INTERPOLATOR_LEVEL,
)

###
# File containing probability distributions
# Mostly copied from the Perl modules
LOG_LN_CONVERTER = 1.0 / math.log(10.0)
distribution_constants = {}  # To store the constants in


def prepare_dict(global_dict: dict, list_of_sub_keys: list) -> None:
    """
    Function that makes sure that the global dict is prepared to have a value set there.
    This dictionary will store values and factors for the distribution functions,
    so that they don't have to be calculated each time.

    Args:
        global_dict: globally accessible dictionary where factors are stored in
        list_of_sub_keys: List of keys that must become be(come) present in the global_dict
    """

    internal_dict_value = global_dict

    # This loop almost mimics a recursive loop into the dictionary.
    # It checks whether the first key of the list is present, if not; set it with an empty dict.
    # Then it overrides itself to be that (new) item, and goes on to do that again, until the list
    # exhausted
    for k in list_of_sub_keys:
        # If the sub key doesnt exist then make an empty dict
        if not internal_dict_value.get(k, None):
            internal_dict_value[k] = {}
        internal_dict_value = internal_dict_value[k]


def set_opts(opts: dict, newopts: dict) -> dict:
    """
    Function to take a default dict and override it with newer values.

    # TODO: consider changing this to just a dict.update

    Args:
        opts: dictionary with default values
        newopts: dictionary with new values

    Returns:
        returns an updated dictionary
    """

    if newopts:
        for opt in newopts.keys():
            if opt in opts.keys():
                opts[opt] = newopts[opt]

    return opts


def flat() -> float:
    """
    Dummy distribution function that returns 1

    Returns:
        a flat uniform distribution: 1
    """

    return 1.0


def number(value: Union[int, float]) -> Union[int, float]:
    """
    Dummy distribution function that returns the input

    Args:
        value: the value that will be returned by this function.

    Returns:
        the value that was provided
    """

    return value


def const(
    min_bound: Union[int, float], max_bound: Union[int, float], val: float = None
) -> Union[int, float]:
    """
    a constant distribution function between min=min_bound and max=max_bound.

    Args:
        min_bound: lower bound of the range
        max_bound: upper bound of the range

    Returns:
            returns the value of 1/(max_bound-min_bound). If val is provided, it will check whether min_bound < val <= max_bound. if not: returns 0
    """

    if val:
        if not min_bound < val <= max_bound:
            print("out of bounds")
            prob = 0
            return prob
    prob = 1.0 / (max_bound - min_bound)
    return prob


@functools.lru_cache(maxsize=16)
def powerlaw_constant(
    min_val: Union[int, float], max_val: Union[int, float], k: Union[int, float]
) -> Union[int, float]:
    """
    Function that returns the constant to normalise a power law

    TODO: what if k is -1?

    Args:
        min_val: lower bound of the range
        max_val: upper bound of the range
        k: power law slope

    Returns:
        constant to normalise the given power law between the min_val and max_val range
    """

    k1 = k + 1.0
    # print(
    #     "Powerlaw consts from {} to {}, k={} where k1={}".format(
    #         min_val, max_val, k, k1
    #     )
    # )

    powerlaw_const = k1 / (max_val ** k1 - min_val ** k1)
    return powerlaw_const


def powerlaw(
    min_val: Union[int, float],
    max_val: Union[int, float],
    k: Union[int, float],
    x: Union[int, float],
) -> Union[int, float]:
    """
    Single power law with index k at x from min to max

    Args:
        min_val: lower bound of the power law
        max_val: upper bound of the power law
        k: slope of the power law
        x: position at which we want to evaluate

    Returns:
        `probability` at the given position(x)
    """

    # Handle faulty value
    if k == -1:
        msg = "wrong value for k"
        raise ValueError(msg)

    if (x < min_val) or (x > max_val):
        print("input value is out of bounds!")
        return 0

    powerlaw_const = powerlaw_constant(min_val, max_val, k)

    # power law
    prob = powerlaw_const * (x ** k)
    # print(
    #     "Power law from {} to {}: const = {}, y = {}".format(
    #         min_val, max_val, const, y
    #     )
    # )
    return prob


@functools.lru_cache(maxsize=16)
def calculate_constants_three_part_powerlaw(
    m0: Union[int, float],
    m1: Union[int, float],
    m2: Union[int, float],
    m_max: Union[int, float],
    p1: Union[int, float],
    p2: Union[int, float],
    p3: Union[int, float],
) -> Union[int, float]:
    """
    Function to calculate the constants for a three-part power law

    TODO: use the power law_constant function to calculate all these values

    Args:
        m0: lower bound mass
        m1: second boundary, between the first slope and the second slope
        m2: third boundary, between the second slope and the third slope
        m_max: upper bound mass
        p1: first slope
        p2: second slope
        p3: third slope

    Returns:
        array of normalisation constants
    """

    # print("Initialising constants for the three-part powerlaw: m0={} m1={} m2={}\
    # m_max={} p1={} p2={} p3={}\n".format(m0, m1, m2, m_max, p1, p2, p3))

    array_constants_three_part_powerlaw = [0, 0, 0]

    array_constants_three_part_powerlaw[1] = (
        ((m1 ** p2) * (m1 ** (-p1)))
        * (1.0 / (1.0 + p1))
        * (m1 ** (1.0 + p1) - m0 ** (1.0 + p1))
    )
    array_constants_three_part_powerlaw[1] += (
        (m2 ** (1.0 + p2) - m1 ** (1.0 + p2))
    ) * (1.0 / (1.0 + p2))
    array_constants_three_part_powerlaw[1] += (
        ((m2 ** p2) * (m2 ** (-p3)))
        * (1.0 / (1.0 + p3))
        * (m_max ** (1.0 + p3) - m2 ** (1.0 + p3))
    )
    array_constants_three_part_powerlaw[1] = 1.0 / (
        array_constants_three_part_powerlaw[1] + 1e-50
    )

    array_constants_three_part_powerlaw[0] = array_constants_three_part_powerlaw[1] * (
        (m1 ** p2) * (m1 ** (-p1))
    )
    array_constants_three_part_powerlaw[2] = array_constants_three_part_powerlaw[1] * (
        (m2 ** p2) * (m2 ** (-p3))
    )

    return array_constants_three_part_powerlaw
    # $$array[1]=(($m1**$p2)*($m1**(-$p1)))*
    # (1.0/(1.0+$p1))*
    # ($m1**(1.0+$p1)-$m0**(1.0+$p1))+
    # (($m2**(1.0+$p2)-$m1**(1.0+$p2)))*
    # (1.0/(1.0+$p2))+
    # (($m2**$p2)*($m2**(-$p3)))*
    # (1.0/(1.0+$p3))*
    # ($mmax**(1.0+$p3)-$m2**(1.0+$p3));
    # $$array[1]=1.0/($$array[1]+1e-50);
    # $$array[0]=$$array[1]*$m1**$p2*$m1**(-$p1);
    # $$array[2]=$$array[1]*$m2**$p2*$m2**(-$p3);
    # #print "ARRAY SET @_ => @$array\n";
    # $threepart_powerlaw_consts{"@_"}=[@$array];


def three_part_powerlaw(
    m: Union[int, float],
    m0: Union[int, float],
    m1: Union[int, float],
    m2: Union[int, float],
    m_max: Union[int, float],
    p1: Union[int, float],
    p2: Union[int, float],
    p3: Union[int, float],
) -> Union[int, float]:
    """
    Generalised three-part power law, usually used for mass distributions

    Args:
        m: mass at which we want to evaluate the distribution.
        m0: lower bound mass
        m1: second boundary, between the first slope and the second slope
        m2: third boundary, between the second slope and the third slope
        m_max: upper bound mass
        p1: first slope
        p2: second slope
        p3: third slope

    Returns:
        'probability' at given mass m
    """

    # TODO: add check on whether the values exist

    three_part_powerlaw_constants = calculate_constants_three_part_powerlaw(
        m0, m1, m2, m_max, p1, p2, p3
    )

    #
    if m < m0:
        prob = 0  # Below lower bound TODO: make this clear.
    elif m0 < m <= m1:
        prob = three_part_powerlaw_constants[0] * (m ** p1)  # Between M0 and M1
    elif m1 < m <= m2:
        prob = three_part_powerlaw_constants[1] * (m ** p2)  # Between M1 and M2
    elif m2 < m <= m_max:
        prob = three_part_powerlaw_constants[2] * (m ** p3)  # Between M2 and M_MAX
    else:
        prob = 0  # Above M_MAX

    return prob


@functools.lru_cache(maxsize=16)
def gaussian_normalizing_const(
    mean: Union[int, float],
    sigma: Union[int, float],
    gmin: Union[int, float],
    gmax: Union[int, float],
) -> Union[int, float]:
    """
    Function to calculate the normalisation constant for the Gaussian

    Args:
        mean: mean of the Gaussian
        sigma: standard deviation of the Gaussian
        gmin: lower bound of the range to calculate the probabilities in
        gmax: upper bound of the range to calculate the probabilities in

    Returns:
        normalisation constant for the Gaussian distribution(mean, sigma) between gmin and gmax
    """

    # First time; calculate multiplier for given mean and sigma
    ptot = 0
    resolution = 1000
    d = (gmax - gmin) / resolution

    for i in range(resolution):
        y = gmin + i * d
        ptot += d * gaussian_func(y, mean, sigma)

    # TODO: Set value in global
    return ptot


def gaussian_func(
    x: Union[int, float], mean: Union[int, float], sigma: Union[int, float]
) -> Union[int, float]:
    """
    Function to evaluate a Gaussian at a given point, but this time without any boundaries.

    Args:
        x: location at which to evaluate the distribution
        mean: mean of the Gaussian
        sigma: standard deviation of the Gaussian

    Returns:
        value of the Gaussian at x
    """
    gaussian_prefactor = 1.0 / math.sqrt(2.0 * math.pi)

    r = 1.0 / (sigma)
    y = (x - mean) * r
    return gaussian_prefactor * r * math.exp(-0.5 * y ** 2)


def gaussian(
    x: Union[int, float],
    mean: Union[int, float],
    sigma: Union[int, float],
    gmin: Union[int, float],
    gmax: Union[int, float],
) -> Union[int, float]:
    """
    Gaussian distribution function. used for e.g. Duquennoy + Mayor 1991

    Args:
        x: location at which to evaluate the distribution
        mean: mean of the Gaussian
        sigma: standard deviation of the Gaussian
        gmin: lower bound of the range to calculate the probabilities in
        gmax: upper bound of the range to calculate the probabilities in

    Returns:
        'probability' of the Gaussian distribution between the boundaries, evaluated at x
    """

    # # location (X value), mean and sigma, min and max range
    # my ($x,$mean,$sigma,$gmin,$gmax) = @_;

    if (x < gmin) or (x > gmax):
        prob = 0
    else:
        # normalise over given range
        # TODO: add loading into global var
        normalisation = gaussian_normalizing_const(mean, sigma, gmin, gmax)
        prob = gaussian_func(x, mean, sigma) / normalisation

    return prob


#####
# Mass distributions
#####


def Kroupa2001(m: Union[int, float], newopts: dict = None) -> Union[int, float]:
    """
    Probability distribution function for Kroupa 2001 IMF, where the default values to the
    three_part_powerlaw are: default = {"m0": 0.1, "m1": 0.5, "m2": 1, "mmax": 100, "p1": -1.3, "p2": -2.3,"p3": -2.3}

    Args:
        m: mass to evaluate the distribution at
        newopts: optional dict to override the default values.

    Returns:
        'probability' of distribution function evaluated at m
    """

    # Default parameters and override them
    default = {
        "m0": 0.1,
        "m1": 0.5,
        "m2": 1,
        "mmax": 100,
        "p1": -1.3,
        "p2": -2.3,
        "p3": -2.3,
    }

    value_dict = default.copy()

    if newopts:
        value_dict.update(newopts)

    return three_part_powerlaw(
        m,
        value_dict["m0"],
        value_dict["m1"],
        value_dict["m2"],
        value_dict["mmax"],
        value_dict["p1"],
        value_dict["p2"],
        value_dict["p3"],
    )


def ktg93(m: Union[int, float], newopts: dict = None) -> Union[int, float]:
    """
    Probability distribution function for KTG93 IMF, where the default values to the three_part_powerlaw are: default = {"m0": 0.1, "m1": 0.5, "m2": 1, "mmax": 80, "p1": -1.3, "p2": -2.2,"p3": -2.7}

    Args:
        m: mass to evaluate the distribution at
        newopts: optional dict to override the default values.

    Returns:
        'probability' of distribution function evaluated at m
    """
    # TODO: ask rob what this means

    # if($m eq 'uncertainties')
    # {
    # # return (pointer to) the uncertainties hash
    # return {
    #     m0=>{default=>0.1,
    #      fixed=>1},
    #     m1=>{default=>0.5,
    #      fixed=>1},
    #     m2=>{default=>1.0,
    #      fixed=>1},
    #     mmax=>{default=>80.0,
    #        fixed=>1},
    #     p1=>{default=>-1.3,
    #      low=>-1.3,
    #      high=>-1.3},
    #     p2=>{default=>-2.2,
    #      low=>-2.2,
    #      high=>-2.2},
    #     p3=>{default=>-2.7,
    #      low=>-2.7,
    #      high=>-2.7}
    # };
    # }

    # set options
    # opts = set_opts({'m0':0.1, 'm1':0.5, 'm2':1.0, 'mmax':80, 'p1':-1.3, 'p2':-2.2, 'p3':-2.7},
    # newopts)

    defaults = {
        "m0": 0.1,
        "m1": 0.5,
        "m2": 1.0,
        "mmax": 80,
        "p1": -1.3,
        "p2": -2.2,
        "p3": -2.7,
    }
    value_dict = defaults.copy()

    if newopts:
        value_dict.update(newopts)

    return three_part_powerlaw(
        m,
        value_dict["m0"],
        value_dict["m1"],
        value_dict["m2"],
        value_dict["mmax"],
        value_dict["p1"],
        value_dict["p2"],
        value_dict["p3"],
    )


# sub ktg93_lnspace
# {
#     # wrapper for KTG93 on a ln(m) grid
#     my $m=$_[0];
#     return ktg93(@_) * $m;
# }


def imf_tinsley1980(m: Union[int, float]) -> Union[int, float]:
    """
    Probability distribution function for Tinsley 1980 IMF (defined up until 80Msol): three_part_powerlaw(m, 0.1, 2.0, 10.0, 80.0, -2.0, -2.3, -3.3)

    Args:
        m: mass to evaluate the distribution at

    Returns:
        'probability' of distribution function evaluated at m
    """

    return three_part_powerlaw(m, 0.1, 2.0, 10.0, 80.0, -2.0, -2.3, -3.3)


def imf_scalo1986(m: Union[int, float]) -> Union[int, float]:
    """
    Probability distribution function for Scalo 1986 IMF (defined up until 80Msol): three_part_powerlaw(m, 0.1, 1.0, 2.0, 80.0, -2.35, -2.35, -2.70)

    Args:
        m: mass to evaluate the distribution at

    Returns:
        'probability' of distribution function evaluated at m
    """
    return three_part_powerlaw(m, 0.1, 1.0, 2.0, 80.0, -2.35, -2.35, -2.70)


def imf_scalo1998(m: Union[int, float]) -> Union[int, float]:
    """
    From Scalo 1998

    Probability distribution function for Scalo 1998 IMF (defined up until 80Msol): three_part_powerlaw(m, 0.1, 1.0, 10.0, 80.0, -1.2, -2.7, -2.3)

    Args:
        m: mass to evaluate the distribution at

    Returns:
        'probability' of distribution function evaluated at m
    """

    return three_part_powerlaw(m, 0.1, 1.0, 10.0, 80.0, -1.2, -2.7, -2.3)


def imf_chabrier2003(m: Union[int, float]) -> Union[int, float]:
    """
    Probability distribution function for IMF of Chabrier 2003 PASP 115:763-795

    Args:
        m: mass to evaluate the distribution at

    Returns:
        'probability' of distribution function evaluated at m
    """

    chabrier_logmc = math.log10(0.079)
    chabrier_sigma2 = 0.69 * 0.69
    chabrier_a1 = 0.158
    chabrier_a2 = 4.43e-2
    chabrier_x = -1.3
    if m <= 0:
        msg = "below bounds"
        raise ValueError(msg)
    if 0 < m < 1.0:
        A = 0.158
        dm = math.log10(m) - chabrier_logmc
        prob = chabrier_a1 * math.exp(-(dm ** 2) / (2.0 * chabrier_sigma2))
    else:
        prob = chabrier_a2 * (m ** chabrier_x)
    prob = prob / (0.1202462 * m * math.log(10))
    return prob


########################################################################
# Binary fractions
########################################################################


def Arenou2010_binary_fraction(m: Union[int, float]) -> Union[int, float]:
    """
    Arenou 2010 function for the binary fraction as f(M1)

    GAIA-C2-SP-OPM-FA-054
    www.rssd.esa.int/doc_fetch.php?id=2969346

    Args:
        m: mass to evaluate the distribution at

    Returns:
        binary fraction at m
    """

    return 0.8388 * math.tanh(0.688 * m + 0.079)


# print(Arenou2010_binary_fraction(0.4))


def raghavan2010_binary_fraction(m: Union[int, float]) -> Union[int, float]:
    """
    Fit to the Raghavan 2010 binary fraction as a function of
    spectral type (Fig 12). Valid for local stars (Z=Zsolar).

    The spectral type is converted  mass by use of the ZAMS
    effective temperatures from binary_c/BSE (at Z=0.02)
    and the new "long_spectral_type" function of binary_c
    (based on Jaschek+Jaschek's Teff-spectral type table).

    Rob then fitted the result

    Args:
        m: mass to evaluate the distribution at

    Returns:
        binary fraction at m
    """

    return min(
        1.0,
        max(
            (m ** 0.1) * (5.12310e-01) + (-1.02070e-01),
            (1.10450e00) * (m ** (4.93670e-01)) + (-6.95630e-01),
        ),
    )


# print(raghavan2010_binary_fraction(2))

########################################################################
# Period distributions
########################################################################


def duquennoy1991(logper: Union[int, float]) -> Union[int, float]:
    """
    Period distribution from Duquennoy + Mayor 1991. Evaluated the function gaussian(logper, 4.8, 2.3, -2, 12)

    Args:
        logper: logarithm of period to evaluate the distribution at

    Returns:
        'probability' at gaussian(logper, 4.8, 2.3, -2, 12)
    """
    return gaussian(logper, 4.8, 2.3, -2, 12)


def sana12(
    M1: Union[int, float],
    M2: Union[int, float],
    a: Union[int, float],
    P: Union[int, float],
    amin: Union[int, float],
    amax: Union[int, float],
    x0: Union[int, float],
    x1: Union[int, float],
    p: Union[int, float],
) -> Union[int, float]:
    """
    distribution of initial orbital periods as found by Sana et al. (2012)
    which is a flat distribution in ln(a) and ln(P) respectively for stars
    * less massive than 15Msun (no O-stars)
    * mass ratio q=M2/M1<0.1
    * log(P)<0.15=x0 and log(P)>3.5=x1
    and is be given by dp/dlogP ~ (logP)^p for all other binary configurations (default p=-0.55)

    arguments are M1, M2, a, Period P, amin, amax, x0=log P0, x1=log P1, p

    example args: 10, 5, sep(M1, M2, P), sep, ?, -2, 12, -0.55

    # TODO: Fix this function!

    Args:
        M1: Mass of primary
        M2: Mass of secondary
        a: separation of binary
        P: period of binary
        amin: minimum separation of the distribution (lower bound of the range)
        amax: maximum separation of the distribution (upper bound of the range)
        x0: log of minimum period of the distribution (lower bound of the range)
        x1: log of maximum period of the distribution (upper bound of the range)
        p: slope of the distribution

    Returns:
        'probability' of orbital period P given the other parameters
    """

    res = 0
    if (M1 < 15.0) or (M2 / M1 < 0.1):
        res = 1.0 / (math.log(amax) - math.log(amin))
    else:
        p1 = 1.0 + p

        # For more details see the LyX document of binary_c for this distribution
        # where the variables and normalisations are given
        # we use the notation x=log(P), xmin=log(Pmin), x0=log(P0), ... to determine the
        x = LOG_LN_CONVERTER * math.log(P)
        xmin = LOG_LN_CONVERTER * math.log(calc_period_from_sep(M1, M2, amin))
        xmax = LOG_LN_CONVERTER * math.log(calc_period_from_sep(M1, M2, amax))

        # print("M1 M2 amin amax P x xmin xmax")
        # print(M1, M2, amin, amax, P, x, xmin, xmax)
        # my $x0 = 0.15;
        # my $x1 = 3.5;

        A1 = 1.0 / (
            x0 ** p * (x0 - xmin) + (x1 ** p1 - x0 ** p1) / p1 + x1 ** p * (xmax - x1)
        )
        A0 = A1 * x0 ** p
        A2 = A1 * x1 ** p

        if x < x0:
            res = 3.0 / 2.0 * LOG_LN_CONVERTER * A0
        elif x > x1:
            res = 3.0 / 2.0 * LOG_LN_CONVERTER * A2
        else:
            res = 3.0 / 2.0 * LOG_LN_CONVERTER * A1 * x ** p

    return res


# print(sana12(10, 2, 10, 100, 1, 1000, math.log(10), math.log(1000), 6))


def interpolate_in_mass_izzard2012(
    M: Union[int, float], high: Union[int, float], low: Union[int, float]
) -> Union[int, float]:
    """
    Function to interpolate in mass

    TODO: fix this function.
    TODO: describe the args
    high: at M=16.3
    low: at 1.15

    Args:
        M: mass
        high:
        low:

    Returns:

    """

    log_interpolation = False

    if log_interpolation:
        return (high - low) / (math.log10(16.3) - math.log10(1.15)) * (
            math.log10(M) - math.log10(1.15)
        ) + low
    else:
        return (high - low) / (16.3 - 1.15) * (M - 1.15) + low


def Izzard2012_period_distribution(
    P: Union[int, float], M1: Union[int, float], log10Pmin: Union[int, float] = -1.0
) -> Union[int, float]:
    """
    period distribution which interpolates between
    Duquennoy and Mayor 1991 at low mass (G/K spectral type <~1.15Msun)
    and Sana et al 2012 at high mass (O spectral type >~16.3Msun)

    This gives dN/dlogP, i.e. DM/Raghavan's Gaussian in log10P at low mass
    and Sana's power law (as a function of logP) at high mass

    TODO: fix this function

    Args:
        P: period
        M1: Primary star mass
        log10Pmin: minimum period in base log10 (optional)

    Returns:
        'probability' of interpolated distribution function at P and M1

    """

    # Check if there is input and force it to be at least 1
    log10Pmin = max(-1.0, log10Pmin)

    # save mass input and limit mass used (M1 from now on) to fitted range
    Mwas = M1
    M1 = max(1.15, min(16.3, M1))
    # print("Izzard2012 called for M={} (truncated to {}), P={}\n".format(Mwas, M1, P))

    # Calculate the normalisations
    # need to normalise the distribution for this mass
    # (and perhaps secondary mass)
    prepare_dict(distribution_constants, ["Izzard2012", M1])
    if not distribution_constants["Izzard2012"][M1].get(log10Pmin):
        distribution_constants["Izzard2012"][M1][
            log10Pmin
        ] = 1  # To prevent this loop from going recursive
        N = 200.0  # Resolution for normalisation. I hope 1000 is enough
        dlP = (10.0 - log10Pmin) / N
        C = 0  # normalisation constant.
        # print("LOOP",log10Pmin)
        for lP in np.arange(log10Pmin, 10, dlP):
            C += dlP * Izzard2012_period_distribution(10 ** lP, M1, log10Pmin)

        distribution_constants["Izzard2012"][M1][log10Pmin] = 1.0 / C
        # print(
        # "Normalisation constant for Izzard2012 M={} (log10Pmin={}) is\
        # {}\n".format(
        #     M1, log10Pmin, distribution_constants["Izzard2012"][M1][log10Pmin]
        # )
        # )

    lP = math.log10(P)
    # log period

    # # fits
    mu = interpolate_in_mass_izzard2012(M1, -17.8, 5.03)
    sigma = interpolate_in_mass_izzard2012(M1, 9.18, 2.28)
    K = interpolate_in_mass_izzard2012(M1, 6.93e-2, 0.0)
    nu = interpolate_in_mass_izzard2012(M1, 0.3, -1)
    g = 1.0 / (1.0 + 1e-30 ** (lP - nu))

    lPmu = lP - mu
    # print(
    #     "M={} ({}) P={} : mu={} sigma={} K={} nu={} norm=%g\n".format(
    #         Mwas, M1, P, mu, sigma, K, nu
    #     )
    # )

    # print "FUNC $distdata{Izzard2012}{$M}{$log10Pmin} * (exp(- (x-$mu)**2/(2.0*$sigma*$sigma) ) + $K/MAX(0.1,$lP)) * $g;\n";

    if (lP < log10Pmin) or (lP > 10.0):
        return 0

    else:
        return (
            distribution_constants["Izzard2012"][M1][log10Pmin]
            * (math.exp(-lPmu * lPmu / (2.0 * sigma * sigma)) + K / max(0.1, lP))
            * g
        )


########################################################################
# Mass ratio distributions
########################################################################


def flatsections(x: float, opts: dict) -> Union[float, int]:
    """
    Function to generate flat distributions, possibly in multiple sections

    Args:
        x: mass ratio value
        opts: list containing the flat sections. Which are themselves dictionaries, with keys "max": upper bound, "min": lower bound and "height": value

    Returns:
        probability of that mass ratio.
    """

    c = 0
    y = 0

    for opt in opts:
        dc = (opt["max"] - opt["min"]) * opt["height"]
        # print("added flatsection ({}-{})*{} = {}\n".format(
        #   opt['max'], opt['min'], opt['height'], dc))
        c += dc
        if opt["min"] <= x <= opt["max"]:
            y = opt["height"]
            # print("Use this\n")

    c = 1.0 / c
    y = y * c

    # print("flatsections gives C={}: y={}\n",c,y)
    return y


# print(flatsections(1, [{'min': 0, 'max': 2, 'height': 3}]))

########################################################################
# Eccentricity distributions
########################################################################

########################################################################
# Star formation histories
########################################################################


def cosmic_SFH_madau_dickinson2014(z):
    """
    Cosmic star formation history distribution from Madau & Dickonson 2014 (https://arxiv.org/pdf/1403.0007.pdf)

    Args:
        z: redshift

    Returns:
        Cosmic star formation rate in Solar mass year^-1 mega parsec^-3
    """

    CSFH = 0.015 * ((1 + z) ** 2.7) / (1 + (((1 + z) / 2.9) ** 5.6))

    return CSFH


########################################################################
# Metallicity distributions
########################################################################


########################################################################
# Moe & DiStefano 2017 functions
#
# The code below are functions that are used to set up and interpolate
# on the Moe & DiStefano 2017 data. The interpolators take the last
# known value if we try to interpolate outside of the tables.
# There are still some open tasks and improvements that can be made:
#
# TODO: Solve the memory issues that are present.
#    Are the interpolators not cleaned?
# TODO: Parallelize the setting up of the interpolators
# TODO: Generalise the code such that we can input other/newer tables

########################################################################

import py_rinterpolate

# Global dictionary to store values in
Moecache = {}


def poisson(lambda_val, n, nmax=None, verbosity=0):
    """
    Function that calculates the Poisson value and normalises
    TODO: improve the description
    """

    cachekey = "{} {} {}".format(lambda_val, n, nmax)

    if distribution_constants.get("poisson_cache", None):
        if distribution_constants["poisson_cache"].get(cachekey, None):
            p_val = distribution_constants["poisson_cache"][cachekey]

            verbose_print(
                "\tMoe and di Stefano 2017: found cached value for poisson({}, {}, {}): {}".format(
                    lambda_val, n, nmax, p_val
                ),
                verbosity,
                _MOE2017_VERBOSITY_LEVEL,
            )

            return p_val

    # Poisson distribution : note, n can be zero
    #
    # nmax is the truncation : if set, we normalise
    # correctly.
    p_val = _poisson(lambda_val, n)

    if nmax:
        I_poisson = 0
        for i in range(nmax + 1):
            I_poisson += _poisson(lambda_val, i)
        p_val = p_val / I_poisson

    # Add to cache
    if not distribution_constants.get("poisson_cache", None):
        distribution_constants["poisson_cache"] = {}
    distribution_constants["poisson_cache"][cachekey] = p_val

    verbose_print(
        "\tMoe and di Stefano 2017: Poisson({}, {}, {}): {}".format(
            lambda_val, n, nmax, p_val
        ),
        verbosity,
        _MOE2017_VERBOSITY_LEVEL,
    )
    return p_val


def _poisson(lambda_val, n):
    """
    Function to return the Poisson value
    """

    return (lambda_val ** n) * np.exp(-lambda_val) / (1.0 * math.factorial(n))


def get_max_multiplicity(multiplicity_array):
    """
    Function to get the maximum multiplicity
    """

    max_multiplicity = 0
    for n in range(4):
        if multiplicity_array[n] > 0:
            max_multiplicity = n + 1
    return max_multiplicity


def merge_multiplicities(result_array, max_multiplicity, verbosity=0):
    """
    Function to fold the multiplicities higher than the max_multiplicity onto the max_multiplicity

    if max_multiplicity == 1:
        All the multiplicities are folded onto multiplicity == 1. This will always total to 1
    if max_multiplicity == 2:
        The multiplicity fractions of the triple and quadruples are folded onto that of the binary multiplicity fraction
    if max_multiplicity == 3:
        The multiplicity fractions of the quadruples are folded onto that of the triples
    """

    if not max_multiplicity in range(1, 5):
        msg = "\tMoe and di Stefano 2017: merge_multiplicities: max_multiplicity has to be between 1 and 4. It is {} now".format(
            max_multiplicity
        )
        verbose_print(
            msg,
            verbosity,
            0,
        )
        raise ValueError(msg)

    # Fold multiplicities:
    verbose_print(
        "\tMoe and di Stefano 2017: merge_multiplicities: Merging multiplicities with initial array {} and max multiplicity {}".format(
            result_array, max_multiplicity
        ),
        verbosity,
        _MOE2017_VERBOSITY_LEVEL,
    )
    for i in range(max_multiplicity, len(result_array))[::-1]:
        result_array[i - 1] += result_array[i]
        result_array[i] = 0
    verbose_print(
        "\tMoe and di Stefano 2017: merge_multiplicities: Merging multiplicities to new array {}".format(
            result_array
        ),
        verbosity,
        _MOE2017_VERBOSITY_LEVEL,
    )

    return result_array


def normalize_dict(result_dict, verbosity=0):
    """
    Function to normalise a dictionary
    """

    sum_result = sum([result_dict[key] for key in result_dict.keys()])
    for key in result_dict.keys():
        result_dict[key] = result_dict[key] / sum_result
    return result_dict


def Moe_di_Stefano_2017_multiplicity_fractions(options, verbosity=0):
    """
    Function that creates a list of probability fractions and
    normalises and merges them according to the users choice.

    TODO: make an extrapolation functionality in this. log10(1.6e1)
    is low, we can probably go a bit further

    The default result that is returned when sampling the mass outside
    of the mass range is now the last known value

    Returns a list of multiplicity fractions for a given input of mass
    """

    # Use the global Moecache
    global Moecache

    multiplicity_modulator_array = np.array(
        options["multiplicity_modulator"]
    )  # Modulator array

    # Check for length
    if not len(multiplicity_modulator_array) == 4:
        msg = "Multiplicity modulator has to have 4 elements. Now it is {}, len: {}".format(
            multiplicity_modulator_array, len(multiplicity_modulator_array)
        )
        verbose_print(
            msg,
            verbosity,
            0,
        )
        raise ValueError(msg)

    # Set up some arrays
    full_fractions_array = np.zeros(4)  # Meant to contain the real fractions
    weighted_fractions_array = np.zeros(
        4
    )  # Meant to contain the fractions multiplied by the multiplicity modulator

    # Get max multiplicity
    max_multiplicity = get_max_multiplicity(multiplicity_modulator_array)

    # ... it's better to interpolate the multiplicity and then
    # use a Poisson distribution to calculate the fractions
    # (this is more accurate)

    # Set up the multiplicity interpolator
    if not Moecache.get("rinterpolator_multiplicity", None):
        Moecache["rinterpolator_multiplicity"] = py_rinterpolate.Rinterpolate(
            table=Moecache["multiplicity_table"],  # Contains the table of data
            nparams=1,  # logM1
            ndata=4,  # The number of datapoints (the parameters that we want to interpolate)
            verbosity=verbosity - (_MOE2017_VERBOSITY_INTERPOLATOR_LEVEL - 1),
        )

    if options["multiplicity_model"] == "Poisson":
        multiplicity = Moecache["rinterpolator_multiplicity"].interpolate(
            [np.log10(options["M_1"])]
        )[0]

        # Fill the multiplicity array
        for n in range(4):
            full_fractions_array[n] = poisson(multiplicity, n, 3, verbosity)

        # Normalize it so it fills to one when taking all the multiplicities:
        full_fractions_array = full_fractions_array / np.sum(full_fractions_array)

        verbose_print(
            "\tMoe and di Stefano 2017: Moe_di_Stefano_2017_multiplicity_fractions: using model {}: full_fractions_array: {}".format(
                "Poisson", full_fractions_array
            ),
            verbosity,
            _MOE2017_VERBOSITY_LEVEL,
        )

    elif options["multiplicity_model"] == "data":
        # use the fractions calculated from Moe's data directly
        #
        # note that in this case, there are no quadruples: these
        # are combined with triples

        # Fill with the raw values
        for n in range(3):
            full_fractions_array[n] = Moecache[
                "rinterpolator_multiplicity"
            ].interpolate([np.log10(options["M_1"])])[n + 1]

        # Set last value
        full_fractions_array[3] = 0.0  # no quadruples
        verbose_print(
            "\tMoe and di Stefano 2017: Moe_di_Stefano_2017_multiplicity_fractions: using model {}: full_fractions_array: {}".format(
                "data", full_fractions_array
            ),
            verbosity,
            _MOE2017_VERBOSITY_LEVEL,
        )

    # Normalisation:
    if options["normalize_multiplicities"] == "raw":
        # Don't multiply by the multiplicity_array, but do give a fractions array
        verbose_print(
            "\tMoe and di Stefano 2017: Moe_di_Stefano_2017_multiplicity_fractions: Not normalising (using raw results): results: {}".format(
                full_fractions_array
            ),
            verbosity,
            _MOE2017_VERBOSITY_LEVEL,
        )
        result = full_fractions_array

    elif options["normalize_multiplicities"] == "norm":
        # Multiply the full_multiplicity_fraction array by the multiplicity_multiplier_array, creating a weighted fractions array
        weighted_fractions_array = full_fractions_array * multiplicity_modulator_array

        # Normalise this so it is in total 1:
        result = weighted_fractions_array / np.sum(weighted_fractions_array)

        verbose_print(
            "\tMoe and di Stefano 2017: Moe_di_Stefano_2017_multiplicity_fractions: Normalising with {}. result: {}".format(
                "norm", result
            ),
            verbosity,
            _MOE2017_VERBOSITY_LEVEL,
        )

    elif options["normalize_multiplicities"] == "merge":
        # We first take the full multiplicity array
        # (i.e. not multiplied by multiplier) and do the merging
        result = merge_multiplicities(
            full_fractions_array, max_multiplicity, verbosity=verbosity
        )

        # Then normalise to be sure
        result = result / np.sum(result)

        verbose_print(
            "\tMoe and di Stefano 2017: Moe_di_Stefano_2017_multiplicity_fractions: Normalising with {}, max_multiplicity={} result={}".format(
                "merge", max_multiplicity, result
            ),
            verbosity,
            _MOE2017_VERBOSITY_LEVEL,
        )

    verbose_print(
        "\tMoe and di Stefano 2017: Moe_di_Stefano_2017_multiplicity_fractions: {}".format(
            str(result)
        ),
        verbosity,
        _MOE2017_VERBOSITY_LEVEL,
    )

    # return array reference
    return result


def build_q_table(options, m, p, verbosity=0):
    ############################################################
    #
    # Build an interpolation table for q, given a mass and
    # orbital period.
    #
    # $m and $p are labels which determine which system(s)
    # to look up from Moe's data:
    #
    # $m can be M1, M2, M3, M4, or if set M1+M2 etc.
    # $p can be P, P2, P3
    #
    # The actual values are in $opts:
    #
    # mass is in $opts->{$m}
    # period is  $opts->{$p}
    #
    # Since the information from the table for Moe and di Stefano 2017 is independent of any choice we make,
    # we need to take into account that for example our choice of minimum mass leads to
    # a minimum q_min that is not the same as in the table
    # We should ignore those parts of the table and renormalise.
    # If we are below the lowest value of qmin in the table we need to extrapolate the data
    #
    # Anyway, the goal of this function is to provide some extrapolated values for q when we should sample outside of the boundaries
    ############################################################

    # We can check if we have a cached value for this already:
    # TODO: fix this cache check.
    incache = False
    if Moecache.get("rinterpolator_q_metadata", None):
        if (Moecache["rinterpolator_q_metadata"].get(m, None)) and (
            Moecache["rinterpolator_q_metadata"].get(p, None)
        ):
            if (Moecache["rinterpolator_q_metadata"][m] == options[m]) and (
                Moecache["rinterpolator_q_metadata"][p] == options[p]
            ):
                incache = True

                verbose_print(
                    "\tMoe and di Stefano 2017: build_q_table: Found cached values for m={} p={}".format(
                        options[m], options[p]
                    ),
                    verbosity,
                    _MOE2017_VERBOSITY_LEVEL,
                )
            else:
                verbose_print(
                    "\tMoe and di Stefano 2017: build_q_table: Cached values for different m={} p={}. Freeing current table and making new table".format(
                        options[m], options[p]
                    ),
                    verbosity,
                    _MOE2017_VERBOSITY_LEVEL,
                )

    #
    if not incache:
        # trim and/or expand the table to the range $qmin to $qmax.

        # qmin is set by the minimum stellar mass : below this
        # the companions are planets
        # qmin = options["ranges"]["M"][
        #     0
        # ]  # TODO: this lower range must not be lower than Mmin.

        qmin = options["Mmin"] / options["M_1"]
        verbose_print(
            "\tMoe and di Stefano 2017: build_q_table qmin: {}".format(
                qmin,
            ),
            verbosity,
            _MOE2017_VERBOSITY_LEVEL,
        )

        # qmax = maximum_mass_ratio_for_RLOF(options[m], options[p])
        # TODO: change this to the above
        qmax = 1

        # qdata contains the table that we modify: we get
        # the original data by interpolating Moe's table
        qdata = {}
        can_renormalize = 1

        qeps = 1e-8  # small number but such that qeps+1 != 1
        if qeps + 1 == 1.0:
            verbose_print(
                "\tMoe and di Stefano 2017: build_q_table: qeps (= {}) +1 == 1. Make qeps larger".format(
                    qeps,
                ),
                verbosity,
                _MOE2017_VERBOSITY_LEVEL,
            )

        if qmin >= qmax:
            # there may be NO binaries in this part of the parameter space:
            # in which case, set up a table with lots of zero in it

            qdata = {0: 0, 1: 0}
            can_renormalize = 0

        else:
            # qmin and qmax mean we'll get something non-zero
            can_renormalize = 1

            # require extrapolation sets whether we need to extrapolate
            # at the low and high ends
            require_extrapolation = {}

            if qmin >= 0.15:
                # qmin is inside Moe's table : this is easy,
                # we just keep points from qmin at the low
                # end to qmax at the high end.
                require_extrapolation["low"] = 0
                require_extrapolation[
                    "high"
                ] = 1  # TODO: shouldn't the extrapolation need to happen if qmax > 0.95
                qdata[qmin] = Moecache["rinterpolator_q"].interpolate(
                    [np.log10(options[m]), np.log10(options[p]), qmin]
                )[0]

                for q in np.arange(0.15, 0.950001, 0.1):
                    if (q >= qmin) and (q <= qmax):
                        qdata[q] = Moecache["rinterpolator_q"].interpolate(
                            [np.log10(options[m]), np.log10(options[p]), q]
                        )[0]
            else:
                require_extrapolation["low"] = 1
                require_extrapolation["high"] = 1
                if qmax < 0.15:
                    # qmax < 0.15 which is off the edge
                    # of the table. In this case, choose
                    # two points at q=0.15 and 0.16 and interpolate
                    # at these in case we want to extrapolate.
                    for q in [0.15, 0.16]:
                        qdata[q] = Moecache["rinterpolator_q"].interpolate(
                            [np.log10(options[m]), np.log10(options[p]), q]
                        )[0]
                else:
                    # qmin < 0.15 and qmax > 0.15, so we
                    # have to generate Moe's table for
                    # q = 0.15 (i.e. 0.1 to 0.2) to 0.95 (0.9 to 1)
                    # as a function of M1 and orbital period,
                    # to obtain the q distribution data.

                    for q in np.arange(0.15, np.min([0.950001, qmax + 0.0001]), 0.1):
                        val = Moecache["rinterpolator_q"].interpolate(
                            [np.log10(options[m]), np.log10(options[p]), q]
                        )[0]
                        qdata[q] = val

                # just below qmin, if qmin>qeps, we want nothing
                if qmin - 0.15 > qeps:
                    q = qmin - qeps
                    qdata[q] = 0
                    require_extrapolation["low"] = 0

            # just above qmax, if qmax<1, we want nothing
            if qmax < 0.95:
                q = qmax + qeps
                qdata[q] = 0
                require_extrapolation["high"] = 0

            # sorted list of qs
            qs = sorted(qdata.keys())

            if len(qs) == 0:
                msg = "No qs found error"
                raise ValueError(msg)

            elif len(qs) == 1:
                # only one q value : pretend there are two
                # with a flat distribution up to 1.0.
                if qs[0] == 1.0:
                    qs[0] = 1.0 - 1e-6
                    qs.append(1)
                    qdata[qs[0]] = 1
                    qdata[qs[1]] = 1
                else:
                    qs.append(1)
                    qdata[qs[1]] = qs[0]

            # We actually should do the extrapolation now.
            else:
                # Loop over both the lower end and the upper end
                for pre in ["low", "high"]:
                    if require_extrapolation[pre] == 0:
                        continue
                    else:
                        sign = -1 if pre == "low" else 1
                        end_index = 0 if pre == "low" else len(qs) - 1
                        indices = (
                            [0, 1] if pre == "low" else [len(qs) - 1, len(qs) - 2]
                        )  # Based on whether we do the high or low end we need to use two different indices
                        method = options.get(
                            "q_{}_extrapolation_method".format(pre), None
                        )
                        qlimit = qmin if pre == "low" else qmax

                        verbose_print(
                            "\tMoe and di Stefano 2017: build_q_table: Extrapolating: Q: {} method: {}, indices: {} End index: {}".format(
                                pre, method, indices, end_index
                            ),
                            verbosity,
                            _MOE2017_VERBOSITY_LEVEL,
                        )

                        # truncate the distribution
                        qdata[max(0.0, min(1.0, qlimit + sign * qeps))] = 0

                        if method == None:
                            # no extrapolation : just interpolate between 0.10 and 0.95
                            verbose_print(
                                "\tMoe and di Stefano 2017: build_q_table: using no extrapolations".format(),
                                verbosity,
                                _MOE2017_VERBOSITY_LEVEL,
                            )
                            continue
                        elif method == "flat":
                            # use the end value and extrapolate it
                            # with zero slope
                            qdata[qlimit] = qdata[qs[end_index]]
                            verbose_print(
                                "\tMoe and di Stefano 2017: build_q_table: using constant extrapolation".format(),
                                verbosity,
                                _MOE2017_VERBOSITY_LEVEL,
                            )
                        elif method == "linear":
                            qdata[qlimit] = linear_extrapolation_q(
                                qs=qs,
                                indices=indices,
                                qlimit=qlimit,
                                qdata=qdata,
                                end_index=end_index,
                                verbosity=verbosity,
                            )

                            verbose_print(
                                "\tMoe and di Stefano 2017: build_q_table: using linear extrapolation".format(),
                                verbosity,
                                _MOE2017_VERBOSITY_LEVEL,
                            )
                            if pre == "low":
                                below_qlimit = qlimit - qeps
                                if below_qlimit > 0:
                                    qdata[below_qlimit] = 0
                                qdata[0] = 0
                                verbose_print(
                                    "\tMoe and di Stefano 2017: build_q_table: using linear extrapolation and setting the points below the lower q bound ({}) to 0 ".format(
                                        qlimit
                                    ),
                                    verbosity,
                                    _MOE2017_VERBOSITY_LEVEL,
                                )

                        elif method == "plaw2":
                            qdata[qlimit] = powerlaw_extrapolation_q(
                                qs=qs, indices=indices, qdata=qdata, verbosity=verbosity
                            )

                            verbose_print(
                                "\tMoe and di Stefano 2017: build_q_table: using powerlaw extrapolation".format(),
                                verbosity,
                                _MOE2017_VERBOSITY_LEVEL,
                            )
                        elif method == "nolowq":
                            newq = 0.05
                            qdata[newq] = 0
                            verbose_print(
                                "\tMoe and di Stefano 2017: build_q_table: setting lowq to 0".format(),
                                verbosity,
                                _MOE2017_VERBOSITY_LEVEL,
                            )
                        elif method == "poly":
                            # TODO: consider implementing the poly method (see Perl version)
                            raise ValueError(
                                "Moe and di Stefano 2017: build_q_table: Method 'poly' not implemented"
                            )

                        else:
                            msg = "\tMoe and di Stefano 2017: build_q_table: Error no other methods available. The chosen method ({}) does not exist!".format(
                                method
                            )
                            verbose_print(
                                msg,
                                verbosity,
                                _MOE2017_VERBOSITY_LEVEL,
                            )
                            raise ValueError(msg)

        # regenerate qs in new table. This is now the updated list of qs where we have some extrapolated numbers
        tmp_table = []
        for q in sorted(qdata.keys()):
            tmp_table.append([q, qdata[q]])

        # Make an interpolation table to contain our modified data
        q_interpolator = py_rinterpolate.Rinterpolate(
            table=tmp_table,
            nparams=1,
            ndata=1,  # Contains the table of data  # q  #
            verbosity=verbosity - (_MOE2017_VERBOSITY_INTERPOLATOR_LEVEL - 1),
        )
        verbose_print(
            "\tMoe and di Stefano 2017: build_q_table: Created a new Q table",
            verbosity,
            _MOE2017_VERBOSITY_LEVEL,
        )

        if can_renormalize:
            verbose_print(
                "\tMoe and di Stefano 2017: build_q_table: Renormalising table",
                verbosity,
                _MOE2017_VERBOSITY_LEVEL,
            )

            # now we integrate and renormalise (if the table is not all zero)
            I = get_integration_constant_q(
                q_interpolator, tmp_table, qdata, verbosity=verbosity
            )

            if I > 0:
                # normalise to 1.0 by dividing the data by 1.0/$I
                q_interpolator.multiply_table_column(1, 1.0 / I)

                # test this
                new_I = get_integration_constant_q(
                    q_interpolator, tmp_table, qdata, verbosity=verbosity
                )

                # fail if error in integral > 1e-6 (should be ~ machine precision)
                if abs(1.0 - new_I) > 1e-6:
                    verbose_print(
                        "\tMoe and di Stefano 2017: build_q_table: Error: > 1e-6 in q probability integral: {}".format(
                            I
                        ),
                        verbosity,
                        _MOE2017_VERBOSITY_LEVEL,
                    )
        # set this new table in the cache
        Moecache["rinterpolator_q_given_{}_log10{}".format(m, p)] = q_interpolator
        verbose_print(
            "\tMoe and di Stefano 2017: build_q_table: stored q_interpolater as {}".format(
                "rinterpolator_q_given_{}_log10{}".format(m, p)
            ),
            verbosity,
            _MOE2017_VERBOSITY_LEVEL,
        )

        # Store the values for which this table was set up in the dict
        if not Moecache.get("rinterpolator_q_metadata", None):
            Moecache["rinterpolator_q_metadata"] = {}
        Moecache["rinterpolator_q_metadata"][m] = options[m]
        Moecache["rinterpolator_q_metadata"][p] = options[p]


def powerlaw_extrapolation_q(qdata, qs, indices, verbosity=0):
    """
    Function to do the power law extrapolation at the lower end of the q range
    """
    newq = 0.05

    # use a power-law extrapolation down to q=0.05, if possible
    if (qdata[qs[indices[0]]] == 0.0) and (qdata[qs[indices[1]]] == 0.0):
        # not possible
        return 0

    else:
        slope = (np.log10(qdata[qs[indices[1]]]) - np.log10(qdata[qs[indices[0]]])) / (
            np.log10(qs[indices[1]]) - np.log10(qs[indices[0]])
        )
        intercept = np.log10(qdata[qs[indices[0]]]) - slope * np.log10(qs[indices[0]])

        return slope * newq + intercept


def linear_extrapolation_q(qs, indices, qlimit, qdata, end_index, verbosity=0):
    """
    Function to do the linear extrapolation for q.
    """

    # linear extrapolation
    dq = qs[indices[1]] - qs[indices[0]]

    if dq == 0:
        verbose_print(
            "\tMoe and di Stefano 2017: build_q_table: linear dq=0".format(),
            verbosity,
            _MOE2017_VERBOSITY_LEVEL,
        )
        # No change
        return qs[end_index]
    else:
        slope = (qdata[qs[indices[1]]] - qdata[qs[indices[0]]]) / dq

        intercept = qdata[qs[indices[0]]] - slope * qs[indices[0]]
        qdata[qlimit] = max(0.0, slope * qlimit + intercept)
        verbose_print(
            "\tMoe and di Stefano 2017: build_q_table: linear Slope: {} intercept: {} dn/dq({}) = {}".format(
                slope, intercept, qlimit, qdata[qlimit]
            ),
            verbosity,
            _MOE2017_VERBOSITY_LEVEL,
        )
    return max(0.0, slope * qlimit + intercept)


def get_integration_constant_q(q_interpolator, tmp_table, qdata, verbosity=0):
    """
    Function to integrate the q interpolator and return the integration constant
    """

    dq = 1e-3  # resolution of the integration/renormalisation
    I = 0

    # integrate: note that the value of the integral is
    # meaningless to within a factor (which depends on $dq)
    for q in np.arange(0, 1 + 2e-6, dq):
        x = q_interpolator.interpolate([q])
        if len(x) == 0:
            msg = "\tMoe and di Stefano 2017: build_q_table: Q interpolator table interpolation failed.\n\t\ttmp_table = {}\n\t\tq_data = {}".format(
                str(tmp_table), str(qdata)
            )
            verbose_print(
                msg,
                verbosity,
                _MOE2017_VERBOSITY_LEVEL,
            )
            raise ValueError(msg)
        else:
            I += x[0] * dq
            # verbose_print(
            #     "\tMoe and di Stefano 2017: build_q_table: dn/dq ({}) = {} I -> = {}".format(q, x[0], I),
            #     verbosity,
            #     _MOE2017_VERBOSITY_LEVEL,
            # )
    return I


def fill_data(sample_values, data_dict):
    """
    Function that returns the normalised array of values for given logmass and logperiod
    used for the e and q values

    TODO: make sure we do the correct thing with the dstep
    """

    data = {}
    I = 0

    dstep = float(sample_values[1]) - float(sample_values[0])

    # Read out the data
    for sample_value in sample_values:
        val = data_dict[sample_value]
        data[sample_value] = val
        I += val

    # Normalise the data
    for sample_value in sample_values:
        data[sample_value] = data[sample_value] / I

    return data


def calc_e_integral(
    options,
    integrals_string,
    interpolator_name,
    mass_string,
    period_string,
    verbosity=0,
):
    """
    Function to calculate the P integral

    We need to renormalise this because min_per > 0, and not all periods should be included
    """

    global Moecache
    min_ecc = 0
    max_ecc = 0.9999

    mass_period_string = "{}_{}".format(options[mass_string], options[period_string])

    # Check if the dict exists
    if not Moecache.get(integrals_string, None):
        Moecache[integrals_string] = {}

    # Check for cached value. If it doesn't exist: calculate
    if not Moecache[integrals_string].get(mass_period_string, None):
        I = 0
        decc = 1e-3

        for ecc in np.arange(min_ecc, max_ecc, decc):
            # Loop over all the values in the table, between the min and max P
            dp_decc = Moecache[interpolator_name].interpolate(
                [np.log10(options[mass_string]), np.log10(options[period_string]), ecc]
            )[0]

            I += dp_decc * decc

        # Set the integral value in the dict
        Moecache[integrals_string][mass_period_string] = I
        verbose_print(
            "\tMoe and di Stefano 2017: calc_ecc_integral: min_ecc: {} max ecc: {} integrals_string: {} interpolator_name: {} mass_string: {} period_string: {} mass: {} period: {} I: {}".format(
                min_ecc,
                max_ecc,
                integrals_string,
                interpolator_name,
                mass_string,
                period_string,
                options[mass_string],
                options[period_string],
                I,
            ),
            verbosity,
            _MOE2017_VERBOSITY_LEVEL,
        )
    else:
        verbose_print(
            "\tMoe and di Stefano 2017: calc_ecc_integral: Found cached value for min_ecc: {} max ecc: {} integrals_string: {} interpolator_name: {} mass_string: {} period_string: {} mass: {} period: {} I: {}".format(
                min_ecc,
                max_ecc,
                integrals_string,
                interpolator_name,
                mass_string,
                period_string,
                options[mass_string],
                options[period_string],
                Moecache[integrals_string][mass_period_string],
            ),
            verbosity,
            _MOE2017_VERBOSITY_LEVEL,
        )


def calc_P_integral(
    options,
    min_logP,
    max_logP,
    integrals_string,
    interpolator_name,
    mass_string,
    verbosity=0,
):
    """
    Function to calculate the P integral

    We need to renormalise this because min_per > 0, and not all periods should be included
    """

    global Moecache

    # Check if the dict exists
    if not Moecache.get(integrals_string, None):
        Moecache[integrals_string] = {}

    # Check for cached value. If it doesn't exist: calculate
    if not Moecache[integrals_string].get(options[mass_string], None):
        I = 0
        dlogP = 1e-3

        for logP in np.arange(min_logP, max_logP, dlogP):
            # Loop over all the values in the table, between the min and max P
            dp_dlogP = Moecache[interpolator_name].interpolate(
                [np.log10(options[mass_string]), logP]
            )[0]

            I += dp_dlogP * dlogP

        # Set the integral value in the dict
        Moecache[integrals_string][options[mass_string]] = I
        verbose_print(
            "\tMoe and di Stefano 2017: calc_P_integral: min_logP: {} integrals_string: {} interpolator_name: {} mass_string: {} mass: {} I: {}".format(
                min_logP,
                integrals_string,
                interpolator_name,
                mass_string,
                options[mass_string],
                I,
            ),
            verbosity,
            _MOE2017_VERBOSITY_LEVEL,
        )
    else:
        verbose_print(
            "\tMoe and di Stefano 2017: calc_P_integral: Found cached value for min_logP: {} integrals_string: {} interpolator_name: {} mass_string: {} mass: {} I: {}".format(
                min_logP,
                integrals_string,
                interpolator_name,
                mass_string,
                options[mass_string],
                Moecache[integrals_string][options[mass_string]],
            ),
            verbosity,
            _MOE2017_VERBOSITY_LEVEL,
        )


def calc_total_probdens(prob_dict):
    """
    Function to calculate the total probability density
    """

    total_probdens = 1
    for key in prob_dict:
        total_probdens *= prob_dict[key]
    prob_dict["total_probdens"] = total_probdens

    return prob_dict


def Moe_di_Stefano_2017_pdf(options, verbosity=0):
    """
    Moe & diStefano function to calculate the probability density.

    takes a dictionary as input (in options) with options:

    M1, M2, M3, M4 => masses (Msun) [M1 required, rest optional]
    P, P2, P3 => periods (days) [number: none=binary, 2=triple, 3=quadruple]
    ecc, ecc2, ecc3 => eccentricities [numbering as for P above]

    mmin => minimum allowed stellar mass (default 0.07)
    mmax => maximum allowed stellar mass (default 80.0)
    """

    verbose_print(
        "\tMoe_di_Stefano_2017_pdf with options:\n\t\t{}".format(json.dumps(options)),
        verbosity,
        _MOE2017_VERBOSITY_LEVEL,
    )

    prob_dict = (
        {}
    )  # Dictionary containing all the pdf values for the different parameters

    # Get the multiplicity from the options, and if its not there, calculate it based on the
    # TODO: the function below makes no sense. We NEED to pass the multiplicity in the
    if not options.get("multiplicity", None):
        msg = "\tMoe_di_Stefano_2017_pdf: Did not find a multiplicity value in the options dictionary"
        verbose_print(
            msg,
            verbosity,
            _MOE2017_VERBOSITY_LEVEL,
        )
        raise ValueError(msg)
        # multiplicity = 1
        # for n in range(2, 5):
        #     multiplicity += 1 if options.get("M{}".format(n), None) else 0
    else:
        multiplicity = options["multiplicity"]

    # Immediately return 0 if the multiplicity modulator is 0
    if options["multiplicity_modulator"][multiplicity - 1] == 0:
        verbose_print(
            "\tMoe_di_Stefano_2017_pdf: returning 0 because of the multiplicity modulator being 0",
            verbosity,
            _MOE2017_VERBOSITY_LEVEL,
        )
        return 0

    ############################################################
    # multiplicity fraction
    # Calculate the probability, or rather, fraction, of stars that belong to this mass

    multiplicity_probability = Moe_di_Stefano_2017_multiplicity_fractions(
        options, verbosity
    )[multiplicity - 1]
    prob_dict["multiplicity"] = multiplicity_probability
    verbose_print(
        "\tMoe_di_Stefano_2017_pdf: Appended multiplicity (mass1 = {}) probability ({}) to the prob dict ({})".format(
            options["M_1"], prob_dict["multiplicity"], prob_dict
        ),
        verbosity,
        _MOE2017_VERBOSITY_LEVEL,
    )

    ############################################################
    # always require an IMF for the primary star
    #
    # NB multiply by M1 to convert dN/dM to dN/dlnM
    # (dlnM = dM/M, so 1/dlnM = M/dM)

    # TODO: Create an n-part-powerlaw method that can have breakpoints and slopes. I'm using a three-part power law now.
    # TODO: is this actually the correct way? putting the M1 in there? Do we sample in log space?
    M1_probability = Kroupa2001(options["M_1"]) * options["M_1"]
    prob_dict["M_1"] = M1_probability
    verbose_print(
        "\tMoe_di_Stefano_2017_pdf: Appended Mass (m={}) probability ({}) to the prob dict ({})".format(
            options["M_1"], prob_dict["M_1"], prob_dict
        ),
        verbosity,
        _MOE2017_VERBOSITY_LEVEL,
    )
    # if M1_probability == 0: # If the probability is 0 then we don't have to calculate more
    #     calc_total_probdens(prob_dict)
    #     return prob_dict

    """
    From here we go through the multiplicities.
    """
    if multiplicity >= 2:
        # If the multiplicity is higher than 1, we will need to construct the following tables:
        # - period distribution table
        # - q distribution table
        # - eccentricity distribution table

        # Set up the interpolator for the periods
        if not Moecache.get("rinterpolator_log10P", None):
            Moecache["rinterpolator_log10P"] = py_rinterpolate.Rinterpolate(
                table=Moecache["period_distributions"],  # Contains the table of data
                nparams=2,  # log10M, log10P
                ndata=2,  # binary, triple
                verbosity=verbosity - (_MOE2017_VERBOSITY_INTERPOLATOR_LEVEL - 1),
            )
            verbose_print(
                "\tMoe_di_Stefano_2017_pdf: Created new period interpolator: {}".format(
                    Moecache["rinterpolator_log10P"]
                ),
                verbosity,
                _MOE2017_VERBOSITY_LEVEL,
            )

        # Make a table storing Moe's data for q distributions
        if (
            options.get("M_2", None)
            or options.get("M_3", None)
            or options.get("M_4", None)
        ):
            if not Moecache.get("rinterpolator_q", None):
                Moecache["rinterpolator_q"] = py_rinterpolate.Rinterpolate(
                    table=Moecache["q_distributions"],  # Contains the table of data
                    nparams=3,  # log10M, log10P, q
                    ndata=1,  #
                    verbosity=verbosity - (_MOE2017_VERBOSITY_INTERPOLATOR_LEVEL - 1),
                )
                verbose_print(
                    "\tMoe_di_Stefano_2017_pdf: Created new q interpolator: {}".format(
                        Moecache["rinterpolator_q"]
                    ),
                    verbosity,
                    _MOE2017_VERBOSITY_LEVEL,
                )

        # Make a table storing Moe's data for q distributions, but only if the ecc is actually sampled
        if "ecc" in options:
            if not options["ecc"] == None:
                if not Moecache.get("rinterpolator_e", None):
                    Moecache["rinterpolator_e"] = py_rinterpolate.Rinterpolate(
                        table=Moecache[
                            "ecc_distributions"
                        ],  # Contains the table of data
                        nparams=3,  # log10M, log10P, e
                        ndata=1,  #
                        verbosity=verbosity
                        - (_MOE2017_VERBOSITY_INTERPOLATOR_LEVEL - 1),
                    )
                    verbose_print(
                        "\tMoe_di_Stefano_2017_pdf: Created new e interpolator: {}".format(
                            Moecache["rinterpolator_e"]
                        ),
                        verbosity,
                        _MOE2017_VERBOSITY_LEVEL,
                    )

        ###############
        # Calculation for period of the binary

        if options.get("M_2", None):
            # Separation of the inner binary
            options["sep"] = calc_sep_from_period(
                options["M_1"], options["M_2"], options["P"]
            )
            # TODO: add check for min_logP with instant RLOF?
            # TODO: Actually use the value above.
            # Total mass inner binary:
            options["M_1+M_2"] = options["M_1"] + options["M_2"]

        # Calculate P integral or use cached value

        # get the periods from the Moecahe
        min_logP = float(Moecache["logperiods"][0])
        max_logP = float(Moecache["logperiods"][-1])

        calc_P_integral(
            options,
            min_logP,
            max_logP,
            "P_integrals",
            "rinterpolator_log10P",
            "M_1",
            verbosity,
        )

        # Set probabilty for P1
        p_val = Moecache["rinterpolator_log10P"].interpolate(
            [np.log10(options["M_1"]), np.log10(options["P"])]
        )[0]
        p_val = p_val / Moecache["P_integrals"][options["M_1"]]
        prob_dict["P"] = p_val
        verbose_print(
            "\tMoe_di_Stefano_2017_pdf: Appended period (m={}, P={}) probability ({}) to the prob list ({})".format(
                options["M_1"], options["P"], prob_dict["P"], prob_dict
            ),
            verbosity,
            _MOE2017_VERBOSITY_LEVEL,
        )
        # if prob_dict['P'] == 0: # If the probability is 0 then we don't have to calculate more
        #     calc_total_probdens(prob_dict)
        #     return prob_dict

        ############################################################
        # mass ratio (0 < q = M2/M1 < qmax)
        #
        # we need to construct the q table for the given M1
        # subject to qmin = Mmin/M1

        if options.get("M_2", None):
            # Build the table for q
            primary_mass = options["M_1"]
            secondary_mass = options["M_2"]
            m_label = "M_1"
            p_label = "P"

            # Construct the q table
            build_q_table(options, m_label, p_label, verbosity=verbosity)
            verbose_print(
                "\tMoe_di_Stefano_2017_pdf: Created q_table ({}) for m={} p={}".format(
                    Moecache[
                        "rinterpolator_q_given_{}_log10{}".format(m_label, p_label)
                    ],
                    options[m_label],
                    options[p_label],
                ),
                verbosity,
                _MOE2017_VERBOSITY_LEVEL,
            )

            # Add probability for the mass ratio
            q_prob = Moecache[
                "rinterpolator_q_given_{}_log10{}".format(m_label, p_label)
            ].interpolate([secondary_mass / primary_mass])[0]
            prob_dict["q"] = q_prob
            verbose_print(
                "\tMoe_di_Stefano_2017_pdf: appended mass ratio (M={} P={} q={}) probability ({}) to the prob list ({}) ".format(
                    options["M_1"],
                    options["P"],
                    options["M_2"] / options["M_1"],
                    prob_dict["q"],
                    prob_dict,
                ),
                verbosity,
                _MOE2017_VERBOSITY_LEVEL,
            )
            # if prob_dict['q'] == 0: # If the probability is 0 then we don't have to calculate more
            #     calc_total_probdens(prob_dict)
            #     return prob_dict

        ############################################################
        # Eccentricity
        # TODO: ask rob if the eccentricity requires an extrapolation as well.

        # Only do this if the eccentricity is sampled
        if "ecc" in options:
            if not options["ecc"] == None:
                # Calculate ecc integral or use cached value
                calc_e_integral(
                    options, "ecc_integrals", "rinterpolator_e", "M_1", "P", verbosity
                )
                mass_period_string = "{}_{}".format(options["M_1"], options["P"])

                # Set probability for ecc
                ecc_val = Moecache["rinterpolator_e"].interpolate(
                    [np.log10(options["M_1"]), np.log10(options["P"]), options["ecc"]]
                )[0]
                ecc_val = ecc_val / Moecache["ecc_integrals"][mass_period_string]
                prob_dict["ecc"] = ecc_val
                verbose_print(
                    "\tMoe_di_Stefano_2017_pdf: Appended eccentricity (m={}, P={}, ecc={}) probability ({}) to the prob list ({})".format(
                        options["M_1"],
                        options["P"],
                        options["ecc"],
                        prob_dict["ecc"],
                        prob_dict,
                    ),
                    verbosity,
                    _MOE2017_VERBOSITY_LEVEL,
                )
                # if prob_dict['ecc'] == 0: # If the probability is 0 then we don't have to calculate more
                #     calc_total_probdens(prob_dict)
                #     return prob_dict

        # Calculations for when multiplicity is bigger than 3
        # BEWARE: binary_c does not evolve these systems actually and the code below should be revised for when binary_c actually evolves triples.
        # For that reason, I would not advise to use things with multiplicity > 3
        if multiplicity >= 3:

            ############################################################
            # orbital period 2 =
            #     orbital period of star 3 (multiplicity==3) or
            #     the star3+star4 binary (multiplicity==4)
            #
            # we assume the same period distribution for star 3
            # (or stars 3 and 4) but with a separation that is >10*a*(1+e)
            # where 10*a*(1+e) is the maximum apastron separation of
            # stars 1 and 2

            # TODO: Is this a correct assumption?
            max_sep = 10.0 * options["sep"] * (1.0 + options["ecc"])
            min_P2 = calc_period_from_sep(options["M_1+M_2"], options["mmin"], max_sep)
            min_logP2 = math.log10(min_P2)
            # max_logP2 = 10.0
            # min_logP = Moecache['logperiods'][0]
            max_logP2 = float(Moecache["logperiods"][-1])

            if options["P2"] < min_P2:
                # period is too short : system is not hierarchical
                prob_dict["P2"] = 0
                verbose_print(
                    "\tMoe_di_Stefano_2017_pdf: period2 is too short: {} < {}, system is not hierarchical. Added 0 to probability list".format(
                        options["P1"], min_P2
                    ),
                    verbosity,
                    _MOE2017_VERBOSITY_LEVEL,
                )
                # if prob_dict['P2'] == 0: # If the probability is 0 then we don't have to calculate more
                #     calc_total_probdens(prob_dict)
                #     return prob_dict

            else:
                # period is long enough that the system is hierarchical
                # hence the separation between the outer star
                # and inner binary
                options["sep2"] = calc_sep_from_period(
                    options["M_3"], options["M_1+M_2"], options["P2"]
                )

                # Check for cached value of P integral or calculate
                calc_P_integral(
                    options,
                    min_logP2,
                    max_logP2,
                    "P2_integrals",
                    "rinterpolator_log10P",
                    "M_1+M_2",
                    verbosity,
                )

                # Add the probability
                p_val = Moecache["rinterpolator_log10P"].interpolate(
                    [np.log10(options["M_1+M_2"]), np.log10(options["P2"])]
                )[0]
                p_val = p_val / Moecache["P2_integrals"][options["M_1+M_2"]]
                prob_dict["P2"] = p_val
                verbose_print(
                    "\tMoe_di_Stefano_2017_pdf: Appended period2 (m1={} m2={}, P2={}) probability ({}) to the prob list ({})".format(
                        options["M_1"],
                        options["M_2"],
                        options["P2"],
                        prob_dict["P2"],
                        prob_dict,
                    ),
                    verbosity,
                    _MOE2017_VERBOSITY_LEVEL,
                )
                # if prob_dict['P2'] == 0: # If the probability is 0 then we don't have to calculate more
                #     calc_total_probdens(prob_dict)
                #     return prob_dict

                ############################################################
                # mass ratio 2 = q2 = M3 / (M1+M2)
                #
                # we need to construct the q table for the given M1
                # subject to qmin = Mmin/(M1+M2)

                # Set the variables for the masses and their names
                primary_mass = options["M_1+M_2"]
                secondary_mass = options["M_3"]
                m_label = "M_1+M_2"
                p_label = "P2"

                # Build q table
                build_q_table(options, m_label, p_label, verbosity=verbosity)
                verbose_print(
                    "\tMoe_di_Stefano_2017_pdf: Called build_q_table",
                    verbosity,
                    _MOE2017_VERBOSITY_LEVEL,
                )

                # Add the probability
                q2_val = Moecache[
                    "rinterpolator_q_given_{}_log10{}".format(m_label, p_label)
                ].interpolate([secondary_mass / primary_mass])[0]
                prob_dict["q2"] = q2_val
                verbose_print(
                    "\tMoe_di_Stefano_2017_pdf: appended mass ratio (M_1+M_2={} M_3={} P={} q={}) probability ({}) to the prob list ({}) ".format(
                        options["M_1+M_2"],
                        options["M_3"],
                        options["P"],
                        secondary_mass / primary_mass,
                        prob_dict["q2"],
                        prob_dict,
                    ),
                    verbosity,
                    _MOE2017_VERBOSITY_LEVEL,
                )
                # if prob_dict['q2'] == 0: # If the probability is 0 then we don't have to calculate more
                #     calc_total_probdens(prob_dict)
                #     return prob_dict

                # TODO: Implement ecc2 calculation
                if multiplicity == 4:
                    # quadruple system.
                    # TODO: Ask Rob about the structure of the quadruple. Is this only double binary quadruples?

                    ############################################################
                    # orbital period 3
                    #
                    # we assume the same period distribution for star 4
                    # as for any other stars but Pmax must be such that
                    # sep3 < sep2 * 0.2

                    # TODO: fix this here
                    max_sep3 = 0.2 * options["sep2"] * (1.0 + options["ecc2"])
                    max_per3 = calc_period_from_sep(
                        options["M_1+M_2"], options["mmin"], max_sep3
                    )

                    # Calculate P integral or use the cached value
                    # TODO: Make sure we use the correct period idea here.
                    calc_P_integral(
                        options,
                        min_logP2,
                        max_logP2,
                        "P2_integrals",
                        "rinterpolator_log10P",
                        "M_1+M_2",
                        verbosity,
                    )

                    # Set probability
                    p_val = Moecache["rinterpolator_log10P"].interpolate(
                        [np.log10(options["M_1+M_2"]), np.log10(options["P2"])]
                    )[0]
                    p_val = p_val / Moecache["P2_integrals"][options["M_1+M_2"]]
                    prob_dict["P3"] = p_val
                    verbose_print(
                        "\tMoe_di_Stefano_2017_pdf: Appended period2 (M=4) (M_1={} M_2={}, P2={}) probability ({}) to the prob list ({})".format(
                            options["M_1"],
                            options["M_2"],
                            options["P2"],
                            prob_dict["P3"],
                            prob_dict,
                        ),
                        verbosity,
                        _MOE2017_VERBOSITY_LEVEL,
                    )
                    # if prob_dict['P3'] == 0: # If the probability is 0 then we don't have to calculate more
                    #     calc_total_probdens(prob_dict)
                    #     return prob_dict

                    ############################################################
                    # mass ratio 2
                    #
                    # we need to construct the q table for the given M1
                    # subject to qmin = Mmin/(M1+M2)
                    # Make a table storing Moe's data for q distributions

                    # Build the table for q2
                    primary_mass = options["M_1+M_2"]
                    secondary_mass = options["M_3"]
                    m_label = "M_1+M_2"
                    p_label = "P2"

                    # Calculate new q table
                    build_q_table(options, m_label, p_label, verbosity=verbosity)
                    verbose_print(
                        "\tMoe_di_Stefano_2017_pdf: Created q_table ".format(),
                        verbosity,
                        _MOE2017_VERBOSITY_LEVEL,
                    )

                    # Add the probability
                    q3_prob = Moecache[
                        "rinterpolator_q_given_{}_log10{}".format(m_label, p_label)
                    ].interpolate([secondary_mass / primary_mass])[0]
                    prob_dict["q3"] = q3_prob
                    verbose_print(
                        "\tMoe_di_Stefano_2017_pdf: appended mass ratio (M_1+M_2={} M_3={} P={} q={}) probability ({}) to the prob list ({}) ".format(
                            options["M_1+M_2"],
                            options["M_3"],
                            options["P"],
                            secondary_mass / primary_mass,
                            prob_dict["q3"],
                            prob_dict,
                        ),
                        verbosity,
                        _MOE2017_VERBOSITY_LEVEL,
                    )
                    # if prob_dict['q3'] == 0: # If the probability is 0 then we don't have to calculate more
                    #     calc_total_probdens(prob_dict)
                    #     return prob_dict

                    # TODO ecc 3

    # check for input of multiplicity
    elif multiplicity not in range(1, 5):
        msg = "\tMoe_di_Stefano_2017_pdf: Unknown multiplicity {}".format(multiplicity)
        verbose_print(
            msg,
            verbosity,
            _MOE2017_VERBOSITY_LEVEL,
        )
        raise ValueError(msg)

    # Calculate total probdens:
    prob_dict = calc_total_probdens(prob_dict)

    # Some info
    if multiplicity == 1:
        verbose_print(
            "\tMoe_di_Stefano_2017_pdf: M_1={} q=N/A log10P=N/A ({}): {} -> {}\n".format(
                options["M_1"],
                len(prob_dict),
                str(prob_dict),
                prob_dict["total_probdens"],
            ),
            verbosity,
            _MOE2017_VERBOSITY_LEVEL,
        )
    elif multiplicity == 2:
        verbose_print(
            "\tMoe_di_Stefano_2017_pdf: M_1={} q={} log10P={} ecc={} ({}): {} -> {}\n".format(
                options["M_1"],
                options["M_2"] / options["M_1"] if options.get("M_2", None) else "N/A",
                np.log10(options["P"]),
                options["ecc"] if options.get("ecc", None) else "N/A",
                len(prob_dict),
                str(prob_dict),
                prob_dict["total_probdens"],
            ),
            verbosity,
            _MOE2017_VERBOSITY_LEVEL,
        )
    elif multiplicity == 3:
        verbose_print(
            "\tMoe_di_Stefano_2017_pdf: M_1={} q={} log10P={} ecc={} M_3={} log10P2={} ecc2={} ({}): {} -> {}".format(
                options["M_1"],
                options["M_2"] / options["M_1"] if options.get("M_2", None) else "N/A",
                np.log10(options["P"]),
                options["ecc"] if options.get("ecc", None) else "N/A",
                options["M_3"],
                np.log10(options["P2"]),
                options["ecc2"] if options.get("ecc2", None) else "N/A",
                len(prob_dict),
                str(prob_dict),
                prob_dict["total_probdens"],
            ),
            verbosity,
            _MOE2017_VERBOSITY_LEVEL,
        )
    elif multiplicity == 4:
        verbose_print(
            "Moe_di_Stefano_2017_pdf: M_1={} q={} log10P={} ecc={} M_3={} log10P2={} ecc2={} M_4={} log10P3={} ecc3={} ({}) : {} -> {}".format(
                options["M_1"],
                options["M_2"] / options["M_1"] if options.get("M_2", None) else "N/A",
                np.log10(options["P"]),
                options["ecc"] if options.get("ecc", None) else "N/A",
                options["M_3"],
                np.log10(options["P2"]),
                options["ecc2"] if options.get("ecc2", None) else "N/A",
                options["M_4"],
                np.log10(options["P3"]),
                options["ecc3"] if options.get("ecc3", None) else "N/A",
                len(prob_dict),
                str(prob_dict),
                prob_dict["total_probdens"],
            ),
            verbosity,
            _MOE2017_VERBOSITY_LEVEL,
        )
    return prob_dict
