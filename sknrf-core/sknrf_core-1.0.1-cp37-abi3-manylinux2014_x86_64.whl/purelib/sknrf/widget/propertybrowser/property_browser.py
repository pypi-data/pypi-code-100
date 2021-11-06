import sys
import os
from enum import Enum, IntEnum, IntFlag, Flag, auto, unique

import numpy as np
import torch as th
import tables as tb
from PySide2.QtCore import Qt, QLocale, QPoint, QPointF, QSize, QSizeF, QRect, QRectF
from PySide2.QtGui import QCursor, QColor, QFont, QKeySequence
from PySide2.QtWidgets import QLabel
from PySide2.QtWidgets import QGridLayout, QSizePolicy
from PySide2.QtWidgets import QApplication, QDialog

from sknrf.settings import Settings
from sknrf.model.sequencer.sweep.real import LinearSweep
from sknrf.widget.propertybrowser.view.enums import DISPLAY, BrowserType
from sknrf.utilities.numeric import Info
from qtpropertybrowser import PkAvg, Scale, Format, Domain, BrowserCol
from sknrf.widget.propertybrowser.view.base import PropertyScrollArea

@unique
class Color(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2

@unique
class ShapeEdges(IntEnum):
    CIRCLE = 0
    TRIANGLE = 3
    RECTANGLE = 4


@unique
class ColorCombiner(Flag):
    BLACK = 0
    RED = auto()
    YELLOW = auto()
    BLUE = auto()
    GREEN = YELLOW | BLUE
    ORANGE = RED | YELLOW
    PURPLE = RED | BLUE
    WHITE = RED | YELLOW | BLUE

@unique
class Direction(IntFlag):
    NORTH = 0x01
    SOUTH = 0x02
    EAST = 0x10
    WEST = 0x20


if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = {"bool": True,
             "flag": ColorCombiner.PURPLE,
             "int_flag": Direction.SOUTH | Direction.WEST,
             "enum": Color.RED,
             "int_enum": ShapeEdges.TRIANGLE,
             "int": 3,
             "float": 3.14,
             "complex": 3.14 - 1j * 4.13,
             "tf_tensor": 1.5*th.ones((Settings().t_points, Settings().f_points), dtype=th.complex128),
             "str": "Hello World",
             "tb file": tb.open_file(os.sep.join([Settings().data_root, "testdata", "dataset", "test.h5"]), "r"),
             "file": open(os.sep.join([Settings().data_root, "testdata", "dataset", "i_read.txt"]), "r"),
             "locale": QLocale(QLocale.English, QLocale.Canada),
             "point": QPoint(1, 3),
             "pointf": QPointF(1.23, 3.21),
             "size": QSize(1, 3),
             "sizef": QSizeF(1.23, 3.21),
             "rect": QRect(0, 1, 2, 3),
             "rectf": QRectF(0.12, 1.23, 2.34, 3.45),
             "cursor": QCursor(),
             "color": QColor(),
             "font": QFont(),
             "key_sequence": QKeySequence(Qt.CTRL + Qt.Key_P),
             "size_policy": QSizePolicy(),
             "list": [1, 2, 3],
             "tuple": ("One", 2, False),
             "dict": {"one": 1, "two": 2, "three": 3},
             "pyobject": LinearSweep()
             }

    info = {"tf_tensor": Info("tf_tensor", write=True, check=True, domain=Domain.TF)}

    dialog = QDialog()
    layout = QGridLayout()

    tree_scroll = PropertyScrollArea(parent=dialog, display=DISPLAY.READ, browser_type=BrowserType.TREE)
    tree_browser = tree_scroll.property_browser
    tree_browser.setAttributes([BrowserCol.PKAVG, BrowserCol.UNIT, BrowserCol.FORMAT, BrowserCol.CHECK])
    tree_browser.setAttributes([BrowserCol.MINIMUM, BrowserCol.MAXIMUM, BrowserCol.CHECK])
    tree_browser.set_model(model, info=info)
    layout.addWidget(QLabel("Tree Browser", parent=dialog), 0, 0)
    layout.addWidget(tree_scroll, 1, 0)

    box_scroll = PropertyScrollArea(parent=dialog, display=DISPLAY.READ, browser_type=BrowserType.BOX)
    box_browser = box_scroll.property_browser
    box_browser.setAttributes([BrowserCol.PKAVG, BrowserCol.UNIT, BrowserCol.FORMAT, BrowserCol.CHECK])
    box_browser.setAttributes([BrowserCol.MINIMUM, BrowserCol.MAXIMUM, BrowserCol.CHECK])
    box_browser.set_model(model, info=info)
    layout.addWidget(QLabel("Box Browser", parent=dialog), 0, 1)
    layout.addWidget(box_scroll, 1, 1)

    button_scroll = PropertyScrollArea(parent=dialog, display=DISPLAY.READ, browser_type=BrowserType.BUTTON)
    button_browser = button_scroll.property_browser
    button_browser.setAttributes([BrowserCol.PKAVG, BrowserCol.UNIT, BrowserCol.FORMAT, BrowserCol.CHECK])
    button_browser.setAttributes([BrowserCol.MINIMUM, BrowserCol.MAXIMUM, BrowserCol.CHECK])
    button_browser.set_model(model, info=info)
    layout.addWidget(QLabel("Button Browser", parent=dialog), 0, 2)
    layout.addWidget(button_scroll, 1, 2)

    tree_browser.update()
    box_browser.update()
    button_browser.update()

    dialog.setLayout(layout)
    dialog.showMaximized()
    sys.exit(app.exec_())
