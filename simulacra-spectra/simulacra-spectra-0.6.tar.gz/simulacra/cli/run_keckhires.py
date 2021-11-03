from simulacra.star import PhoenixModel
from simulacra.detector import Detector
from simulacra.tellurics import TelFitModel
from simulacra.gascell import GasCellModel


import astropy.units as u

def run_keckhires(*args):
    # parser args into these constants and filename
    filename = 'out/somethingsomethingsometing.h5'
    logg = 1.0
    T = 4600
    z = -1.0
    alpha = 0.4
    epoches = 30
    resolution = 120000
    ra, dec = 1.0,10
    period = 300 * u.day
    amplitude = 10 * u.km/u.s
    # no jitter or stretch to wavelength grid
    epsilon = 0.01
    w = 1.0

    stellar_model   = PhoenixModel(alpha,z,T,alpha)
    tellurics_model = TelFitModel(500*u.nm,630*u.nm)
    gascell_model   = GasCellModel(filename='./data/gascell/keck_fts_inUse.idl')

    detector = Detector(stellar_model,resolution,epsilon=epsilon,w=w)
    detector.add_model(tellurics_model)
    detector.add_model(gascell_model)

    res,data = detector.simulate(epoches)
    data.to_h5(filename)
    # return data
