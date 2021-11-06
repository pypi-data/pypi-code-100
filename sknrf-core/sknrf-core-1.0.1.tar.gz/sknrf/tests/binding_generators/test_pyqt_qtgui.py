import sys
from PyQt4 import QtGui
from foolib import FooMenu

app = QtGui.QApplication(sys.argv)

form = FooMenu(parent=None)
form.show()

sys.exit(app.exec_())