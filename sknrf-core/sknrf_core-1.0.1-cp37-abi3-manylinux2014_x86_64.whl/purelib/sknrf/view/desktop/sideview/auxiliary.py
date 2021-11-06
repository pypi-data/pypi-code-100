from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QHBoxLayout

from sknrf.view.desktop.sideview.base import AbstractSideView
from sknrf.view.desktop.device.tile import AuxiliaryGroupView


class AuxiliarySideView(AbstractSideView, QWidget):

    def __init__(self, model, parent=None):
        super(AuxiliarySideView, self).__init__(parent=parent)
        self.setObjectName("auxTab")
        self.aux_panel_view = AuxiliaryGroupView(model.device_model().aux, model.device_model(), parent=self)

        self.aux_panel_view.tile_map["pm"].menuButton.setIcon(QIcon(":/PNG/black/64/pm.png"))
        self.aux_panel_view.tile_map["sa"].menuButton.setIcon(QIcon(":/PNG/black/64/sa.png"))
        self.aux_panel_view.tile_map["vna"].menuButton.setIcon(QIcon(":/PNG/black/64/vna.png"))

        self.vbl = QHBoxLayout()
        self.vbl.setContentsMargins(0, 0, 0, 0)
        self.vbl.setSpacing(0)
        self.vbl.addWidget(self.aux_panel_view)
        self.setLayout(self.vbl)

    def set_model(self, model):
        self.aux_panel_view.deleteLater()
        self.aux_panel_view = AuxiliaryGroupView(model.device_model().aux, model.device_model(), parent=self)
        self.vbl.insertWidget(1, self.aux_panel_view)
        self.setLayout(self.vbl)

    def update(self, *args, values=True):
        super(AuxiliarySideView, self).update()
        all_ = not(values)

        if values or all_:
            self.aux_panel_view.update()
