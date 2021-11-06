from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QHBoxLayout

from sknrf.view.desktop.sideview.base import AbstractSideView
from sknrf.view.desktop.device.tile import MIPIGroupView


class MIPISideView(AbstractSideView, QWidget):

    def __init__(self, model, parent=None):
        super(MIPISideView, self).__init__(parent=parent)
        self.setObjectName("DUTControlTab")
        self.mipi_panel_view = MIPIGroupView(model.device_model().duts[0], model.device_model(), parent=self)

        self.mipi_panel_view.tile_map["rffe"].menuButton.setIcon(QIcon(":/PNG/black/64/rffe.png"))
        self.mipi_panel_view.tile_map["et"].menuButton.setIcon(QIcon(":/PNG/black/64/et.png"))

        self.hbl = QHBoxLayout()
        self.hbl.setContentsMargins(0, 0, 0, 0)
        self.hbl.setSpacing(0)
        self.hbl.addWidget(self.mipi_panel_view)
        self.setLayout(self.hbl)

    def set_model(self, model):
        self.mipi_panel_view.deleteLater()
        self.mipi_panel_view = MIPIGroupView(model.device_model().duts[0], model.device_model(), parent=self)
        self.hbl.addWidget(self.mipi_panel_view)
        self.setLayout(self.hbl)

    def update(self, *args, values=True):
        super(MIPISideView, self).update()
        all_ = not(values)

        if values or all_:
            self.mipi_panel_view.update()
