from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QHBoxLayout

from sknrf.view.desktop.sideview.base import AbstractSideView
from sknrf.view.desktop.device.tile import DUTTileGroupView


class DUTSideView(AbstractSideView, QWidget):

    def __init__(self, model, parent=None):
        super(DUTSideView, self).__init__(parent=parent)
        self.setObjectName("dutTab")
        self.dut_panel_view = DUTTileGroupView(model.device_model().duts, model.device_model(), parent=self)

        for index in range(len(model.device_model().duts)):
            self.dut_panel_view.tile_map["DUT" + str(index)].menuButton.setIcon(QIcon(":/PNG/black/64/dut.png"))

        self.vbl = QHBoxLayout()
        self.vbl.setContentsMargins(0, 0, 0, 0)
        self.vbl.setSpacing(0)
        self.vbl.addWidget(self.dut_panel_view)
        self.setLayout(self.vbl)

    def set_model(self, model):
        self.dut_panel_view.deleteLater()
        self.dut_panel_view = DUTTileGroupView(model.device_model().duts, model.device_model(), parent=self)
        self.vbl.insertWidget(1, self.dut_panel_view)
        self.setLayout(self.vbl)

    def update(self, *args, values=True):
        super(DUTSideView, self).update()
        all_ = not(values)

        if values or all_:
            self.dut_panel_view.update()
