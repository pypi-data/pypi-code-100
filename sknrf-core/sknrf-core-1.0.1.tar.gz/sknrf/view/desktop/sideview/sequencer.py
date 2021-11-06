from PySide2.QtWidgets import QFrame, QWidget
from PySide2.QtWidgets import QVBoxLayout

from sknrf.model.base import AbstractModel
from sknrf.view.desktop.sideview.base import AbstractSideView
from sknrf.view.desktop.sideview.QSequencerSideView import Ui_sequencerSideViewFrame
from sknrf.view.desktop.sequencer.widgets import ActionTreeView


class SequencerSideView(QFrame, AbstractSideView, Ui_sequencerSideViewFrame):
    """The sequencer tab in the Sidebar Widget.

    A Sidebar Widget with the following contents:
        * Sequencer libraries
        * Seqence Info Display
    """

    def __init__(self, model, parent=None, base_class=AbstractModel, enable_methods=True):
        super(SequencerSideView, self).__init__(parent)
        self.setupUi(self)
        self._base_class = base_class
        self._enable_methods = enable_methods
        self.set_model(model)

    def set_model(self, model):
        super(SequencerSideView, self).set_model(model)
        self.sidebar_tab_map = {}
        self.sidebar_vbl_map = {}
        self.sidebar_tree_map = {}

        for package_name, package_list in model.package_map().items():
            self.sidebar_tab_map[package_name] = QWidget()
            self.sidebar_tab_map[package_name].setObjectName(package_name + "Tab")
            self.sidebar_vbl_map[package_name] = QVBoxLayout(self.sidebar_tab_map[package_name])
            self.sidebar_vbl_map[package_name].setContentsMargins(0, 0, 0, 0)
            self.sidebar_tree_map[package_name] = ActionTreeView(self.sidebar_tab_map[package_name],
                                                                 package=package_list[0],
                                                                 base_class=self._base_class,
                                                                 enable_methods=self._enable_methods)
            self.sidebar_tree_map[package_name].setDragEnabled(True)
            self.sidebar_tree_map[package_name].setHeaderHidden(True)
            self.sidebar_tree_map[package_name].setObjectName(package_name + "TreeView")
            self.sidebar_tree_map[package_name].header().setDefaultSectionSize(0)
            self.sidebar_vbl_map[package_name].addWidget(self.sidebar_tree_map[package_name])
            self.actionTabWidget.addTab(self.sidebar_tab_map[package_name], package_name)
            self.sidebar_tree_map[package_name].set_package(package_list[0])
            self.sidebar_tree_map[package_name].set_info_edit(self.infoEdit)

    def update(self, *args):
        super(SequencerSideView, self).update()