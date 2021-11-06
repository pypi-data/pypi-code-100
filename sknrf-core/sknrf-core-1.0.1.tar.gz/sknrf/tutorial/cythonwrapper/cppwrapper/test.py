import sys

from rect import Rectangle
import cppwrapper
from qdialog import PyQDialog

from PySide import QtCore
from PySide import QtGui


if __name__ == "__main__":
    print("Calling built-in wrapped C++ functions")
    vect = cppwrapper.load_vector()
    cppwrapper.print_vector(vect)

    print("Calling user-defined wrapped C++ class")
    rec = Rectangle(1, 2, 3, 4)
    print(rec.get_area())
    print(rec.x0)
    rec.x0 = 2
    print(rec.x0)

    print("Calling user-defined wrapped Qt C++ Class")
    app = QtGui.QApplication(sys.argv)
    form = PyQDialog()
    # form.show()
    print(sys.argv)
    app.exec_()