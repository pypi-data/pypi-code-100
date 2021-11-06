from PySide2.QtWidgets import QApplication
from PySide2.QtQuickWidgets import QQuickWidget
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QUrl
 
app = QApplication([])
view = QQuickView()
widget = QQuickWidget()
url = QUrl("tutorial3.qml")
 
# view.setSource(url)
widget.setSource(url)
widget.show()
# view.show()
app.exec_()
