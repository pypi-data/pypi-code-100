import logging
import sys
from collections import OrderedDict
import inspect

from PySide2 import QtCore
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import QApplication, QMainWindow, QFrame, QWidget, QLabel, QSplitter
from PySide2.QtWidgets import QVBoxLayout, QSizePolicy

from sknrf.settings import InstrumentFlag, instrument_icon_map
from sknrf.model.base import AbstractModel
from sknrf.model.runtime import RuntimeThread
from sknrf.model.sequencer.base import ActionItemDataType, ActionItemDataRole, ActionItem
from sknrf.view.desktop.sequencer.widgets import ActionTreeView
from sknrf.view.base import AbstractView
from sknrf.view.desktop.sideview.base import AbstractSideView, SideViewTabWidget, LogSideView
from sknrf.view.desktop.sideview.QLauncherSideView import Ui_launcherSideViewFrame
from sknrf.view.desktop.launcher.QLauncher import Ui_launcherFrame
from sknrf.view.desktop.launcher.QLauncherMenu import Ui_launcherMenu

from sknrf.view.desktop import calibration


logger = logging.getLogger(__name__)


class LauncherTreeView(ActionTreeView):

    def currentChanged(self, current, previous):
        """Updates the info edit widget with documentation from the current selected item.

        Args:
            current (ActionItem): current selected item
            previous (ActionItem): previous selected item
        """
        super(LauncherTreeView, self).currentChanged(current, previous)
        item = self.model().itemFromIndex(current)
        if item and self._info_edit:
            action_type = item.data(ActionItemDataRole.TypeRole.value)
            obj = None
            if action_type == ActionItemDataType.Module:
                obj = item.data(ActionItemDataRole.ModuleRole.value)
            elif action_type == ActionItemDataType.Class or action_type == ActionItemDataType.Function:
                obj = item.data(ActionItemDataRole.ObjectRole.value)
            elif action_type == ActionItemDataType.Method:
                obj = getattr(item.data(ActionItemDataRole.ObjectRole.value), item.data(Qt.DisplayRole))
            doc_text = str(inspect.getdoc(obj))
            doc_text = '<html><b><font size="3">' + obj.__name__ + "</font></b><br><br>" + doc_text + "</html>"
            self._info_edit.setText(doc_text.replace("\n", "<br>"))


class LauncherSideView(AbstractSideView, QFrame, Ui_launcherSideViewFrame):
    """The launcher tab in the Sidebar Widget.

    A Sidebar Widget with the following contents:
        * Application libraries
        * Application Info Display
    """
    def __init__(self, model, parent=None, base_class=AbstractView):
        super(LauncherSideView, self).__init__(parent=parent)
        self.setupUi(self)
        self._base_class = base_class
        self.sidebar_tab_map = {}
        self.sidebar_vbl_map = {}
        self.sidebar_tree_map = {}
        self.set_model(model)

    def set_model(self, model):
        super(LauncherSideView, self).set_model(model)
        self.sidebar_tab_map = {}
        self.sidebar_vbl_map = {}
        self.sidebar_tree_map = {}

        for package_name, package_list in model.package_map().items():
            self.sidebar_tab_map[package_name] = QWidget()
            self.sidebar_tab_map[package_name].setObjectName(package_name + "Tab")
            self.sidebar_vbl_map[package_name] = QVBoxLayout(self.sidebar_tab_map[package_name])
            self.sidebar_vbl_map[package_name].setContentsMargins(0, 0, 0, 0)
            self.sidebar_tree_map[package_name] = LauncherTreeView(self.sidebar_tab_map[package_name],
                                                                 package=package_list[0],
                                                                 base_class=self._base_class,
                                                                 enable_methods=False)
            self.sidebar_tree_map[package_name].setDragEnabled(True)
            self.sidebar_tree_map[package_name].setHeaderHidden(True)
            self.sidebar_tree_map[package_name].setObjectName(package_name + "TreeView")
            self.sidebar_tree_map[package_name].header().setDefaultSectionSize(0)
            self.sidebar_vbl_map[package_name].addWidget(self.sidebar_tree_map[package_name])
            self.actionTabWidget.addTab(self.sidebar_tab_map[package_name], package_name)
            self.sidebar_tree_map[package_name].set_package(package_list[0])
            self.sidebar_tree_map[package_name].set_info_edit(self.infoEdit)

    def update(self, *args):
        super(LauncherSideView, self).update()


class Launcher(QFrame, Ui_launcherFrame):

    def __init__(self, parent=None):
        super(Launcher, self).__init__(parent=parent)
        self.setupUi(self)
        self.gbl = self.iconGridLayout
        self._model = None

    def model(self):
        return self._model

    def set_model(self, model):
        port_nums = model._port_nums
        instruments = model._instruments
        all_instruments = [InstrumentFlag.LFSOURCE, InstrumentFlag.LFRECEIVER, InstrumentFlag.LFZTUNER,
                           InstrumentFlag.RFSOURCE, InstrumentFlag.RFRECEIVER, InstrumentFlag.RFZTUNER]

        while self.gbl.count() > 0:
            item = self.gbl.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            self.gbl.removeItem(item)

        for port_index, port_num in enumerate(port_nums):
            port_label = QLabel("Port %s:" % (port_num,))
            port_label.setStyleSheet("font: bold 24pt \"Helvetica\";")
            self.gbl.addWidget(port_label, 0, port_index)
            required_instruments = instruments[port_index]
            for instrument_index, instrument in enumerate(all_instruments):
                icon = QIcon(instrument_icon_map[instrument])
                label = QLabel("", parent=self)
                label.setPixmap(QPixmap(icon.pixmap(QtCore.QSize(128, 128))))
                label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                label.setEnabled(bool(instrument & required_instruments))
                self.gbl.addWidget(label, instrument_index + 1, port_index)
        self._model = model


class LauncherMenuView(AbstractView, QMainWindow, Ui_launcherMenu):
    """Launcher Menu View Widget for launching external applications

        Keyword Args:
            parent (QWidget): Parent GUI container
    """

    def __init__(self, device_model, datagroup_model, package_map, parent=None):
        super(LauncherMenuView, self).__init__(parent=parent)
        self.setupUi(self)
        # Content Splitter
        self.splitter = QSplitter(self.centralwidget)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.splitter.setSizePolicy(size_policy)
        self.sideViewTabWidget = SideViewTabWidget(parent=self.centralwidget)
        # log_side_view = LogSideView(AbstractModel, logger, parent=self.sideViewTabWidget)

        self.runtime_thread = RuntimeThread()
        self.runtime_model = None

        # Initialize Views
        self.sidebar_views = OrderedDict((("Launcher", LauncherSideView(model=package_map, parent=self.sideViewTabWidget)),))
                                          # ("Log", log_side_view)))
        for tab_name, tab_widget in self.sidebar_views.items():
            self.sideViewTabWidget.addTab(tab_widget, tab_name)
        self.launcher_view = Launcher(parent=self.centralwidget)
        self.runtime_view = None
        self.menu = None

        self.splitter.addWidget(self.sideViewTabWidget)
        self.splitter.addWidget(self.launcher_view)
        self.layout = self.centralwidget.layout()
        self.layout.addWidget(self.splitter)

        self.connect_signals()

    def connect_signals(self):
        tree_map = self.sidebar_views["Launcher"].sidebar_tree_map
        for name, tree in tree_map.items():
            tree.clicked.connect(self.set_preview)
        self.launcher_view.buttonBox.accepted.connect(self.open_menu)

    def disconnect_signals(self):
        pass

    def set_preview(self, item):
        action_type = item.data(ActionItemDataRole.TypeRole.value)
        if action_type == ActionItemDataType.Module:
            return
        elif action_type == ActionItemDataType.Class or action_type == ActionItemDataType.Function:
            class_ = item.data(ActionItemDataRole.ObjectRole.value)
            self.launcher_view.set_model(class_)

    def open_menu(self):
        class_ = self.launcher_view.model()
        if class_ is None:
            return
        self.menu = class_(parent=None)
        self.menu.setAttribute(Qt.WA_DeleteOnClose)
        self.menu.destroyed.connect(self.window().update)
        self.menu.showMaximized()

    def update(self, sideview=False, preview=False):
        super(LauncherMenuView, self).update()
        all_ = not (sideview or preview)

        if sideview or all_:
            self.sideViewTabWidget.currentWidget().update()
        if preview or all_:
            self.launcher_view.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    AbstractModel.init()
    package_map = OrderedDict((("Calibration", [calibration]),))
    side_model = SequencerSideModel(package_map)
    form = LauncherMenuView(AbstractModel.device_model(), AbstractModel.datagroup_model(), side_model)
    form.showMaximized()
    app.exec_()