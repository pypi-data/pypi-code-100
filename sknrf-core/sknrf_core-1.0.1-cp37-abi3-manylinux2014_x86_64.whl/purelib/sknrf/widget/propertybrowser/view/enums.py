from enum import Enum, Flag, auto, unique


from qtpropertybrowser import QtGroupPropertyManager
from qtpropertybrowser import QtIntPropertyManager, QtBoolPropertyManager
from qtpropertybrowser import QtDoublePropertyManager, QtComplexPropertyManager
from qtpropertybrowser import QtTFTensorPropertyManager
from qtpropertybrowser import QtStringPropertyManager, QtFilePropertyManager
from qtpropertybrowser import QtDatePropertyManager, QtTimePropertyManager, QtDateTimePropertyManager
from qtpropertybrowser import QtCharPropertyManager, QtKeySequencePropertyManager
from qtpropertybrowser import QtLocalePropertyManager
from qtpropertybrowser import QtPointPropertyManager, QtPointFPropertyManager
from qtpropertybrowser import QtSizePropertyManager, QtSizeFPropertyManager
from qtpropertybrowser import QtRectPropertyManager, QtRectFPropertyManager
from qtpropertybrowser import QtEnumPropertyManager, QtFlagPropertyManager
from qtpropertybrowser import QtSizePolicyPropertyManager
from qtpropertybrowser import QtFontPropertyManager, QtColorPropertyManager, QtCursorPropertyManager
from qtpropertybrowser import QtGroupEditorFactory
from qtpropertybrowser import QtIntEditFactory, QtSpinBoxFactory, QtSliderFactory, QtScrollBarFactory, QtCheckBoxFactory
from qtpropertybrowser import QtDoubleEditFactory, QtDoubleSpinBoxFactory, QtComplexEditFactory
from qtpropertybrowser import QtTFTensorEditFactory
from qtpropertybrowser import QtLineEditFactory, QtFileEditorFactory
from qtpropertybrowser import QtDateEditFactory, QtTimeEditFactory, QtDateTimeEditFactory
from qtpropertybrowser import QtKeySequenceEditorFactory, QtCharEditorFactory
from qtpropertybrowser import QtLocaleEditorFactory
from qtpropertybrowser import QtPointEditorFactory, QtPointFEditorFactory
from qtpropertybrowser import QtSizeEditorFactory, QtSizeFEditorFactory
from qtpropertybrowser import QtRectEditorFactory, QtRectFEditorFactory
from qtpropertybrowser import QtEnumEditorFactory, QtFlagEditorFactory
from qtpropertybrowser import QtSizePolicyEditorFactory
from qtpropertybrowser import QtFontEditorFactory, QtColorEditorFactory, QtCursorEditorFactory


@unique
class BrowserType(Enum):
    TREE = auto()
    BOX = auto()
    BUTTON = auto()


@unique
class DISPLAY(Flag):
    CHECK = auto()
    PUBLIC = auto()
    READ = auto()


@unique
class PropertyID(Enum):
    INT_SPIN = auto()
    INT_EDIT = auto()
    INT_SLIDER = auto()
    INT_SCROLL = auto()
    BOOL = auto()
    DOUBLE_SPIN = auto()
    DOUBLE_EDIT = auto()
    COMPLEX_EDIT = auto()
    TF_EDIT = auto()
    TF_FILE_EDIT = auto()
    STRING = auto()
    TB_FILE = auto()
    FILE = auto()
    DATE = auto()
    TIME = auto()
    DATETIME = auto()
    KEY_SEQUENCE = auto()
    CHAR = auto()
    LOCALE = auto()
    POINT = auto()
    POINTF = auto()
    SIZE = auto()
    SIZEF = auto()
    RECT = auto()
    RECTF = auto()
    ENUM = auto()
    FLAG = auto()
    SIZE_POLICY = auto()
    FONT = auto()
    COLOR = auto()
    CURSOR = auto()
    LIST = auto()
    TUPLE = auto()
    PY_OBJECT = auto()


id_manager_map = {
    PropertyID.INT_SPIN: QtIntPropertyManager,
    PropertyID.INT_EDIT: QtIntPropertyManager,
    PropertyID.INT_SLIDER: QtIntPropertyManager,
    PropertyID.INT_SCROLL: QtIntPropertyManager,
    PropertyID.BOOL: QtBoolPropertyManager,
    PropertyID.DOUBLE_SPIN: QtDoublePropertyManager,
    PropertyID.DOUBLE_EDIT: QtDoublePropertyManager,
    PropertyID.COMPLEX_EDIT: QtComplexPropertyManager,
    PropertyID.TF_EDIT: QtTFTensorPropertyManager,
    PropertyID.TF_FILE_EDIT: QtTFTensorPropertyManager,
    PropertyID.STRING: QtStringPropertyManager,
    PropertyID.TB_FILE: QtFilePropertyManager,
    PropertyID.FILE: QtFilePropertyManager,
    PropertyID.DATE: QtDatePropertyManager,
    PropertyID.TIME: QtTimePropertyManager,
    PropertyID.DATETIME: QtDateTimePropertyManager,
    PropertyID.KEY_SEQUENCE: QtKeySequencePropertyManager,
    PropertyID.CHAR: QtCharPropertyManager,
    PropertyID.LOCALE: QtLocalePropertyManager,
    PropertyID.POINT: QtPointPropertyManager,
    PropertyID.POINTF: QtPointFPropertyManager,
    PropertyID.SIZE: QtSizePropertyManager,
    PropertyID.SIZEF: QtSizeFPropertyManager,
    PropertyID.RECT: QtRectPropertyManager,
    PropertyID.RECTF: QtRectFPropertyManager,
    PropertyID.ENUM: QtEnumPropertyManager,
    PropertyID.FLAG: QtFlagPropertyManager,
    PropertyID.SIZE_POLICY: QtSizePolicyPropertyManager,
    PropertyID.FONT: QtFontPropertyManager,
    PropertyID.COLOR: QtColorPropertyManager,
    PropertyID.CURSOR: QtCursorPropertyManager,
    PropertyID.LIST: QtGroupPropertyManager,
    PropertyID.TUPLE: QtGroupPropertyManager,
    PropertyID.PY_OBJECT: QtGroupPropertyManager,
}

id_factory_map = {
    PropertyID.INT_SPIN: QtSpinBoxFactory,
    PropertyID.INT_EDIT: QtIntEditFactory,
    PropertyID.INT_SLIDER: QtSliderFactory,
    PropertyID.INT_SCROLL: QtScrollBarFactory,
    PropertyID.BOOL: QtCheckBoxFactory,
    PropertyID.DOUBLE_SPIN: QtDoubleSpinBoxFactory,
    PropertyID.DOUBLE_EDIT: QtDoubleEditFactory,
    PropertyID.COMPLEX_EDIT: QtComplexEditFactory,
    PropertyID.TF_EDIT: QtTFTensorEditFactory,
    PropertyID.TF_FILE_EDIT: QtTFTensorEditFactory,
    PropertyID.STRING: QtLineEditFactory,
    PropertyID.TB_FILE: QtFileEditorFactory,
    PropertyID.FILE: QtFileEditorFactory,
    PropertyID.DATE: QtDateEditFactory,
    PropertyID.TIME: QtTimeEditFactory,
    PropertyID.DATETIME: QtDateTimeEditFactory,
    PropertyID.KEY_SEQUENCE: QtKeySequenceEditorFactory,
    PropertyID.CHAR: QtCharEditorFactory,
    PropertyID.LOCALE: QtLocaleEditorFactory,
    PropertyID.POINT: QtPointEditorFactory,
    PropertyID.POINTF: QtPointFEditorFactory,
    PropertyID.SIZE: QtSizeEditorFactory,
    PropertyID.SIZEF: QtSizeFEditorFactory,
    PropertyID.RECT: QtRectEditorFactory,
    PropertyID.RECTF: QtRectFEditorFactory,
    PropertyID.ENUM: QtEnumEditorFactory,
    PropertyID.FLAG: QtFlagEditorFactory,
    PropertyID.SIZE_POLICY: QtSizePolicyEditorFactory,
    PropertyID.FONT: QtFontEditorFactory,
    PropertyID.COLOR: QtColorEditorFactory,
    PropertyID.CURSOR: QtCursorEditorFactory,
    PropertyID.LIST: QtGroupEditorFactory,
    PropertyID.TUPLE: QtGroupEditorFactory,
    PropertyID.PY_OBJECT: QtGroupEditorFactory,
}
