from PySide2 import QtCore
from PySide2.QtWidgets import QTableView


class EquationTableView(QTableView):
    """The equation table.

        Parameters
        ----------
        parent : QWidget
               The tables parent widget.
    """
    def __init__(self, parent=None):
        super(EquationTableView, self).__init__(parent)
        self.show()

    @QtCore.Slot(object, object)
    def selectionChanged(self, selected, deselected):
        """The equation table.

            Parameters
            ----------
            parent : QWidget
                   The tables parent widget.
        """
        super(EquationTableView, self).selectionChanged(selected, deselected)
        indexes = selected.indexes()
        if indexes:
            self.model().set_selected(indexes[0])
