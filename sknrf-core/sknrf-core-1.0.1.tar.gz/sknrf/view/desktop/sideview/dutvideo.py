from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QHBoxLayout

from sknrf.view.desktop.sideview.base import AbstractSideView
from sknrf.view.desktop.device.tile import DUTVideoGroupView


class DUTVideoSideView(AbstractSideView, QWidget):

    def __init__(self, model, parent=None):
        super(DUTVideoSideView, self).__init__(parent=parent)
        self.setObjectName("videoTab")
        self.video_panel_view = DUTVideoGroupView(model.device_model().duts[0].video, model.device_model(), parent=self)

        for index in range(len(model.device_model().duts[0].video)):
            self.video_panel_view.tile_map["video" + str(index)].menuButton.setIcon(QIcon(":/PNG/black/64/video.png"))

        self.vbl = QHBoxLayout()
        self.vbl.setContentsMargins(0, 0, 0, 0)
        self.vbl.setSpacing(0)
        self.vbl.addWidget(self.video_panel_view)
        self.setLayout(self.vbl)

    def set_model(self, model):
        self.video_panel_view.deleteLater()
        self.video_panel_view = DUTVideoGroupView(model.device_model().duts[0].video, model.device_model(), parent=self)
        self.vbl.insertWidget(1, self.video_panel_view)
        self.setLayout(self.vbl)

    def update(self, *args, values=True):
        super(DUTVideoSideView, self).update()
        all_ = not (values,)

        if values or all_:
            self.video_panel_view.update()
