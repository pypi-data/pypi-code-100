import os
import xml.etree.ElementTree as ET

import numpy as np
from scipy.interpolate import interp1d
from skrf import network

from sknrf.settings import Settings
from sknrf.utilities.rf import rU2dBU, dBU2rU, z2g


def t2offset(f, s21, z0=50.0):
    """ Returns the calkit offset loss parameter defined at freq=1GHz"""
    group_delay = -np.diff(s21)/(2*np.pi)
    s21_loss_dB = rU2dBU(interp1d(f, s21)(1e9))
    s21_delay = interp1d(f, group_delay)(1e9)
    loss_GOhm_s = (np.log(10.0)/10)*s21_loss_dB*np.sqrt(1e9/1e9)*(z0/s21_delay)
    return loss_GOhm_s, group_delay, z0


def offset2t(f, loss, group_delay, z0=50.0):
    """ Returns the s21 of the calkit offset"""
    s21_angle = -2*np.pi*f*group_delay
    loss_GOhm_s = loss/(2*np.pi*1e9)
    s21_loss_dB = loss_GOhm_s/((np.log(10.0)/10)*np.sqrt(f/1e9)*(z0/s21_angle))
    return dBU2rU(s21_loss_dB)*np.exp(1j*s21_angle)


def xkt2calkit(xkt_filename, calkit_dirname="", fstart=0.0, fstop=1e100, fstep=100e6):
    if len(calkit_dirname) == 0:
        calkit_dirname = os.sep.join((Settings().data_root, "calkits"))
    _, calkit_name = os.path.split(xkt_filename)
    calkit_name, _ = os.path.splitext(calkit_name)
    calkit_1port_dirname = os.sep.join((calkit_dirname, calkit_name))
    calkit_2port_dirname = os.sep.join((calkit_dirname, calkit_name + "_" + calkit_name))
    if not os.path.exists(calkit_1port_dirname):
        os.makedirs(calkit_1port_dirname)
    if not os.path.exists(calkit_2port_dirname):
        os.makedirs(calkit_2port_dirname)

    tree = ET.parse(xkt_filename)
    calkit = tree.getroot()
    for heading in calkit:
        if heading.tag == "StandardList":
            standards = heading
            for standard in standards:
                if standard.tag == "ShortStandard":
                    name = standard.find("Label").text
                    fmin = max(fstart, float(standard.find("MinimumFrequencyHz").text))
                    fmax = min(fstop, float(standard.find("MaximumFrequencyHz").text))
                    f = np.arange(fmin, fmax, fstep).reshape(-1, 1, 1)
                    L0 = float(standard.find("L0").text)
                    L1 = float(standard.find("L1").text)
                    L2 = float(standard.find("L2").text)
                    L3 = float(standard.find("L3").text)
                    s = z2g(1j * 2 * np.pi * (L0 + L1 * f + L2 * f ** 2 + L3 * f ** 3))
                    group_delay = float(standard.find("Offset").find("OffsetDelay").text)
                    loss = float(standard.find("Offset").find("OffsetLoss").text)
                    z0 = float(standard.find("Offset").find("OffsetZ0").text)
                    s = s*offset2t(f, loss, group_delay, z0)**2
                    filename = os.sep.join((calkit_1port_dirname, name + ".s1p"))
                elif standard.tag == "OpenStandard":
                    name = standard.find("Label").text
                    fmin = max(fstart, float(standard.find("MinimumFrequencyHz").text))
                    fmax = min(fstop, float(standard.find("MaximumFrequencyHz").text))
                    f = np.arange(fmin, fmax, fstep).reshape(-1, 1, 1)
                    C0 = float(standard.find("C0").text)
                    C1 = float(standard.find("C1").text)
                    C2 = float(standard.find("C2").text)
                    C3 = float(standard.find("C3").text)
                    s = z2g(1 / (2 * np.pi * (C0 + C1 * f + C2 * f ** 2 + C3 * f ** 3)))
                    group_delay = float(standard.find("Offset").find("OffsetDelay").text)
                    loss = float(standard.find("Offset").find("OffsetLoss").text)
                    z0 = float(standard.find("Offset").find("OffsetZ0").text)
                    s = s * offset2t(f, loss, group_delay, z0) ** 2
                    filename = os.sep.join((calkit_1port_dirname, name + ".s1p"))
                elif standard.tag == "FixedLoadStandard":
                    name = standard.find("Label").text
                    fmin = max(fstart, float(standard.find("MinimumFrequencyHz").text))
                    fmax = min(fstop, float(standard.find("MaximumFrequencyHz").text))
                    f = np.arange(fmin, fmax, fstep).reshape(-1, 1, 1)
                    s = 0.00*f
                    group_delay = float(standard.find("Offset").find("OffsetDelay").text)
                    loss = float(standard.find("Offset").find("OffsetLoss").text)
                    z0 = float(standard.find("Offset").find("OffsetZ0").text)
                    if group_delay > 0.0:
                        s = s * offset2t(f, loss, group_delay, z0) ** 2
                    filename = os.sep.join((calkit_1port_dirname, name + ".s1p"))
                elif standard.tag == "ThruStandard":
                    name = standard.find("Label").text
                    fmin = max(fstart, float(standard.find("MinimumFrequencyHz").text))
                    fmax = min(fstop, float(standard.find("MaximumFrequencyHz").text))
                    f = np.arange(fmin, fmax, fstep).reshape(-1, 1, 1)
                    s = np.tile(np.array([[0, 1], [1, 0]]), (f.size, 1, 1))
                    group_delay = float(standard.find("Offset").find("OffsetDelay").text)
                    loss = float(standard.find("Offset").find("OffsetLoss").text)
                    z0 = float(standard.find("Offset").find("OffsetZ0").text)
                    if group_delay > 0.0:
                        s = s * offset2t(f, loss, group_delay, z0)
                    filename = os.sep.join((calkit_2port_dirname, name + ".s2p"))
                elif standard.tag == "IsolationStandard":
                    name = standard.find("Label").text
                    fmin = max(fstart, float(standard.find("MinimumFrequencyHz").text))
                    fmax = min(fstop, float(standard.find("MaximumFrequencyHz").text))
                    f = np.arange(fmin, fmax, fstep).reshape(-1, 1, 1)
                    s = np.tile(np.array([[0, 1], [1, 0]]), (f.size, 1, 1))
                    group_delay = float(standard.find("Offset").find("OffsetDelay").text)
                    loss = float(standard.find("Offset").find("OffsetLoss").text)
                    z0 = float(standard.find("Offset").find("OffsetZ0").text)
                    s = s * offset2t(f, loss, group_delay, z0)
                    filename = os.sep.join((calkit_2port_dirname, name + ".s2p"))
                else:
                    raise ValueError("Unsupported Calkit Standard")
                ntwk = network.Network(f=f.reshape(-1)/1e9, s=s, z0=z0)
                ntwk.write_touchstone(filename, form="ma")


if __name__ == "__main__":
    xkt2calkit(os.sep.join((Settings().data_root, "calkits", "pna_calkits", "85033DE.xkt")),
               # fstart=0, fstop=10e9, fstep=10e6)
               fstart=1e9-10e3, fstop=1e9+10e3, fstep=5e3)
