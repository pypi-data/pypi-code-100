import logging

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QTreeView

logger = logging.getLogger()


class DatagroupTreeView(QTreeView):

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Delete:
            index = self.currentIndex()
            if index.parent().row() == -1:  # level 1
                self.model().removeRow(index, index.parent(), self.parent().datagroup_model())
            else:  # level 2
                pass

