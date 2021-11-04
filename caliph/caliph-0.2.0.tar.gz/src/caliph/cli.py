# from argparse import ArgumentParser
from .routines import pH_calibration, pH_convert
from numpy import savetxt, loadtxt
import fire
import sys


def calib_cli(ph4, ph10, temperature=25, save=False):
    """Calculates calibration curve for a two point pH calibration.

    Note: Assumes pH 4.01 and pH 10.01 buffer solutions are used, and the calibration curve is of the form y = m*x + c where [m, c] is returned.

    Args:
        ph4 (float): pH measured for pH 4.01 buffer solution
        ph10 (float): pH measured for pH 10.01 buffer solution
        temperature (float, optional): Measurement temperature in C. Defaults to 25.
        save (bool, optional): Save calibration data to calib.dat. Defaults to False.
    """

    print(f"measured pHs are {ph4} {ph10}, temperature is {temperature} C")

    calib = pH_calibration([ph4, ph10], temperature)
    print(f"Calibration is {calib}")
    if save:
        print("Saving to calib.dat")
        savetxt("calib.dat", calib, delimiter="\t")


def calib():
    fire.Fire(calib_cli)


def convert_cli(ph, file=True, slope=None, offset=None):
    """Converts a measured pH to a calibrated value.

    Note: Both slope and offset must be set if the calib.dat file is not being used

    Args:
        ph (array/float): Array or single pH measurement
        file (bool, optional): Reads calib.dat in current folder to get calibration constants. Defaults to True.
        slope (float, optional): Slope correction. Defaults to None.
        offset (float, optional): Offset correction. Defaults to None.
    """
    if file and (slope is None and offset is None):
        try:
            calibration = loadtxt("./calib.dat", delimiter="\t")
        except FileNotFoundError:
            print("Error, calib.dat not found")
            sys.exit(1)
        except OSError:
            print("OS error occurred trying to open calib.dat")
            sys.exit(1)

        except Exception as err:
            print(f"Unexpected error opening calib.dat is", repr(err))
            sys.exit(1)

    elif slope is None or offset is None:
        print(
            "Error either calib.dat is used or calibration array [slope, offset] must be passed as an argument"
        )
        sys.exit(1)

    else:
        calibration = [slope, offset]
    ph_calib = pH_convert(ph, calibration)

    print(f"Calibrated pH: {ph_calib}\ncalibration is {calibration}")


def conv():
    fire.Fire(convert_cli)
