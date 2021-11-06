import os
import logging

from PySide2 import QtCore
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QFrame
import matplotlib as mpl

from sknrf.app.dataviewer.view.image.QImageFrame import Ui_imageFrame

logger = logging.getLogger()


class ImageFrame(QFrame, Ui_imageFrame):

    def __init__(self, parent=None):
        super(ImageFrame, self).__init__(parent=parent)
        self.setupUi(self)
        icon_path = os.path.join(mpl.rcParams['datapath'], 'images')
        # self.panToolButton.setIcon(QIcon(os.path.join(icon_path, 'move.png')))
        self.zoomToolButton.setIcon(QIcon(os.path.join(icon_path, 'zoom_to_rect.png')))
        self.homeToolButton.setIcon(QIcon(os.path.join(icon_path, 'home.png')))
        self.subplotsToolButton.setIcon(QIcon(os.path.join(icon_path, 'subplots.png')))

    def connect_signals(self):
        self._parent.gctb().message.connect(self.set_coordinates)

    def disconnect_signals(self):
        self._parent.gctb().message.disconnect(self.set_coordinates)

    @QtCore.Slot(str)
    def set_coordinates(self, message):
        self.coordinatesLabel.setText(message)

    def update(self, plots=False):
        super(ImageFrame, self).update()
        self._parent.update(plots=plots)


