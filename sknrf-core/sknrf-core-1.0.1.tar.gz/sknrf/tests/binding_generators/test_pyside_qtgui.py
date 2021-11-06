import sys
from PySide import QtGui
from foolib import FooMenu

app = QtGui.QApplication(sys.argv)

form = FooMenu(parent=None)
form.show()

sys.exit(app.exec_())