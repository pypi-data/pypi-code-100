"""
    =================================
    Impedance Match Calibration Model
    =================================

    This module defines the calibration models for the impedance match calibrations.

    See Also
    ----------
    sknrf.view.desktop.calibration.impedance.base.AbstractImpedanceModel, sknrf.model.base.AbstractModel
"""
# import logging
#
# import numpy as np
#
# from sknrf.device.base import Settings
# from sknrf.model.sequencer.transform import ImpedanceTransform
# from sknrf.model.calibration.impedance.base import AbstractImpedanceModel
# from sknrf.utilities.numeric import AttributeInfo
# from sknrf.utilities.rf import gamma2z, zp2z
#
# logger = logging.getLogger(__name__)
#
#
# class ImpedanceMatchModel(AbstractImpedanceModel):
#     """A calibration model for vector calibrations.
#
#         See Also
#         ----------
#         AbstractReceiverModel
#     """
#
#     def __init__(self):
#         super(ImpedanceMatchModel, self).__init__()
#
#     def __getstate__(self, state={}):
#         # Automatically save selected object ATTRIBUTES
#         if self.__class__ == ImpedanceMatchModel:
#             state = self.__dict__.copy()
#         state = super(ImpedanceMatchModel, self).__getstate__(state=state)
#         # ### Manually save selected object PROPERTIES here ###
#         return state
#
#     def __setstate__(self, state):
#         if self.__class__ == ImpedanceMatchModel:
#             self.__init__()
#         super(ImpedanceMatchModel, self).__setstate__(state)
#         # ### Manually load saved object ATTRIBUTES and PROPERTIES here ###
#
#     def __info__(self):
#         """ Initializes the display information of a device and stores information in self.info.
#         """
#         # Automatically generate info of ATTRIBUTES and PROPERTIES
#         if self.info is None and self.__class__ == ImpedanceMatchModel:
#             self.info = AttributeInfo.initialize(self, self.display_order)
#         super(ImpedanceMatchModel, self).__info__()
#         # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
#
#     def calculate(self):
#         try:
#             num_ports = len(self.port_indices)
#             self.calibration = [None]*num_ports
#             transforms = [t for t in self.device_model().transforms if hasattr(t, "_ABCD")]
#             data = np.tile(np.eye(2 * len(self.device_model().ports)), (Settings().f_points * Settings().t_points, 1, 1))
#             for transform in transforms:
#                 data = np.asarray([np.mat(abcd) * np.mat(data_) for abcd, data_ in zip(transform._ABCD, data)])
#             abcd = data
#
#             for measure_name, measured_thru in self.measured_ntwks.items():
#                 port_nums = measure_name.split("_")[1:]
#                 port_index1 = int(port_nums[0]) - 1
#                 port_index2 = int(port_nums[1]) - 1
#                 ideal_thru = self.ideal_ntwks[measure_name]
#                 # Todo: Remove the adapters from the measured thru using ideal thru
#                 zp = gamma2z(measured_thru.s[:, port_index1, port_index1])
#                 abcd2 = abcd[:, 2*port_index2:2*port_index2+2, 2*port_index2:2*port_index2+2]
#                 self.calibration[port_index2] = zp2z(zp, abcd2)
#                 zp = gamma2z(measured_thru.s[:, port_index2, port_index2])
#                 abcd1 = abcd[:, 2*port_index1:2*port_index1 + 2, 2*port_index1:2*port_index1 + 2]
#                 self.calibration[port_index1] = zp2z(zp,abcd1)
#         except:
#             logger.error("Unable to calculate calibration data", exc_info=True)
#             return False
#         else:
#             return True
#
#     def apply_cal(self):
#         transforms = self.device_model().transforms
#         for port_index in self.port_indices:
#             z = np.asarray(self.calibration[port_index]).reshape(-1)
#             transform = ImpedanceTransform("Impedance Match Calibration", ports=[port_index],
#                                            z=z, instrument_flags=self.instrument_flags)
#             transforms.insert(len(transforms), transform)