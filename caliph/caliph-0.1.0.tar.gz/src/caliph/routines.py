import numpy as _np

def pH_calibration(pH_measured, temperature=25.0):
    """Calculates calibration curve y = m*x + c for two point
    pH calibration. Assumes pH 4.01 and pH 10.01 buffer solutions are used

    Args:
        pH_measured (float): pH measured for pH 4 and pH 10 solutions
        temperature (float, optional): Measurement temperature in C. Defaults to 25.

    Returns:
        array: calibration slope and offset
    """    

    temp = _np.array([ 0,  5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80,
        85, 90, 95])

    pH4 = _np.array([4.01, 4.  , 4.  , 4.  , 4.  , 4.01, 4.02, 4.03, 4.04, 4.05, 4.06,
        4.07, 4.09, 4.11, 4.12, 4.14, 4.16, 4.17, 4.19, 4.2 ])

    pH10 = _np.array([10.32, 10.25, 10.18, 10.12, 10.06, 10.01,  9.96,  9.92,  9.88,
            9.85,  9.82,  9.79,  9.77,  9.76,  9.75,  9.74,  9.73,  9.74,
            9.75,  9.76])

    pH4_tcomp = _np.interp(temperature,temp, pH4)
    pH10_tcomp = _np.interp(temperature,temp, pH10)
    pH_actual = _np.array([pH4_tcomp, pH10_tcomp])
    conv_fit = _np.polyfit(pH_measured, pH_actual, 1)
    return conv_fit


def pH_convert(pH_measured, calibration):
        """Converts measured pH values to calibrated ones

        Args:
            pH_measured (array): measured pH values
            calibration (array): calibration constants [slope, offset] 

        Returns:
            array: calibrated pH
        """        
        calib_func = _np.poly1d(calibration)
        pH_calibrated = calib_func(pH_measured)
        return pH_calibrated


