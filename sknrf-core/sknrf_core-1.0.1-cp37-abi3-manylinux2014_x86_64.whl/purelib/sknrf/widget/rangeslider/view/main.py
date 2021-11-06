import sys
from PySide2.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QWidget
from qrangeslider import QRangeSlider


def set_lower_index(index):
    print("set_lower_index")


def set_upper_index(index):
    print("set_upper_index")


def set_min_label(self, index):
    print("set_min_label")


def set_max_label(self, index):
    print("set_max_label")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = QDialog()
    layout = QVBoxLayout()
    label = QLabel("Hello World", parent=dialog)
    slider = QRangeSlider(dialog)

    # slider.lowerPositionChanged.connect(set_min_label)
    # slider.lowerValueChanged.connect(set_lower_index)
    # slider.upperPositionChanged.connect(set_max_label)
    # slider.upperValueChanged.connect(set_upper_index)

    layout.addWidget(label)
    layout.addWidget(slider)
    dialog.setLayout(layout)

    dialog.show()
    sys.exit(app.exec_())
