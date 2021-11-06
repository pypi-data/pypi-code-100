# import os
# from itertools import combinations
#
# import numpy as np
#
# from sknrf.device.instrument.rfsource import NoRFSource
# from sknrf.model.sequencer.transform import Instrument
# from sknrf.model.calibration.base import calkit_connector_map
# from sknrf.model.calibration.impedance.match import ImpedanceMatchModel
# from sknrf.view.desktop.calibration.impedance.base import ImpedanceCalibrationWizard
# from sknrf.view.desktop.calibration.impedance.base import ImpedanceConnectionPage, ImpedanceInstrumentPage, ImpedanceIntroductionPage
# from sknrf.view.desktop.calibration.impedance.base import ImpedanceContentPage, ImpedanceConclusionPage
#
#
# class ImpedanceMatchConnectionPage(ImpedanceConnectionPage):
#
#     def isComplete(self):
#         return len(self.wizard().port_indices()) > 1
#
#
# class ImpedanceMatchInstrumentPage(ImpedanceInstrumentPage):
#
#     def __init__(self):
#         super(ImpedanceMatchInstrumentPage, self).__init__()
#         self.add_instrument(Instrument.ALL.value)
#
#
# class ImpedanceMatchIntroductionPage(ImpedanceIntroductionPage):
#
#     def __init__(self):
#         super(ImpedanceMatchIntroductionPage, self).__init__()
#         self.setTitle("Impedance Match Calibration")
#         self.setSubTitle("Impedance Match Calibration")
#
#         self.add_requirement("LF Source is turned off.")
#         self.add_requirement("RF Source is connected to each port.")
#
#         self.add_recommendation("RF ZTuner should be matched to the Load impedance.")
#
#     def check_requirements(self):
#         super(ImpedanceMatchIntroductionPage, self).check_requirements()
#         for port_index in self.wizard().port_indices():
#             port = self.wizard().model().device_model().ports[port_index]
#             port.lfsource.on = False
#             self.requirementsCheckBoxList[0].setChecked(not port.lfsource.on)
#             if not isinstance(port.rfsource, NoRFSource):
#                 self.requirementsCheckBoxList[1].setChecked(True)
#             else:
#                 self.requirementsCheckBoxList[1].setChecked(False)
#
#     def check_recommendations(self):
#         super(ImpedanceMatchIntroductionPage, self).check_recommendations()
#         for port_index in self.wizard().port_indices():
#             port = self.wizard().model().device_model().ports[port_index]
#             if np.all(np.equal(port.rfztuner.z, 50)):
#                 self.recommendationsCheckBoxList[0].setChecked(True)
#             else:
#                 self.recommendationsCheckBoxList[0].setChecked(False)
#
#     def isComplete(self):
#         return True
#
#
# class ImpedanceMatchContentPage(ImpedanceContentPage):
#     pass
#
#
# class ImpedanceMatchConclusionPage(ImpedanceConclusionPage):
#     pass
#
#
# class ImpedanceMatchWizard(ImpedanceCalibrationWizard):
#     def __init__(self, model=None):
#         super(ImpedanceMatchWizard, self).__init__()
#
#         self.addPage(ImpedanceMatchConnectionPage())
#         self.addPage(ImpedanceMatchInstrumentPage())
#         self.addPage(ImpedanceMatchIntroductionPage())
#         self.addPage(ImpedanceMatchConclusionPage())
#
#         if model is None:
#             model = ImpedanceMatchModel()
#         self.set_model(model)
#         self.connect_signals()
#
#     def initialize_content_pages(self):
#         super(ImpedanceMatchWizard, self).initialize_content_pages()
#         pages = list()
#         self._model.ideal_ntwks.clear()
#         self._model.measured_ntwks.clear()
#         for combo in combinations(self.port_indices(), 2):
#             port_num1, port_num2 = combo[0] + 1, combo[1] + 1
#             port_id1, port_id2 = "Port%d" % (port_num1,), "Port%d " % (port_num2,)
#             port_connector1 = self._model.port_connectors[combo[0]]
#             port_connector2 = self._model.port_connectors[combo[1]]
#             calkit_connector1 = self._model.calkit_connectors[combo[0]]
#             calkit_connector2 = self._model.calkit_connectors[combo[1]]
#             calkit_filepath = calkit_connector_map[calkit_connector1] + "_" + calkit_connector2
#             contents = [port_id1] + ["Adapter"] * int(port_connector1 != calkit_connector1) + \
#                        ["Thru"] + \
#                        ["Adapter"] * int(port_connector2 != calkit_connector2) + [port_id2]
#             pages.append(
#                 ImpedanceMatchContentPage("Thru_%d_%d" % (port_num1, port_num2), contents, optional=False))
#             self.set_ideal(contents.index("Thru"), os.sep.join((calkit_filepath, "Thru.s2p")), pages[-1])
#         self.insert_content_pages(pages)
#
#     def insert_optional_content_page(self):
#         raise NotImplementedError("Optional content pages are not allowed for this calibration.")
