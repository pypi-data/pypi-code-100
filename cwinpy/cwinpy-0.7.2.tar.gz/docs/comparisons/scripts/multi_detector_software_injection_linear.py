#!/usr/bin/env python

"""
Compare cwinpy with lalapps_pulsar_parameter_estimation_nested for noise-only
data for a multiple detectors (H1, L1 and V1) containing a software injection
with close-to-circular polarisation.
"""

import os
import subprocess as sp
from collections import OrderedDict

import corner
import h5py
import matplotlib
import matplotlib.font_manager as font_manager
import numpy as np
from astropy.utils.data import download_file
from bilby.core.prior import Uniform
from comparitors import comparisons
from cwinpy import HeterodynedData
from cwinpy.pe import pe
from lalinference import LALInferenceHDF5PosteriorSamplesDatasetName
from lalinference.io import read_samples
from matplotlib.lines import Line2D

matplotlib.use("Agg")

# URL for ephemeris files
DOWNLOAD_URL = "https://git.ligo.org/lscsoft/lalsuite/raw/master/lalpulsar/lib/{}"

# create a fake pulsar parameter file
parcontent = """\
PSRJ     J0123+3456
RAJ      01:23:45.6789
DECJ     34:56:54.321
F0       567.89
F1       -1.2e-12
PEPOCH   56789
H0       1.1e-25
COSIOTA  -0.05
PSI      0.5
PHI0     1.2
"""

injection_parameters = OrderedDict()
injection_parameters["h0"] = 1.1e-25
injection_parameters["phi0"] = 1.2
injection_parameters["psi"] = 0.5
injection_parameters["cosiota"] = -0.05

label = "multi_detector_software_injection_linear"
outdir = "outputs"

if not os.path.isdir(outdir):
    os.makedirs(outdir)

# add content to the par file
parfile = os.path.join(outdir, "{}.par".format(label))
with open(parfile, "w") as fp:
    fp.write(parcontent)

# create some fake heterodyned data
detectors = ["H1", "L1", "V1"]  # the detector to use
asd = 1e-24  # noise amplitude spectral density
times = np.linspace(1000000000.0, 1000086340.0, 1440)  # times
het = {}
hetfiles = []
for detector in detectors:
    het[detector] = HeterodynedData(
        times=times,
        par=parfile,
        injpar=parfile,
        inject=True,
        fakeasd=asd,
        detector=detector,
    )

    # output the data
    hetfile = os.path.join(outdir, "{}_{}_data.txt".format(label, detector))
    het[detector].write(hetfile)
    hetfiles.append(hetfile)

# create priors
phi0range = [0.0, np.pi]
psirange = [0.0, np.pi / 2.0]
cosiotarange = [-1.0, 1.0]
h0range = [0.0, 1e-23]

# set prior for lalapps_pulsar_parameter_estimation_nested
priorfile = os.path.join(outdir, "{}_prior.txt".format(label))
priorcontent = """H0 uniform {} {}
PHI0 uniform {} {}
PSI uniform {} {}
COSIOTA uniform {} {}
"""
with open(priorfile, "w") as fp:
    fp.write(priorcontent.format(*(h0range + phi0range + psirange + cosiotarange)))

# set prior for bilby
priors = OrderedDict()
priors["h0"] = Uniform(h0range[0], h0range[1], "h0", latex_label=r"$h_0$")
priors["phi0"] = Uniform(
    phi0range[0], phi0range[1], "phi0", latex_label=r"$\phi_0$", unit="rad"
)
priors["psi"] = Uniform(
    psirange[0], psirange[1], "psi", latex_label=r"$\psi$", unit="rad"
)
priors["cosiota"] = Uniform(
    cosiotarange[0], cosiotarange[1], "cosiota", latex_label=r"$\cos{\iota}$"
)

# run lalapps_pulsar_parameter_estimation_nested
try:
    execpath = os.environ["CONDA_PREFIX"]
except KeyError:
    raise KeyError(
        "Please work in a conda environment with lalsuite and cwinpy installed"
    )

execpath = os.path.join(execpath, "bin")

lppen = os.path.join(execpath, "lalapps_pulsar_parameter_estimation_nested")
n2p = os.path.join(execpath, "lalinference_nest2pos")

Nlive = 1024  # number of nested sampling live points
Nmcmcinitial = 0  # set to 0 so that prior samples are not resampled

outfile = os.path.join(outdir, "{}_nest.hdf".format(label))

# set ephemeris files
efile = download_file(DOWNLOAD_URL.format("earth00-40-DE405.dat.gz"), cache=True)
sfile = download_file(DOWNLOAD_URL.format("sun00-40-DE405.dat.gz"), cache=True)
tfile = download_file(DOWNLOAD_URL.format("te405_2000-2040.dat.gz"), cache=True)

# set the command line arguments
runcmd = " ".join(
    [
        lppen,
        "--verbose",
        "--input-files",
        ",".join(hetfiles),
        "--detectors",
        ",".join(detectors),
        "--par-file",
        parfile,
        "--prior-file",
        priorfile,
        "--Nlive",
        "{}".format(Nlive),
        "--Nmcmcinitial",
        "{}".format(Nmcmcinitial),
        "--outfile",
        outfile,
        "--ephem-earth",
        efile,
        "--ephem-sun",
        sfile,
        "--ephem-timecorr",
        tfile,
    ]
)

with sp.Popen(
    runcmd,
    stdout=sp.PIPE,
    stderr=sp.PIPE,
    shell=True,
    bufsize=1,
    universal_newlines=True,
) as p:
    for line in p.stderr:
        print(line, end="")

# convert nested samples to posterior samples
outpost = os.path.join(outdir, "{}_post.hdf".format(label))
runcmd = " ".join([n2p, "-p", outpost, outfile])
with sp.Popen(
    runcmd,
    stdout=sp.PIPE,
    stderr=sp.PIPE,
    shell=True,
    bufsize=1,
    universal_newlines=True,
) as p:
    for line in p.stdout:
        print(line, end="")

# get posterior samples
post = read_samples(outpost, tablename=LALInferenceHDF5PosteriorSamplesDatasetName)
lp = len(post["H0"])
postsamples = np.zeros((lp, len(priors)))
for i, p in enumerate(priors.keys()):
    postsamples[:, i] = post[p.upper()]

# get evidence
hdf = h5py.File(outpost, "r")
a = hdf["lalinference"]["lalinference_nest"]
evsig = a.attrs["log_evidence"]
evnoise = a.attrs["log_noise_evidence"]
hdf.close()

# run bilby via the pe interface
runner = pe(
    data_file=hetfiles,
    par_file=parfile,
    prior=priors,
    detector=detectors,
    sampler="dynesty",
    sampler_kwargs={"Nlive": Nlive, "walks": 40},
    outdir=outdir,
    label=label,
)

result = runner.result

# evaluate the likelihood on a grid
gridpoints = 35
grid_size = dict()
for p in priors.keys():
    grid_size[p] = np.linspace(
        np.min(result.posterior[p]), np.max(result.posterior[p]), gridpoints
    )

grunner = pe(
    data_file=hetfiles,
    par_file=parfile,
    prior=priors,
    detector=detectors,
    outdir=outdir,
    label=label,
    grid=True,
    grid_kwargs={"grid_size": grid_size},
)

grid = grunner.grid

# output comparisons
comparisons(label, outdir, grid, priors, cred=0.9)

# plot results
fig = result.plot_corner(save=False, parameters=list(priors.keys()), color="b")
fig = corner.corner(
    postsamples,
    fig=fig,
    color="r",
    bins=50,
    smooth=0.9,
    quantiles=[0.16, 0.84],
    levels=(1 - np.exp(-0.5), 1 - np.exp(-2), 1 - np.exp(-9 / 2.0)),
    fill_contours=True,
    hist_kwargs={"density": True},
)
axes = fig.get_axes()
axidx = 0
for p in priors.keys():
    axes[axidx].plot(
        grid.sample_points[p],
        np.exp(grid.marginalize_ln_posterior(not_parameters=p) - grid.log_evidence),
        "k--",
    )
    axidx += 5

# custom legend
legend_elements = [
    Line2D([], [], color="r", label="lalapps_pulsar_parameter_estimation_nested"),
    Line2D([], [], color="b", label="cwinpy_pe"),
    Line2D([], [], color="k", ls="--", label="cwinpy_pe (grid)"),
]
font = font_manager.FontProperties(family="monospace")
leg = axes[3].legend(
    handles=legend_elements, loc="upper right", frameon=False, prop=font, handlelength=3
)
for line in leg.get_lines():
    line.set_linewidth(1.0)

fig.savefig(os.path.join(outdir, "{}_corner.png".format(label)), dpi=150)
