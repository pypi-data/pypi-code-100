import sys
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class filedialogdemo(QWidget):
   def __init__(self, convert, parent = None):
      self.convert = convert
      super(filedialogdemo, self).__init__(parent)
		
      layout = QVBoxLayout()

      self.instructions1 = [QLabel("Step 1:"), QLabel("Find the file you downloaded from ManageBac, and we'll convert it to CSV for you.")]
      for instruction in self.instructions1:
         layout.addWidget(instruction)
      self.source = QPushButton("Choose *.xls file")
      self.source.clicked.connect(self.getfile)
		
      layout.addWidget(self.source)
	
      self.instructions2 = [QLabel("Step 2:"), QLabel("Take the output provided below, copy and paste into Google Sheets")]
      for instruction in self.instructions2:
         layout.addWidget(instruction)

      self.contents = QTextEdit()
      doc = self.contents.document()
      option = doc.defaultTextOption()
      option.setFlags(QTextOption.Flag.ShowTabsAndSpaces)
      layout.addWidget(self.contents)

      self.done_btn = QPushButton("Got it! Done")
      self.done_btn.clicked.connect(self.close)
      self.instructions3 = [QLabel("Step 3:"), QLabel("Once pasted into Google Sheets, use Data -> Split Text into Columns"), self.done_btn]
      for instruction in self.instructions3:
         layout.addWidget(instruction)

      self.setLayout(layout)

      self.setWindowTitle("Convert MB Excel Download to CSV")
		
   def getfile(self):
      fname = QFileDialog.getOpenFileName(self, 'Open file', 
         '~/Downloads',"Excel files (*.xls)")
      csv = self.convert(fname[0])
      self.contents.setText(csv)


def gui_main(convert):
   app = QApplication(sys.argv)
   ex = filedialogdemo(convert)
   ex.show()
   sys.exit(app.exec())


if __name__ == '__main__':
   gui_main()

