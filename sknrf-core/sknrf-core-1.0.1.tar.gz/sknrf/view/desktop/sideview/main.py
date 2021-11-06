from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QVBoxLayout

from sknrf.view.desktop.sideview.base import AbstractSideView
from sknrf.view.desktop.settings.settings import SettingsFrame
from sknrf.app.dataviewer.view.dataset.dataset import DatasetEquationView


class MainSideView(AbstractSideView, QWidget):
    """The default tab in the Sidebar Widget.

    A Sidebar Widget with the following contents:
        * Frequency-Domain and Time-Domain sweep settings.
        * Datagroup and Dataset selection.
        * Dataset equation table.

        Args:
            dataset_model (DatasetModel): The current selected dataset.

        Keyword Args:
            parent (QWidget): Parent GUI container
    """

    def __init__(self, model, parent=None):
        super(MainSideView, self).__init__(parent=parent)
        self.setObjectName("mainTab")
        dataset = model.datagroup_model()["Single"].dataset("Single")
        self.settings_frame = SettingsFrame(parent=self)
        self.equation_frame = DatasetEquationView(dataset, parent=self)

        self.vbl = QVBoxLayout()
        self.vbl.setContentsMargins(0, 0, 0, 0)
        self.vbl.setSpacing(0)
        self.vbl.addWidget(self.settings_frame)
        self.vbl.addWidget(self.equation_frame)
        self.setLayout(self.vbl)

    def set_model(self, model):
        super(MainSideView, self).set_model(model)
        dataset = model.datagroup_model()["Single"].dataset("Single")
        self.equation_frame.set_model(dataset)

    def update(self, *args, settings=False, equation=False):
        super(MainSideView, self).update()
        all_ = not(settings)

        if settings or all_:
            self.settings_frame.update()
        if equation or all_:
            self.equation_frame.update()
