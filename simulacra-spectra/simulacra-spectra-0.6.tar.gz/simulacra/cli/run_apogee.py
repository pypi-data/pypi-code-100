from simulacra.star import PhoenixModel
from simulacra.detector import Detector
from simulacra.tellurics import TelFitModel

import astropy.units as u

def run_apogee(*args):
    # parser args into these constants and filename
    print(args)
    filename = 'out/somethingsomethingsometing.h5'
    logg = 1.0
    T = 4600
    z = -1.0
    alpha = 0.4
    epoches = 30
    resolution = 22500
    ra, dec =
    period = 10 * u.day
    amplitude = 300 * u.m/u.s
    # no jitter or stretch to the wavelength grid
    epsilon = 0.0
    w = 0.0

    stellar_model   = PhoenixModel(alpha,z,T,alpha)
    tellurics_model = TelFitModel(1.5*u.micron,1.7*u.micron)

    detector = Detector(stellar_model,resolution,epsilon=epsilon,w=w)
    detector.add_model(tellurics_model)

    res,data = detector.simulate(epoches)
    data.to_h5(filename)
    # return data
