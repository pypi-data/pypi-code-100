"""
    ============================
    Impedance Calibration Models
    ============================

    This module defines the calibration models for the impedance calibrations.

    See Also
    ----------
    sknrf.view.desktop.calibration.impedance.base, sknrf.model.base.AbstractModel
"""
import logging
import abc
import re

from sknrf.model.calibration.base import AbstractCalibrationModel
from sknrf.utilities.numeric import AttributeInfo

logger = logging.getLogger(__name__)


class AbstractImpedanceModel(AbstractCalibrationModel):
    """A calibration model for vector calibrations.

        See Also
        ----------
        AbstractCalibrationModel
    """

    def __init__(self):
        super(AbstractImpedanceModel, self).__init__()
        self.measured_ntwks = dict()
        self.ideal_ntwks = dict()

    @abc.abstractmethod
    def calculate(self):
        return True

    @abc.abstractmethod
    def apply_cal(self):
        pass
