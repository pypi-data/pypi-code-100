"""
Module containing the spacing functions for the binarycpython package. Very under-populated at the moment, but more are likely to come soon

Tasks:
    TODO: add more spacing functions to this module.
"""

from typing import Union
import functools
import math
import numpy as np
import py_rinterpolate
import sys
from binarycpython.utils.grid import Population


@functools.lru_cache(maxsize=16)
def const(
    min_bound: Union[int, float], max_bound: Union[int, float], steps: int
) -> list:
    """
    Samples a range linearly. Uses numpy linspace.

    Args:
        min_bound: lower bound of range
        max_bound: upper bound of range
        steps: number of segments between min_bound and max_bound

    Returns:
        np.linspace(min_bound, max_bound, steps+1)
    """
    return np.linspace(min_bound, max_bound, steps + 1)


############################################################
@functools.lru_cache(maxsize=16)
def const_ranges(ranges) -> list:
    """
    Samples a series of ranges linearly.

    Args:
        ranges: a tuple of tuples passed to the const() spacing function.

    Returns:
        numpy array of masses

    Example:
        The following allocates 10 stars between 0.1 and 0.65, 20 stars between 0.65
        and 0.85, and 10 stars between 0.85 and 10.0 Msun.

        samplerfunc="const_ranges((({},{},{}),({},{},{}),({},{},{})))".format(
            0.1,0.65,10,
            0.65,0.85,20,
            0.85,10.0,10
        ),

    """

    masses = np.empty(0)
    for range in ranges:
        masses = np.append(masses, const(*range))
    return np.unique(masses)


############################################################
def peak_normalized_gaussian_func(
    x: Union[int, float], mean: Union[int, float], sigma: Union[int, float]
) -> Union[int, float]:
    """
    Function to evaluate a Gaussian at a given point, note
    that the normalization is such that the peak is always 1.0,
    not that the integral is 1.0

    Args:
        x: location at which to evaluate the distribution
        mean: mean of the Gaussian
        sigma: standard deviation of the Gaussian

    Returns:
        value of the Gaussian at x
    """
    gaussian_prefactor = 1.0  # / math.sqrt(2.0 * math.pi)

    r = 1.0 / sigma
    y = (x - mean) * r
    return math.exp(-0.5 * y ** 2)


############################################################
@functools.lru_cache(maxsize=16)
def gaussian_zoom(
    min_bound: Union[int, float],
    max_bound: Union[int, float],
    zoom_mean: Union[int, float],
    zoom_dispersion: Union[int, float],
    zoom_magnitude: Union[int, float],
    steps: int,
) -> list:
    """
    Samples such that a region is zoomed in according to a 1-Gaussian function

    Args:
        min_bound: lower bound of range
        max_bound: upper bound of range
        zoom_mean: mean of the Gaussian zoom location
        zoom_dispersion: dispersion of the Gaussian
        zoom_magnitude: depth of the Gaussian (should be 0<= zoom_magntiude <1)
        steps: number of segments between min_bound and max_bound assuming a linear step
               this is what you'd normally call "resolution"

    Returns:
        Numpy array of sample values
    """

    # linear spacing: this is what we'd have
    # in the absence of a Gaussian zoom
    linear_spacing = (max_bound - min_bound) / (steps - 1)

    # make the list of values
    x = min_bound
    array = np.array([])
    while x <= max_bound:
        array = np.append(array, x)
        g = peak_normalized_gaussian_func(x, zoom_mean, zoom_dispersion)
        f = 1.0 - zoom_magnitude * g
        dx = linear_spacing * f
        x = x + dx

    # force the last array member to be max_bound if it's not
    if array[-1] != max_bound:
        array[-1] = max_bound

    return np.unique(array)


@functools.lru_cache(maxsize=16)
def const_dt(
    self,
    dt=1000.0,
    dlogt=0.1,
    mmin=0.07,
    mmax=100.0,
    nres=1000,
    logspacing=False,
    tmin=3.0,  # start at 3Myr
    tmax=None,  # use max_evolution_time by default
    mindm=None,  # tuple of tuples
    maxdm=((0.07, 1.0, 0.1), (1.0, 300.0, 1.0)),  # tuple of tuples
    fsample=1.0,
    factor=1.0,
    logmasses=False,
    log10masses=False,
    showlist=False,
    showtable=False,
):
    """
    const_dt returns a list of masses spaced at a constant age difference

    Args:
        dt: the time difference between the masses (1000.0 Myr, used when logspacing==False)
        dlogt : the delta log10(time) difference between masses (0.1 dex, used when logspacing==True)
        mmin: the minimum mass to be considered in the stellar lifetime interpolation table (0.07 Msun)
        mmax: the maximum mass to be considered in the stellar lifetime interpolation table (100.0 Msun)
        nres: the resolution of the stellar lifetime interpolation table (100)
        logspacing: whether to use log-spaced time, in which case dt is actually d(log10(t))
        tmin: the minimum time to consider (Myr, default 3.0 Myr)
        tmax: the maximum time to consider (Myr, default None which means we use the grid option 'max_evolution_time')
        mindm: a tuple of tuples containing a mass range and minimum mass spacing in that range. The default is ((0.07,1.0,0.1),(1.0,300.0,1.0)) allocated a minimum dm of 0.1Msun in the mass range 0.07 to 1.0 Msun and 1.0Msun in the range 1.0 to 300.0 Msun. Anything you set overrides this. Note, if you use only one tuple, you must set it with a trailing comma, thus, e.g. ((0.07,1.0,0.1),). (default None)
        maxdm: a list of tuples similar to mindm but specifying a maximum mass spacing. In the case of maxdm, if the third option in each tuple is negative it is treated as a log step (its absolute value is used as the step).  (default None)
        fsample: a global sampling (Shannon-like) factor (<1) to improve resolution (default 1.0, set to smaller to improve resolution)
        factor: all masses generated are multiplied by this after generation
        showtable: if True, the mass list and times are shown to stdout after generation
        showlist: if True, show the mass list once generated
        logmasses: if True, the masses are logged with math.log()
        log10masses: if True, the masses are logged with math.log10()

    Returns:
        Array of masses.

    Example:
    # these are lines set as options to Population.add_grid_value(...)

    # linear time bins of 1Gyr
    samplerfunc="const_dt(self,dt=1000,nres=100,mmin=0.07,mmax=2.0,showtable=True)"

    # logarithmic spacing in time, generally suitable for Galactic
    # chemical evolution yield grids.
    samplerfunc="const_dt(self,dlogt=0.1,nres=100,mmin=0.07,mmax=80.0,maxdm=((0.07,1.0,0.1),(1.0,10.0,1.0),(10.0,80.0,2.0)),showtable=True,logspacing=True,fsample=1.0/4.0)"

    """

    # first, make a stellar lifetime table
    #
    # we should use the bse_options from self
    # so our lifetime_population uses the same physics
    lifetime_population = Population()
    lifetime_population.bse_options = dict(self.bse_options)

    # we only want to evolve the star during nuclear burning,
    # we don't want a dry run of the grid
    # we want to use the right number of CPU cores
    lifetime_population.set(
        do_dry_run=False,
        num_cores=self.grid_options["num_cores"],
        max_stellar_type_1=10,
        save_ensemble_chunks=False,
    )

    # make a grid in M1
    lifetime_population.add_grid_variable(
        name="lnM_1",
        parameter_name="M_1",
        longname="log Primary mass",  # == single-star mass
        valuerange=[math.log(mmin), math.log(mmax)],
        samplerfunc="const(math.log({mmin}),math.log({mmax}),{nres})".format(
            mmin=mmin, mmax=mmax, nres=nres
        ),
        probdist="1",  # dprob/dm1 : we don't care, so just set it to 1
        dphasevol="dlnM_1",
        precode="M_1=math.exp(lnM_1)",
        condition="",  # Impose a condition on this grid variable. Mostly for a check for yourself
        gridtype="edge",
    )

    # set up the parse function
    def _parse_function(self, output):
        if output:
            for line in output.splitlines():
                data = line.split()
                if data[0] == "SINGLE_STAR_LIFETIME":
                    # append (log10(mass), log10(lifetime)) tuples
                    logm = math.log10(float(data[1]))
                    logt = math.log10(float(data[2]))
                    # print(line)
                    # print("logM=",logm,"M=",10.0**logm," -> logt=",logt)
                    self.grid_results["interpolation table m->t"][logm] = logt
                    self.grid_results["interpolation table t->m"][logt] = logm

    lifetime_population.set(
        parse_function=_parse_function,
    )

    # run to build the interpolation table
    print("Running population to make lifetime interpolation table, please wait")
    lifetime_population.evolve()
    # print("Data table",lifetime_population.grid_results['interpolation table t->m'])

    # convert to nested lists for the interpolator
    #
    # make time -> mass table
    data_table_time_mass = []
    times = sorted(lifetime_population.grid_results["interpolation table t->m"].keys())
    for time in times:
        mass = lifetime_population.grid_results["interpolation table t->m"][time]
        # we have to make sure the time is monotonic (not guaranteed at high mass)
        if len(data_table_time_mass) == 0:
            data_table_time_mass.append([time, mass])
        elif mass < data_table_time_mass[-1][1]:
            data_table_time_mass.append([time, mass])

    # make mass -> time table
    data_table_mass_time = []
    masses = sorted(lifetime_population.grid_results["interpolation table m->t"].keys())
    for mass in masses:
        time = lifetime_population.grid_results["interpolation table m->t"][mass]
        data_table_mass_time.append([mass, time])

    # set up interpolators
    interpolator_time_mass = py_rinterpolate.Rinterpolate(
        table=data_table_time_mass, nparams=1, ndata=1, verbosity=0  # mass  # lifetime
    )
    interpolator_mass_time = py_rinterpolate.Rinterpolate(
        table=data_table_mass_time, nparams=1, ndata=1, verbosity=0  # lifetime  # mass
    )

    # function to get a mass given a time (Myr)
    def _mass_from_time(linear_time):
        return 10.0 ** interpolator_time_mass.interpolate([math.log10(linear_time)])[0]

    # function to get a time given a mass (Msun)
    def _time_from_mass(mass):
        return 10.0 ** interpolator_mass_time.interpolate([math.log10(mass)])[0]

    # return a unique list
    def _uniq(_list):
        return sorted(list(set(_list)))

    # format a whole list like %g
    def _format(_list):
        return [float("{x:g}".format(x=x)) for x in _list]

    # construct mass list, always include the min and max
    mass_list = [mmin, mmax]

    # first, make sure the stars are separated by only
    # maxdm
    if maxdm:
        for x in maxdm:
            range_min = x[0]
            range_max = x[1]
            dm = x[2]
            if dm < 0.0:
                # use log scale
                dlogm = -dm
                logm = math.log(mmin)
                logmmax = math.log(mmax)
                logrange_min = math.log(range_min)
                logrange_max = math.log(range_max)
                while logm <= logmmax:
                    if logm >= logrange_min and logm <= logrange_max:
                        mass_list.append(math.exp(logm))
                    logm += dlogm
            else:
                # use linear scale
                m = mmin
                while m <= mmax:
                    if m >= range_min and m <= range_max:
                        mass_list.append(m)
                    m += dm

    # start time loop at tmax or max_evolution_time
    t = tmax if tmax else self.bse_options["max_evolution_time"]

    # set default mass list
    if logspacing:
        logt = math.log10(t)
        logtmin = math.log10(tmin)
        while logt > logtmin:
            m = _mass_from_time(10.0 ** logt)
            mass_list.append(m)
            logt = max(logtmin, logt - dlogt * fsample)
    else:
        while t > tmin:
            m = _mass_from_time(t)
            mass_list.append(m)
            t = max(tmin, t - dt * fsample)

    # make mass list unique
    mass_list = _uniq(mass_list)

    if mindm:
        for x in mindm:
            range_min = x[0]
            range_max = x[1]
            mindm = x[2]
            # impose a minimum dm: if two masses in the list
            # are separated by < this, remove the second
            for index, mass in enumerate(mass_list):
                if index > 0 and mass >= range_min and mass <= range_max:
                    dm = mass_list[index] - mass_list[index - 1]
                    if dm < mindm:
                        mass_list[index - 1] = 0.0
            mass_list = _uniq(mass_list)
            if mass_list[0] == 0.0:
                mass_list.remove(0.0)

    # apply multiplication factor if given
    if factor and factor != 1.0:
        mass_list = [m * factor for m in mass_list]

    # reformat numbers
    mass_list = _format(mass_list)

    # show the mass<>time table?
    if showtable:
        twas = 0.0
        logtwas = 0.0
        for i, m in enumerate(mass_list):
            t = _time_from_mass(m)
            logt = math.log10(t)
            if twas > 0.0:
                print(
                    "{i:4d} m={m:13g} t={t:13g} log10(t)={logt:13g} dt={dt:13g} dlog10(t)={dlogt:13g}".format(
                        i=i, m=m, t=t, logt=logt, dt=twas - t, dlogt=logtwas - logt
                    )
                )
            else:
                print(
                    "{i:4d} m={m:13g} t={t:13g} log10(t)={logt:13g}".format(
                        i=i, m=m, t=t, logt=logt
                    )
                )
            twas = t
            logtwas = logt
        exit()

    # return the mass list as a numpy array
    mass_list = np.unique(np.array(mass_list))

    # perhaps log the masses
    if logmasses:
        mass_list = np.log(mass_list)
    if log10masses:
        mass_list = np.log10(mass_list)

    if showlist:
        print("const_dt mass list ({} masses)\n".format(len(mass_list)), mass_list)

    return mass_list
