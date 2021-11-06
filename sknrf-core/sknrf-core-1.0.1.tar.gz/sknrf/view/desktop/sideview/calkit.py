from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QHBoxLayout

from sknrf.view.desktop.sideview.base import AbstractSideView
from sknrf.view.desktop.device.tile import PortTileGroupView


class CalkitSideView(AbstractSideView, QWidget):

    def __init__(self, model, parent=None):
        super(CalkitSideView, self).__init__(parent=parent)
        self.setObjectName("calkitTab")
        self.calkit_panel_view = PortTileGroupView(model.device_model().ports[0], model.device_model(), parent=self)

        self.calkit_panel_view.tile_map["lfsource"].menuButton.setIcon(QIcon(":/PNG/black/64/lfsource_ref.png"))
        self.calkit_panel_view.tile_map["lfreceiver"].menuButton.setIcon(QIcon(":/PNG/black/64/lfreceiver_ref.png"))
        self.calkit_panel_view.tile_map["lfztuner"].menuButton.setIcon(QIcon(":/PNG/black/64/lfztuner_ref.png"))
        self.calkit_panel_view.tile_map["rfsource"].menuButton.setIcon(QIcon(":/PNG/black/64/rfsource_ref.png"))
        self.calkit_panel_view.tile_map["rfreceiver"].menuButton.setIcon(QIcon(":/PNG/black/64/rfreceiver_ref.png"))
        self.calkit_panel_view.tile_map["rfztuner"].menuButton.setIcon(QIcon(":/PNG/black/64/rfztuner_ref.png"))

        self.hbl = QHBoxLayout()
        self.hbl.setContentsMargins(0, 0, 0, 0)
        self.hbl.setSpacing(0)
        self.hbl.addWidget(self.calkit_panel_view)
        self.setLayout(self.hbl)

    def set_model(self, model):
        self.calkit_panel_view.deleteLater()
        self.calkit_panel_view = PortTileGroupView(model.device_model().ports[0], model.device_model(), parent=self)
        self.hbl.addWidget(self.calkit_panel_view)
        self.setLayout(self.hbl)

    def update(self, *args, values=True):
        super(CalkitSideView, self).update()
        all_ = not(values)

        if values or all_:
            self.calkit_panel_view.update()