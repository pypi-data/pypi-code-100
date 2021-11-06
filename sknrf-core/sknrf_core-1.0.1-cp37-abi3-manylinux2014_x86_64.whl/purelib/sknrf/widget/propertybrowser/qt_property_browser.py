import sys
from enum import Enum, Flag, auto, unique

from PySide2.QtCore import Qt, QDate, QDateTime, QTime, QLocale, QPoint, QPointF, QSize, QSizeF, QRect, QRectF
from PySide2.QtGui import QCursor, QColor, QFont, QKeySequence
from PySide2.QtWidgets import QSizePolicy
from PySide2.QtWidgets import QApplication, QDialog, QLabel, QGridLayout, QScrollArea


@unique
class Color(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2


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


def set_value(property_, value):
    print("Set Value of: %s" % (property_.propertyManager(),))


if __name__ == "__main__":
    from view.enums import PropertyID, id_manager_map, id_factory_map
    from qtpropertybrowser import QtTreePropertyBrowser, QtGroupBoxPropertyBrowser, QtButtonPropertyBrowser
    from qtpropertybrowser import PkAvg, Scale, Format, Domain, BrowserCol

    app = QApplication(sys.argv)
    dialog = QDialog()
    layout = QGridLayout()
    group = [None]*2

    tree_scroll_area = QScrollArea()
    tree_browser = QtTreePropertyBrowser()
    # tree_browser.setAttributes([BrowserCol.MINIMUM, BrowserCol.MAXIMUM])
    tree_browser.setAttributes([BrowserCol.UNIT, BrowserCol.FORMAT, BrowserCol.CHECK])
    box_scroll_area = QScrollArea()
    box_browser = QtGroupBoxPropertyBrowser()
    # box_browser.setAttributes([BrowserCol.MINIMUM, BrowserCol.MAXIMUM])
    box_browser.setAttributes([BrowserCol.UNIT, BrowserCol.FORMAT, BrowserCol.CHECK])
    button_scroll_area = QScrollArea()
    button_browser = QtButtonPropertyBrowser()
    # button_browser.setAttributes([BrowserCol.MINIMUM, BrowserCol.MAXIMUM])
    button_browser.setAttributes([BrowserCol.UNIT, BrowserCol.FORMAT, BrowserCol.CHECK])

    manager_map = {}
    for k, v in id_manager_map.items():
        manager_map[k] = v()

    factory_map = {}
    for k, v in id_factory_map.items():
        factory_map[k] = v()

    factory_map[PropertyID.TF_EDIT].setSubFactory(factory_map[PropertyID.COMPLEX_EDIT])
    print(factory_map[PropertyID.COMPLEX_EDIT])
    print(factory_map[PropertyID.TF_EDIT].subFactory())

    for count in range(len(group)):
        # group
        group[count] = manager_map[PropertyID.PY_OBJECT].addProperty("group_%d" % (count + 1,))
        tree_browser.setFactoryForManager(manager_map[PropertyID.PY_OBJECT], factory_map[PropertyID.PY_OBJECT])
        box_browser.setFactoryForManager(manager_map[PropertyID.PY_OBJECT], factory_map[PropertyID.PY_OBJECT])
        button_browser.setFactoryForManager(manager_map[PropertyID.PY_OBJECT], factory_map[PropertyID.PY_OBJECT])

        # int_spin_rw
        manager_map[PropertyID.INT_SPIN].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.INT_SPIN].addProperty("int_spinbox_rw_%d" % (count + 1,))
        property_.propertyManager().setReadOnly(property_, False)
        property_.propertyManager().setUnit(property_, "V")
        property_.propertyManager().setMinimum(property_, 0)
        property_.propertyManager().setMaximum(property_, 2)
        property_.propertyManager().setValue(property_, 3)
        tree_browser.setFactoryForManager(manager_map[PropertyID.INT_SPIN], factory_map[PropertyID.INT_SPIN])
        box_browser.setFactoryForManager(manager_map[PropertyID.INT_SPIN], factory_map[PropertyID.INT_SPIN])
        button_browser.setFactoryForManager(manager_map[PropertyID.INT_SPIN], factory_map[PropertyID.INT_SPIN])
        group[count].addSubProperty(property_)

        # int_edit_r
        manager_map[PropertyID.INT_EDIT].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.INT_EDIT].addProperty("int_edit_r_%d" % (count + 1,))
        property_.propertyManager().setReadOnly(property_, True)
        property_.propertyManager().setUnit(property_, "V")
        property_.propertyManager().setMinimum(property_, 0)
        property_.propertyManager().setMaximum(property_, 2)
        property_.propertyManager().setValue(property_, 3)
        tree_browser.setFactoryForManager(manager_map[PropertyID.INT_EDIT], factory_map[PropertyID.INT_EDIT])
        box_browser.setFactoryForManager(manager_map[PropertyID.INT_EDIT], factory_map[PropertyID.INT_EDIT])
        button_browser.setFactoryForManager(manager_map[PropertyID.INT_EDIT], factory_map[PropertyID.INT_EDIT])
        group[count].addSubProperty(property_)

        # int_edit_rw
        manager_map[PropertyID.INT_EDIT].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.INT_EDIT].addProperty("int_edit_rw_%d" % (count + 1,))
        property_.propertyManager().setReadOnly(property_, False)
        property_.propertyManager().setUnit(property_, "V")
        property_.propertyManager().setMinimum(property_, 0)
        property_.propertyManager().setMaximum(property_, 2)
        property_.propertyManager().setValue(property_, 3)
        tree_browser.setFactoryForManager(manager_map[PropertyID.INT_EDIT], factory_map[PropertyID.INT_EDIT])
        box_browser.setFactoryForManager(manager_map[PropertyID.INT_EDIT], factory_map[PropertyID.INT_EDIT])
        button_browser.setFactoryForManager(manager_map[PropertyID.INT_EDIT], factory_map[PropertyID.INT_EDIT])
        group[count].addSubProperty(property_)

        # int_slider_rw
        manager_map[PropertyID.INT_SLIDER].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.INT_SLIDER].addProperty("int_slider_rw_%d" % (count + 1,))
        property_.propertyManager().setReadOnly(property_, False)
        property_.propertyManager().setUnit(property_, "V")
        property_.propertyManager().setMinimum(property_, 0)
        property_.propertyManager().setMaximum(property_, 2)
        property_.propertyManager().setValue(property_, 3)
        tree_browser.setFactoryForManager(manager_map[PropertyID.INT_SLIDER], factory_map[PropertyID.INT_SLIDER])
        box_browser.setFactoryForManager(manager_map[PropertyID.INT_SLIDER], factory_map[PropertyID.INT_SLIDER])
        button_browser.setFactoryForManager(manager_map[PropertyID.INT_SLIDER], factory_map[PropertyID.INT_SLIDER])
        group[count].addSubProperty(property_)

        # int_scroll_rw
        manager_map[PropertyID.INT_SCROLL].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.INT_SCROLL].addProperty("int_scroll_rw_%d" % (count + 1,))
        property_.propertyManager().setReadOnly(property_, False)
        property_.propertyManager().setUnit(property_, "V")
        property_.propertyManager().setMinimum(property_, 0)
        property_.propertyManager().setMaximum(property_, 2)
        property_.propertyManager().setValue(property_, 3)
        tree_browser.setFactoryForManager(manager_map[PropertyID.INT_SCROLL], factory_map[PropertyID.INT_SCROLL])
        box_browser.setFactoryForManager(manager_map[PropertyID.INT_SCROLL], factory_map[PropertyID.INT_SCROLL])
        button_browser.setFactoryForManager(manager_map[PropertyID.INT_SCROLL], factory_map[PropertyID.INT_SCROLL])
        group[count].addSubProperty(property_)

        # bool
        manager_map[PropertyID.BOOL].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.BOOL].addProperty("bool_%d" % (count + 1,))
        property_.propertyManager().setValue(property_, False)
        tree_browser.setFactoryForManager(manager_map[PropertyID.BOOL], factory_map[PropertyID.BOOL])
        box_browser.setFactoryForManager(manager_map[PropertyID.BOOL], factory_map[PropertyID.BOOL])
        button_browser.setFactoryForManager(manager_map[PropertyID.BOOL], factory_map[PropertyID.BOOL])
        group[count].addSubProperty(property_)

        # double_spin_rw
        manager_map[PropertyID.DOUBLE_SPIN].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.DOUBLE_SPIN].addProperty("double_spin_rw_%d" % (count + 1,))
        property_.propertyManager().setReadOnly(property_, False)
        property_.propertyManager().setUnit(property_, "V")
        property_.propertyManager().setPrecision(property_, 2)
        property_.propertyManager().setMinimum(property_, 0)
        property_.propertyManager().setMaximum(property_, 2)
        property_.propertyManager().setValue(property_, 3.14)
        tree_browser.setFactoryForManager(manager_map[PropertyID.DOUBLE_SPIN], factory_map[PropertyID.DOUBLE_SPIN])
        box_browser.setFactoryForManager(manager_map[PropertyID.DOUBLE_SPIN], factory_map[PropertyID.DOUBLE_SPIN])
        button_browser.setFactoryForManager(manager_map[PropertyID.DOUBLE_SPIN], factory_map[PropertyID.DOUBLE_SPIN])
        group[count].addSubProperty(property_)

        # double_edit_r
        manager_map[PropertyID.DOUBLE_EDIT].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.DOUBLE_EDIT].addProperty("double_edit_r_%d" % (count + 1,))
        property_.propertyManager().setReadOnly(property_, True)
        property_.propertyManager().setScale(property_, Scale.K)
        property_.propertyManager().setUnit(property_, "V")
        property_.propertyManager().setPrecision(property_, 2)
        property_.propertyManager().setMinimum(property_, 0)
        property_.propertyManager().setMaximum(property_, 2)
        property_.propertyManager().setValue(property_, 3.14)
        tree_browser.setFactoryForManager(manager_map[PropertyID.DOUBLE_EDIT], factory_map[PropertyID.DOUBLE_EDIT])
        box_browser.setFactoryForManager(manager_map[PropertyID.DOUBLE_EDIT], factory_map[PropertyID.DOUBLE_EDIT])
        button_browser.setFactoryForManager(manager_map[PropertyID.DOUBLE_EDIT], factory_map[PropertyID.DOUBLE_EDIT])
        group[count].addSubProperty(property_)

        # double_edit_rw
        manager_map[PropertyID.DOUBLE_EDIT].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.DOUBLE_EDIT].addProperty("double_edit_rw_%d" % (count + 1,))
        property_.propertyManager().setReadOnly(property_, False)
        property_.propertyManager().setUnit(property_, "V")
        property_.propertyManager().setPrecision(property_, 2)
        property_.propertyManager().setMinimum(property_, 0)
        property_.propertyManager().setMaximum(property_, 2)
        property_.propertyManager().setValue(property_, 3.14)
        tree_browser.setFactoryForManager(manager_map[PropertyID.DOUBLE_EDIT], factory_map[PropertyID.DOUBLE_EDIT])
        box_browser.setFactoryForManager(manager_map[PropertyID.DOUBLE_EDIT], factory_map[PropertyID.DOUBLE_EDIT])
        button_browser.setFactoryForManager(manager_map[PropertyID.DOUBLE_EDIT], factory_map[PropertyID.DOUBLE_EDIT])
        group[count].addSubProperty(property_)

        # complex_edit_r
        manager_map[PropertyID.COMPLEX_EDIT].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.COMPLEX_EDIT].addProperty("complex_edit_r_%d" % (count + 1,))
        property_.propertyManager().setReadOnly(property_, True)
        property_.propertyManager().setUnit(property_, "V")
        property_.propertyManager().setPrecision(property_, 2)
        property_.propertyManager().setMinimum(property_, 0)
        property_.propertyManager().setMaximum(property_, 2)
        property_.propertyManager().setValue(property_, 2 + 2j)
        tree_browser.setFactoryForManager(manager_map[PropertyID.COMPLEX_EDIT], factory_map[PropertyID.COMPLEX_EDIT])
        box_browser.setFactoryForManager(manager_map[PropertyID.COMPLEX_EDIT], factory_map[PropertyID.COMPLEX_EDIT])
        button_browser.setFactoryForManager(manager_map[PropertyID.COMPLEX_EDIT], factory_map[PropertyID.COMPLEX_EDIT])
        group[count].addSubProperty(property_)

        # complex_edit_rw
        manager_map[PropertyID.COMPLEX_EDIT].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.COMPLEX_EDIT].addProperty("complex_edit_rw_%d" % (count + 1,))
        property_.propertyManager().setReadOnly(property_, False)
        property_.propertyManager().setScale(property_, Scale.K)
        property_.propertyManager().setUnit(property_, "rW")
        property_.propertyManager().setPrecision(property_, 2)
        property_.propertyManager().setMinimum(property_, 0)
        property_.propertyManager().setMaximum(property_, 2)
        property_.propertyManager().setValue(property_, 2 + 2j)
        tree_browser.setFactoryForManager(manager_map[PropertyID.COMPLEX_EDIT], factory_map[PropertyID.COMPLEX_EDIT])
        box_browser.setFactoryForManager(manager_map[PropertyID.COMPLEX_EDIT], factory_map[PropertyID.COMPLEX_EDIT])
        button_browser.setFactoryForManager(manager_map[PropertyID.COMPLEX_EDIT], factory_map[PropertyID.COMPLEX_EDIT])
        group[count].addSubProperty(property_)

        # tf_tensor_r
        manager_map[PropertyID.TF_EDIT].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.TF_EDIT].addProperty("tf_tensor_r_%d" % (count + 1,))
        property_.propertyManager().setReadOnly(property_, True)
        property_.propertyManager().setUnit(property_, "V")
        property_.propertyManager().setPrecision(property_, 2)
        property_.propertyManager().setMinimum(property_, [0, 0])
        property_.propertyManager().setMaximum(property_, [2, 2])
        property_.propertyManager().setValue(property_, [2 + 2j, 2 + 2j])
        tree_browser.setFactoryForManager(manager_map[PropertyID.TF_EDIT], factory_map[PropertyID.TF_EDIT])
        box_browser.setFactoryForManager(manager_map[PropertyID.TF_EDIT], factory_map[PropertyID.TF_EDIT])
        button_browser.setFactoryForManager(manager_map[PropertyID.TF_EDIT], factory_map[PropertyID.TF_EDIT])
        tree_browser.setFactoryForManager(manager_map[PropertyID.TF_EDIT].subComplexPropertyManager(),
                                          factory_map[PropertyID.COMPLEX_EDIT])
        box_browser.setFactoryForManager(manager_map[PropertyID.TF_EDIT].subComplexPropertyManager(),
                                         factory_map[PropertyID.COMPLEX_EDIT])
        button_browser.setFactoryForManager(manager_map[PropertyID.TF_EDIT].subComplexPropertyManager(),
                                            factory_map[PropertyID.COMPLEX_EDIT])
        group[count].addSubProperty(property_)

        # tf_tensor_rw
        manager_map[PropertyID.TF_EDIT].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.TF_EDIT].addProperty("tf_tensor_rw_%d" % (count + 1,))
        property_.propertyManager().setSize(property_, 5)
        property_.propertyManager().setReadOnly(property_, False)
        property_.propertyManager().setScale(property_, Scale.m)
        property_.propertyManager().setUnit(property_, "V")
        property_.propertyManager().setFormat(property_, Format.LIN_DEG)
        property_.propertyManager().setPrecision(property_, 2)
        property_.propertyManager().setMinimum(property_, [0, 0, 0, 0, 0])
        property_.propertyManager().setMaximum(property_, [2, 2, 2, 2, 2])
        property_.propertyManager().setValue(property_, [2 + 2j, 2 + 2j, 2 + 2j, 2 + 2j, 2 + 2j])
        tree_browser.setFactoryForManager(manager_map[PropertyID.TF_EDIT], factory_map[PropertyID.TF_EDIT])
        box_browser.setFactoryForManager(manager_map[PropertyID.TF_EDIT], factory_map[PropertyID.TF_EDIT])
        button_browser.setFactoryForManager(manager_map[PropertyID.TF_EDIT], factory_map[PropertyID.TF_EDIT])
        tree_browser.setFactoryForManager(manager_map[PropertyID.TF_EDIT].subComplexPropertyManager(),
                                          factory_map[PropertyID.COMPLEX_EDIT])
        box_browser.setFactoryForManager(manager_map[PropertyID.TF_EDIT].subComplexPropertyManager(),
                                         factory_map[PropertyID.COMPLEX_EDIT])
        button_browser.setFactoryForManager(manager_map[PropertyID.TF_EDIT].subComplexPropertyManager(),
                                            factory_map[PropertyID.COMPLEX_EDIT])
        group[count].addSubProperty(property_)

        # str
        manager_map[PropertyID.STRING].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.STRING].addProperty("str_%d" % (count + 1,))
        property_.propertyManager().setValue(property_, "Hello World")
        tree_browser.setFactoryForManager(manager_map[PropertyID.STRING], factory_map[PropertyID.STRING])
        box_browser.setFactoryForManager(manager_map[PropertyID.STRING], factory_map[PropertyID.STRING])
        button_browser.setFactoryForManager(manager_map[PropertyID.STRING], factory_map[PropertyID.STRING])
        group[count].addSubProperty(property_)

        # file
        value = open("./file.txt", mode='w')
        value.close()
        manager_map[PropertyID.FILE].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.FILE].addProperty("file_%d" % (count + 1,))
        property_.propertyManager().setReadOnly(property_, False)
        property_.setEnabled(True)
        property_.propertyManager().setValue(property_, value.name)
        tree_browser.setFactoryForManager(manager_map[PropertyID.FILE], factory_map[PropertyID.FILE])
        box_browser.setFactoryForManager(manager_map[PropertyID.FILE], factory_map[PropertyID.FILE])
        button_browser.setFactoryForManager(manager_map[PropertyID.FILE], factory_map[PropertyID.FILE])
        group[count].addSubProperty(property_)

        # date
        manager_map[PropertyID.DATE].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.DATE].addProperty("date_%d" % (count + 1,))
        property_.propertyManager().setValue(property_, QDate.currentDate())
        tree_browser.setFactoryForManager(manager_map[PropertyID.DATE], factory_map[PropertyID.DATE])
        box_browser.setFactoryForManager(manager_map[PropertyID.DATE], factory_map[PropertyID.DATE])
        button_browser.setFactoryForManager(manager_map[PropertyID.DATE], factory_map[PropertyID.DATE])
        group[count].addSubProperty(property_)

        # time
        manager_map[PropertyID.TIME].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.TIME].addProperty("time_%d" % (count + 1,))
        property_.propertyManager().setValue(property_, QTime.currentTime())
        tree_browser.setFactoryForManager(manager_map[PropertyID.TIME], factory_map[PropertyID.TIME])
        box_browser.setFactoryForManager(manager_map[PropertyID.TIME], factory_map[PropertyID.TIME])
        button_browser.setFactoryForManager(manager_map[PropertyID.TIME], factory_map[PropertyID.TIME])
        group[count].addSubProperty(property_)

        # datetime
        manager_map[PropertyID.DATETIME].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.DATETIME].addProperty("datetime_%d" % (count + 1,))
        property_.propertyManager().setValue(property_, QDateTime.currentDateTime())
        tree_browser.setFactoryForManager(manager_map[PropertyID.DATETIME], factory_map[PropertyID.DATETIME])
        box_browser.setFactoryForManager(manager_map[PropertyID.DATETIME], factory_map[PropertyID.DATETIME])
        button_browser.setFactoryForManager(manager_map[PropertyID.DATETIME], factory_map[PropertyID.DATETIME])
        group[count].addSubProperty(property_)

        # key sequence
        value = QKeySequence(Qt.CTRL + Qt.Key_P)
        manager_map[PropertyID.KEY_SEQUENCE].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.KEY_SEQUENCE].addProperty("key sequence_%d" % (count + 1,))
        property_.propertyManager().setValue(property_, value)
        tree_browser.setFactoryForManager(manager_map[PropertyID.KEY_SEQUENCE], factory_map[PropertyID.KEY_SEQUENCE])
        box_browser.setFactoryForManager(manager_map[PropertyID.KEY_SEQUENCE], factory_map[PropertyID.KEY_SEQUENCE])
        button_browser.setFactoryForManager(manager_map[PropertyID.KEY_SEQUENCE], factory_map[PropertyID.KEY_SEQUENCE])
        group[count].addSubProperty(property_)

        # char
        value = 'a'
        manager_map[PropertyID.CHAR].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.CHAR].addProperty("char_%d" % (count + 1,))
        property_.propertyManager().setValue(property_, value)
        tree_browser.setFactoryForManager(manager_map[PropertyID.CHAR], factory_map[PropertyID.CHAR])
        box_browser.setFactoryForManager(manager_map[PropertyID.CHAR], factory_map[PropertyID.CHAR])
        button_browser.setFactoryForManager(manager_map[PropertyID.CHAR], factory_map[PropertyID.CHAR])
        group[count].addSubProperty(property_)

        # locale
        manager_map[PropertyID.LOCALE].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.LOCALE].addProperty("locale_%d" % (count + 1,))
        property_.propertyManager().setValue(property_, QLocale(QLocale.English, QLocale.Canada))
        tree_browser.setFactoryForManager(manager_map[PropertyID.LOCALE], factory_map[PropertyID.LOCALE])
        box_browser.setFactoryForManager(manager_map[PropertyID.LOCALE], factory_map[PropertyID.LOCALE])
        button_browser.setFactoryForManager(manager_map[PropertyID.LOCALE], factory_map[PropertyID.LOCALE])
        box_browser.setFactoryForManager(manager_map[PropertyID.LOCALE].subEnumPropertyManager(),
                                         factory_map[PropertyID.ENUM])
        button_browser.setFactoryForManager(manager_map[PropertyID.LOCALE].subEnumPropertyManager(),
                                            factory_map[PropertyID.ENUM])
        tree_browser.setFactoryForManager(manager_map[PropertyID.LOCALE].subEnumPropertyManager(),
                                          factory_map[PropertyID.ENUM])
        box_browser.setFactoryForManager(manager_map[PropertyID.LOCALE].subEnumPropertyManager(),
                                         factory_map[PropertyID.ENUM])
        button_browser.setFactoryForManager(manager_map[PropertyID.LOCALE].subEnumPropertyManager(),
                                            factory_map[PropertyID.ENUM])
        group[count].addSubProperty(property_)

        # point
        manager_map[PropertyID.POINT].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.POINT].addProperty("point_%d" % (count + 1,))
        property_.propertyManager().setValue(property_, QPoint(1, 3))
        tree_browser.setFactoryForManager(manager_map[PropertyID.POINT], factory_map[PropertyID.POINT])
        box_browser.setFactoryForManager(manager_map[PropertyID.POINT], factory_map[PropertyID.POINT])
        button_browser.setFactoryForManager(manager_map[PropertyID.POINT], factory_map[PropertyID.POINT])
        tree_browser.setFactoryForManager(manager_map[PropertyID.POINT].subIntPropertyManager(),
                                          factory_map[PropertyID.INT_EDIT])
        box_browser.setFactoryForManager(manager_map[PropertyID.POINT].subIntPropertyManager(),
                                         factory_map[PropertyID.INT_EDIT])
        button_browser.setFactoryForManager(manager_map[PropertyID.POINT].subIntPropertyManager(),
                                            factory_map[PropertyID.INT_EDIT])
        group[count].addSubProperty(property_)

        # pointf
        manager_map[PropertyID.POINTF].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.POINTF].addProperty("pointf_%d" % (count + 1,))
        property_.propertyManager().setValue(property_, QPointF(1.23, 3.21))
        tree_browser.setFactoryForManager(manager_map[PropertyID.POINTF], factory_map[PropertyID.POINTF])
        box_browser.setFactoryForManager(manager_map[PropertyID.POINTF], factory_map[PropertyID.POINTF])
        button_browser.setFactoryForManager(manager_map[PropertyID.POINTF], factory_map[PropertyID.POINTF])
        tree_browser.setFactoryForManager(manager_map[PropertyID.POINTF].subDoublePropertyManager(),
                                          factory_map[PropertyID.DOUBLE_EDIT])
        box_browser.setFactoryForManager(manager_map[PropertyID.POINTF].subDoublePropertyManager(),
                                         factory_map[PropertyID.DOUBLE_EDIT])
        button_browser.setFactoryForManager(manager_map[PropertyID.POINTF].subDoublePropertyManager(),
                                            factory_map[PropertyID.DOUBLE_EDIT])
        group[count].addSubProperty(property_)

        # size_r
        manager_map[PropertyID.SIZE].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.SIZE].addProperty("size_r_%d" % (count + 1,))
        property_.propertyManager().setReadOnly(property_, True)
        property_.propertyManager().setMinimum(property_, QSize(0, 0))
        property_.propertyManager().setMaximum(property_, QSize(2, 2))
        property_.propertyManager().setValue(property_, QSize(-1, 3))
        tree_browser.setFactoryForManager(manager_map[PropertyID.SIZE], factory_map[PropertyID.SIZE])
        box_browser.setFactoryForManager(manager_map[PropertyID.SIZE], factory_map[PropertyID.SIZE])
        button_browser.setFactoryForManager(manager_map[PropertyID.SIZE], factory_map[PropertyID.SIZE])
        tree_browser.setFactoryForManager(manager_map[PropertyID.SIZE].subIntPropertyManager(),
                                          factory_map[PropertyID.INT_EDIT])
        box_browser.setFactoryForManager(manager_map[PropertyID.SIZE].subIntPropertyManager(),
                                         factory_map[PropertyID.INT_EDIT])
        button_browser.setFactoryForManager(manager_map[PropertyID.SIZE].subIntPropertyManager(),
                                            factory_map[PropertyID.INT_EDIT])
        group[count].addSubProperty(property_)

        # size_rw
        manager_map[PropertyID.SIZE].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.SIZE].addProperty("size_rw_%d" % (count + 1,))
        property_.propertyManager().setReadOnly(property_, False)
        property_.propertyManager().setMinimum(property_, QSize(0, 0))
        property_.propertyManager().setMaximum(property_, QSize(255, 255))
        property_.propertyManager().setValue(property_, QSize(-1, 3))
        tree_browser.setFactoryForManager(manager_map[PropertyID.SIZE], factory_map[PropertyID.SIZE])
        box_browser.setFactoryForManager(manager_map[PropertyID.SIZE], factory_map[PropertyID.SIZE])
        button_browser.setFactoryForManager(manager_map[PropertyID.SIZE], factory_map[PropertyID.SIZE])
        tree_browser.setFactoryForManager(manager_map[PropertyID.SIZE].subIntPropertyManager(),
                                          factory_map[PropertyID.INT_EDIT])
        box_browser.setFactoryForManager(manager_map[PropertyID.SIZE].subIntPropertyManager(),
                                         factory_map[PropertyID.INT_EDIT])
        button_browser.setFactoryForManager(manager_map[PropertyID.SIZE].subIntPropertyManager(),
                                            factory_map[PropertyID.INT_EDIT])
        group[count].addSubProperty(property_)

        # sizef_r
        manager_map[PropertyID.SIZEF].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.SIZEF].addProperty("sizef_r_%d" % (count + 1,))
        property_.propertyManager().setReadOnly(property_, True)
        property_.propertyManager().setMinimum(property_, QSize(0, 0))
        property_.propertyManager().setMaximum(property_, QSize(2, 2))
        property_.propertyManager().setValue(property_, QSizeF(-1.23, 3.21))
        tree_browser.setFactoryForManager(manager_map[PropertyID.SIZEF], factory_map[PropertyID.SIZEF])
        box_browser.setFactoryForManager(manager_map[PropertyID.SIZEF], factory_map[PropertyID.SIZEF])
        button_browser.setFactoryForManager(manager_map[PropertyID.SIZEF], factory_map[PropertyID.SIZEF])
        tree_browser.setFactoryForManager(manager_map[PropertyID.SIZEF].subDoublePropertyManager(),
                                          factory_map[PropertyID.DOUBLE_EDIT])
        box_browser.setFactoryForManager(manager_map[PropertyID.SIZEF].subDoublePropertyManager(),
                                         factory_map[PropertyID.DOUBLE_EDIT])
        button_browser.setFactoryForManager(manager_map[PropertyID.SIZEF].subDoublePropertyManager(),
                                            factory_map[PropertyID.DOUBLE_EDIT])
        group[count].addSubProperty(property_)

        # sizef_rw
        manager_map[PropertyID.SIZEF].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.SIZEF].addProperty("sizef_rw_%d" % (count + 1,))
        property_.propertyManager().setReadOnly(property_, False)
        property_.propertyManager().setMinimum(property_, QSize(0, 0))
        property_.propertyManager().setMaximum(property_, QSize(2, 2))
        property_.propertyManager().setValue(property_, QSizeF(-1.23, 3.21))
        tree_browser.setFactoryForManager(manager_map[PropertyID.SIZEF], factory_map[PropertyID.SIZEF])
        box_browser.setFactoryForManager(manager_map[PropertyID.SIZEF], factory_map[PropertyID.SIZEF])
        button_browser.setFactoryForManager(manager_map[PropertyID.SIZEF], factory_map[PropertyID.SIZEF])
        tree_browser.setFactoryForManager(manager_map[PropertyID.SIZEF].subDoublePropertyManager(),
                                          factory_map[PropertyID.DOUBLE_EDIT])
        box_browser.setFactoryForManager(manager_map[PropertyID.SIZEF].subDoublePropertyManager(),
                                         factory_map[PropertyID.DOUBLE_EDIT])
        button_browser.setFactoryForManager(manager_map[PropertyID.SIZEF].subDoublePropertyManager(),
                                            factory_map[PropertyID.DOUBLE_EDIT])
        group[count].addSubProperty(property_)

        # rect
        manager_map[PropertyID.RECT].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.RECT].addProperty("rect_%d" % (count + 1,))
        property_.propertyManager().setValue(property_, QRect(0, 1, 2, 3))
        tree_browser.setFactoryForManager(manager_map[PropertyID.RECT], factory_map[PropertyID.RECT])
        box_browser.setFactoryForManager(manager_map[PropertyID.RECT], factory_map[PropertyID.RECT])
        button_browser.setFactoryForManager(manager_map[PropertyID.RECT], factory_map[PropertyID.RECT])
        tree_browser.setFactoryForManager(manager_map[PropertyID.RECT].subIntPropertyManager(),
                                          factory_map[PropertyID.INT_EDIT])
        box_browser.setFactoryForManager(manager_map[PropertyID.RECT].subIntPropertyManager(),
                                         factory_map[PropertyID.INT_EDIT])
        button_browser.setFactoryForManager(manager_map[PropertyID.RECT].subIntPropertyManager(),
                                            factory_map[PropertyID.INT_EDIT])
        group[count].addSubProperty(property_)

        # rectf
        manager_map[PropertyID.RECTF].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.RECTF].addProperty("rectf_%d" % (count + 1,))
        property_.propertyManager().setValue(property_, QRectF(0.12, 1.23, 2.34, 3.45))
        tree_browser.setFactoryForManager(manager_map[PropertyID.RECTF], factory_map[PropertyID.RECTF])
        box_browser.setFactoryForManager(manager_map[PropertyID.RECTF], factory_map[PropertyID.RECTF])
        button_browser.setFactoryForManager(manager_map[PropertyID.RECTF], factory_map[PropertyID.RECTF])
        tree_browser.setFactoryForManager(manager_map[PropertyID.RECTF].subDoublePropertyManager(),
                                          factory_map[PropertyID.DOUBLE_EDIT])
        box_browser.setFactoryForManager(manager_map[PropertyID.RECTF].subDoublePropertyManager(),
                                         factory_map[PropertyID.DOUBLE_EDIT])
        button_browser.setFactoryForManager(manager_map[PropertyID.RECTF].subDoublePropertyManager(),
                                            factory_map[PropertyID.DOUBLE_EDIT])
        group[count].addSubProperty(property_)

        # enum
        value = Color.RED
        manager_map[PropertyID.ENUM].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.ENUM].addProperty("enum_%d" % (count + 1,))
        items = sorted(value.__class__.__members__.items(), key=lambda t: t[1].value)
        names = [k for k, v in items]
        manager_map[PropertyID.ENUM].setEnumNames(property_, names)
        try:
            manager_map[PropertyID.ENUM].setValue(property_, value.value)
        except AttributeError:
            manager_map[PropertyID.ENUM].setValue(property_, value)
        tree_browser.setFactoryForManager(manager_map[PropertyID.ENUM], factory_map[PropertyID.ENUM])
        box_browser.setFactoryForManager(manager_map[PropertyID.ENUM], factory_map[PropertyID.ENUM])
        button_browser.setFactoryForManager(manager_map[PropertyID.ENUM], factory_map[PropertyID.ENUM])
        group[count].addSubProperty(property_)

        # flags
        value = ColorCombiner.PURPLE
        manager_map[PropertyID.FLAG].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.FLAG].addProperty("flag_%d" % (count + 1,))
        items = value.__class__.__members__.items()
        names = [k for ind, (k, v) in enumerate(items) if (v.value & (v.value - 1)) == 0 and v.value != 0]
        manager_map[PropertyID.FLAG].setFlagNames(property_, names)
        try:
            manager_map[PropertyID.FLAG].setValue(property_, value.value)
        except AttributeError:
            manager_map[PropertyID.FLAG].setValue(property_, value)
        tree_browser.setFactoryForManager(manager_map[PropertyID.FLAG], factory_map[PropertyID.FLAG])
        box_browser.setFactoryForManager(manager_map[PropertyID.FLAG], factory_map[PropertyID.FLAG])
        button_browser.setFactoryForManager(manager_map[PropertyID.FLAG], factory_map[PropertyID.FLAG])
        tree_browser.setFactoryForManager(manager_map[PropertyID.FLAG].subBoolPropertyManager(),
                                          factory_map[PropertyID.BOOL])
        box_browser.setFactoryForManager(manager_map[PropertyID.FLAG].subBoolPropertyManager(),
                                         factory_map[PropertyID.BOOL])
        button_browser.setFactoryForManager(manager_map[PropertyID.FLAG].subBoolPropertyManager(),
                                            factory_map[PropertyID.BOOL])
        group[count].addSubProperty(property_)

        # size_policy
        manager_map[PropertyID.SIZE_POLICY].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.SIZE_POLICY].addProperty("size_policy_%d" % (count + 1,))
        property_.propertyManager().setValue(property_, QSizePolicy())
        tree_browser.setFactoryForManager(manager_map[PropertyID.SIZE_POLICY], factory_map[PropertyID.SIZE_POLICY])
        box_browser.setFactoryForManager(manager_map[PropertyID.SIZE_POLICY], factory_map[PropertyID.SIZE_POLICY])
        button_browser.setFactoryForManager(manager_map[PropertyID.SIZE_POLICY], factory_map[PropertyID.SIZE_POLICY])
        tree_browser.setFactoryForManager(manager_map[PropertyID.SIZE_POLICY].subEnumPropertyManager(),
                                          factory_map[PropertyID.ENUM])
        tree_browser.setFactoryForManager(manager_map[PropertyID.SIZE_POLICY].subIntPropertyManager(),
                                          factory_map[PropertyID.INT_EDIT])
        box_browser.setFactoryForManager(manager_map[PropertyID.SIZE_POLICY].subEnumPropertyManager(),
                                         factory_map[PropertyID.ENUM])
        box_browser.setFactoryForManager(manager_map[PropertyID.SIZE_POLICY].subIntPropertyManager(),
                                         factory_map[PropertyID.INT_EDIT])
        button_browser.setFactoryForManager(manager_map[PropertyID.SIZE_POLICY].subEnumPropertyManager(),
                                            factory_map[PropertyID.ENUM])
        button_browser.setFactoryForManager(manager_map[PropertyID.SIZE_POLICY].subIntPropertyManager(),
                                            factory_map[PropertyID.INT_EDIT])
        group[count].addSubProperty(property_)

        # font
        manager_map[PropertyID.FONT].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.FONT].addProperty("font_%d" % (count + 1,))
        property_.propertyManager().setValue(property_, QFont())
        tree_browser.setFactoryForManager(manager_map[PropertyID.FONT], factory_map[PropertyID.FONT])
        box_browser.setFactoryForManager(manager_map[PropertyID.FONT], factory_map[PropertyID.FONT])
        button_browser.setFactoryForManager(manager_map[PropertyID.FONT], factory_map[PropertyID.FONT])
        group[count].addSubProperty(property_)

        # color
        manager_map[PropertyID.COLOR].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.COLOR].addProperty("color_%d" % (count + 1,))
        property_.propertyManager().setValue(property_, QColor())
        tree_browser.setFactoryForManager(manager_map[PropertyID.COLOR], factory_map[PropertyID.COLOR])
        box_browser.setFactoryForManager(manager_map[PropertyID.COLOR], factory_map[PropertyID.COLOR])
        button_browser.setFactoryForManager(manager_map[PropertyID.COLOR], factory_map[PropertyID.COLOR])
        group[count].addSubProperty(property_)

        # cursor
        manager_map[PropertyID.CURSOR].valueChanged.connect(set_value)
        property_ = manager_map[PropertyID.CURSOR].addProperty("cursor_%d" % (count + 1,))
        property_.propertyManager().setValue(property_, QCursor())
        tree_browser.setFactoryForManager(manager_map[PropertyID.CURSOR], factory_map[PropertyID.CURSOR])
        box_browser.setFactoryForManager(manager_map[PropertyID.CURSOR], factory_map[PropertyID.CURSOR])
        button_browser.setFactoryForManager(manager_map[PropertyID.CURSOR], factory_map[PropertyID.CURSOR])
        group[count].addSubProperty(property_)

        browser_item = tree_browser.addProperty(group[count])
        tree_browser.setExpanded(browser_item, True)
        browser_item = box_browser.addProperty(group[count])
        browser_item = button_browser.addProperty(group[count])
        button_browser.setExpanded(browser_item, True)

    tree_browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    tree_scroll_area.setWidgetResizable(True)
    tree_scroll_area.setWidget(tree_browser)
    layout.addWidget(QLabel("Tree Browser", parent=dialog), 0, 0)
    layout.addWidget(tree_scroll_area, 1, 0)

    tree_scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    box_scroll_area.setWidgetResizable(True)
    box_scroll_area.setWidget(box_browser)
    layout.addWidget(QLabel("Box Browser", parent=dialog), 0, 1)
    layout.addWidget(box_scroll_area, 1, 1)

    button_scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    button_scroll_area.setWidgetResizable(True)
    button_scroll_area.setWidget(button_browser)
    layout.addWidget(QLabel("Button Browser", parent=dialog), 0, 2)
    layout.addWidget(button_scroll_area, 1, 2)

    dialog.setLayout(layout)
    dialog.showMaximized()
    sys.exit(app.exec_())
