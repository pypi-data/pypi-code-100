import logging
from warnings import warn

import numpy as np
import torch as th
import tables as tb
from PySide2.QtWidgets import QWidget, QScrollArea

from sknrf.device.signal import tf
from sknrf.widget.propertybrowser.view.enums import DISPLAY, PropertyID, BrowserType
from sknrf.widget.propertybrowser.view.enums import id_manager_map, id_factory_map
from sknrf.widget.propertybrowser.view.helper import type_id_map, domain_id_map, unsupported_types
from sknrf.widget.propertybrowser.view.helper import get_attr, get_attr_info, set_attr, model_generator
from qtpropertybrowser import QtTreePropertyBrowser, QtGroupBoxPropertyBrowser, QtButtonPropertyBrowser
from qtpropertybrowser import QtProperty, QtBrowserItem
from qtpropertybrowser import PkAvg, Scale, Format, Domain, BrowserCol
from sknrf.utilities.numeric import Info


__author__ = 'dtbespal'

logger = logging.getLogger(__name__)


def enum_mapping(enum):
    """Maps from 0-based enum indices to the actual enum values"""
    items = enum.__class__.__members__
    keys, values = list(items.keys()), list(items.values())
    map_ = dict(zip(range(len(values)), values))
    return keys, map_


def flag_mapping(flag):
    """Maps from 0-based flag indices to the actual flag values"""
    items = flag.__class__.__members__.items()
    items = {k: v for k, v in items if (v.value & (v.value - 1)) == 0 and v.value != 0}
    keys, values = list(items.keys()), list(items.values())
    map_ = {2**index: value for index, value in zip(range(len(values)), values)}
    return keys, map_


class PropertyBrowserMixIn(object):
    """Property Browser Widget for rendering/editing the public properties of an object.

    Keyword Args:
        parent (QWidget): Parent GUI container
        display (DISPLAY): display configuration

    .. raw:: html

       <table width="100%" style="text-align:center">
        <tr>
            <th width="14%" style="text-align:center">Data Type</th>
            <th width="14%" style="text-align:center">Property Manager (Renderer)</th>
            <th width="14%" style="text-align:center">Property Factory (Editor)</th>
        </tr>
        <tr>
            <th style="text-align:center">bool</th>
            <td><a href="http://docs.huihoo.com/qt/solutions/4/qtpropertybrowser/qtboolpropertymanager.html">QtBoolPropertyManager</a></td>
            <td><a href="http://docs.huihoo.com/qt/solutions/4/qtpropertybrowser/qtcheckboxfactory.html">QtCheckBoxFactory</a></td>
        </tr>
        <tr>
            <th style="text-align:center">int</th>
            <td><a href="http://docs.huihoo.com/qt/solutions/4/qtpropertybrowser/qtintpropertymanager.html">QtIntPropertyManager</a></td>
            <td><a href="http://docs.huihoo.com/qt/solutions/4/qtpropertybrowser/qtspinboxFactory.html">QtSpinBoxFactory</a></td>
        </tr>
        <tr>
            <th style="text-align:center">float</th>
            <td><a href="http://docs.huihoo.com/qt/solutions/4/qtpropertybrowser/qtdoublepropertymanager.html">QtDoublePropertyManager</a></td>
            <td><a href="http://docs.huihoo.com/qt/solutions/4/qtpropertybrowser/qtdoublespinboxfactory.html">QtDoubleSpinBoxFactory</a></td>
        </tr>
        <tr>
            <th style="text-align:center">complex</th>
            <td><a href="http://docs.huihoo.com/qt/solutions/4/qtpropertybrowser/qtcomplexpropertymanager.html">QtComplexPropertyManager</a></td>
            <td><a href="http://docs.huihoo.com/qt/solutions/4/qtpropertybrowser/qtcomplexeditfactory.html">QtComplexEditFactory</a></td>
        </tr>
        <tr>
            <th style="text-align:center">str</th>
            <td><a href="http://docs.huihoo.com/qt/solutions/4/qtpropertybrowser/qtstringpropertymanager.html">QtStringPropertyManager</a></td>
            <td><a href="http://docs.huihoo.com/qt/solutions/4/qtpropertybrowser/qtlineeditfactory.html">QtLineEditFactory</a></td>
        </tr>
        <tr>
            <th style="text-align:center">enum</th>
            <td><a href="http://docs.huihoo.com/qt/solutions/4/qtpropertybrowser/qtenumpropertymanager.html">QtEnumPropertyManager</a></td>
            <td><a href="http://docs.huihoo.com/qt/solutions/4/qtpropertybrowser/qtenumeditorfactory.html">QtEnumEditorFactory</a></td>
        </tr>
        <tr>
            <th style="text-align:center">flag</th>
            <td><a href="http://docs.huihoo.com/qt/solutions/4/qtpropertybrowser/qtflagpropertymanager.html">QtFlagPropertyManager</a></td>
            <td></td>
        </tr>
        <tr>
            <th style="text-align:center">file</th>
            <td><a href="http://docs.huihoo.com/qt/solutions/4/qtpropertybrowser/qtfilepathmanager.html">QtFilePathManager</a></td>
            <td><a href="http://docs.huihoo.com/qt/solutions/4/qtpropertybrowser/qtfileeditorfactory.html">QtFileEditorFactory</a></td>
        </tr>
        <tr>
            <th style="text-align:center">tb_file</th>
            <td><a href="http://docs.huihoo.com/qt/solutions/4/qtpropertybrowser/qtfilepathmanager.html">QtFilePathManager</a></td>
            <td><a href="http://docs.huihoo.com/qt/solutions/4/qtpropertybrowser/qtfileeditorfactory.html">QtFileEditorFactory</a></td>
        </tr>
        <tr>
            <th style="text-align:center">tb_array</th>
            <td><a href="http://docs.huihoo.com/qt/solutions/4/qtpropertybrowser/qtcomplexpropertymanager.html">QtComplexPropertyManager</a></td>
            <td><a href="http://docs.huihoo.com/qt/solutions/4/qtpropertybrowser/qtcomplexeditfactory.html">QtComplexEditFactory</a></td>
        </tr>
        <tr>
            <th style="text-align:center">array</th>
            <td><a href="http://docs.huihoo.com/qt/solutions/4/qtpropertybrowser/qtcomplexarraypropertymanager.html">QtComplexArrayPropertyManager</a></td>
            <td><a href="http://docs.huihoo.com/qt/solutions/4/qtpropertybrowser/qtarrayeditfactory.html">QtArrayEditFactory</a></td>
        </tr>
        <tr>
            <th style="text-align:center">nsignal</th>
            <td><a href="http://docs.huihoo.com/qt/solutions/4/qtpropertybrowser/qtcomplexarraypropertymanager.html">QtComplexArrayPropertyManager</a></td>
            <td><a href="http://docs.huihoo.com/qt/solutions/4/qtpropertybrowser/qtarrayeditfactory.html">QtArrayEditFactory</a></td>
        </tr>
        <tr>
            <th style="text-align:center">SignalArray</th>
            <td><a href="http://docs.huihoo.com/qt/solutions/4/qtpropertybrowser/qtcomplexarraypropertymanager.html">QtComplexArrayPropertyManager</a></td>
            <td><a href="http://docs.huihoo.com/qt/solutions/4/qtpropertybrowser/qtequationeditfactory.html">QtEquationEditFactory</a></td>
        </tr>
        <tr>
            <th style="text-align:center">group</th>
            <td><a href="http://docs.huihoo.com/qt/solutions/4/qtpropertybrowser/qtgrouppropertymanager.html">QtGroupPropertyManager</a></td>
            <td></td>
        </tr>
       </table>
    """

    def __init__(self, parent=None, display=DISPLAY.READ):
        self._slot_set_value = None
        self._slot_set_range = None
        self._slot_set_pk_avg = None
        self._slot_set_check = None
        self.__rendering = False
        self._display = display
        self._id_manager_map = {}
        self._id_factory_map = {}
        self._manager_id_map = {}
        self.property_values_map = {}
        self._model = None
        self.update_func = self.update
        self.update_kwargs = {}

    def connect_signals(self, slot_set_value=None, slot_set_range=None, slot_set_pk_avg=None, slot_set_check=None):
        self._slot_set_value = slot_set_value if slot_set_value else self.slot_set_value
        self._slot_set_range = slot_set_range if slot_set_range else self.slot_set_range
        self._slot_set_pk_avg = slot_set_pk_avg if slot_set_pk_avg else self.slot_set_pk_avg
        self._slot_set_check = slot_set_check if slot_set_check else self.slot_set_check
        for v in self._id_manager_map.values():
            if hasattr(v, "valueChanged"):
                v.valueChanged.connect(self._slot_set_value)
            if hasattr(v, "rangeChanged"):
                v.rangeChanged.connect(self._slot_set_range)
            if hasattr(v, "pkAvgChanged"):
                v.pkAvgChanged.connect(self._slot_set_pk_avg)
            if hasattr(v, "checkChanged"):
                v.checkChanged.connect(self._slot_set_check)

    def disconnect_signals(self):
        for v in self._id_manager_map.values():
            if hasattr(v, "valueChanged"):
                try:
                    v.valueChanged.disconnect()
                except RuntimeError:  # Multiple disconnects
                    pass
            if hasattr(v, "rangeChanged"):
                try:
                    v.rangeChanged.disconnect()
                except RuntimeError:  # Multiple disconnects
                    pass
            if hasattr(v, "pkAvgChanged"):
                try:
                    v.pkAvgChanged.disconnect()
                except RuntimeError:  # Multiple disconnects
                    pass
            if hasattr(v, "checkChanged"):
                try:
                    v.checkChanged.disconnect()
                except RuntimeError:  # Multiple disconnects
                    pass

    def setFactoryForManager(self, id_):
        manager = self._id_manager_map[id_]
        factory = self._id_factory_map[id_]
        super().setFactoryForManager(manager, factory)

        if id_ == PropertyID.FLAG:
            super().setFactoryForManager(manager.subBoolPropertyManager(),
                                         self._id_factory_map[PropertyID.BOOL])
        elif id_ == PropertyID.TF_EDIT:
            self._id_factory_map[PropertyID.TF_EDIT].setSubFactory(self._id_factory_map[PropertyID.COMPLEX_EDIT])
            super().setFactoryForManager(manager.subComplexPropertyManager(),
                                         self._id_factory_map[PropertyID.COMPLEX_EDIT])
        elif id_ == PropertyID.TF_FILE_EDIT:
            self._id_factory_map[PropertyID.TF_FILE_EDIT].setSubFactory(self._id_factory_map[PropertyID.COMPLEX_EDIT])
            super().setFactoryForManager(manager.subComplexPropertyManager(),
                                         self._id_factory_map[PropertyID.COMPLEX_EDIT])
        elif id_ == PropertyID.LOCALE:
            super().setFactoryForManager(manager.subEnumPropertyManager(),
                                         self._id_factory_map[PropertyID.ENUM])
        elif id_ == PropertyID.POINT:
            super().setFactoryForManager(manager.subIntPropertyManager(),
                                         self._id_factory_map[PropertyID.INT_SPIN])
        elif id_ == PropertyID.POINTF:
            super().setFactoryForManager(manager.subDoublePropertyManager(),
                                         self._id_factory_map[PropertyID.DOUBLE_SPIN])
        elif id_ == PropertyID.SIZE:
            super().setFactoryForManager(manager.subIntPropertyManager(),
                                         self._id_factory_map[PropertyID.INT_SPIN])
        elif id_ == PropertyID.SIZEF:
            super().setFactoryForManager(manager.subDoublePropertyManager(),
                                         self._id_factory_map[PropertyID.DOUBLE_SPIN])
        elif id_ == PropertyID.RECT:
            super().setFactoryForManager(manager.subIntPropertyManager(),
                                         self._id_factory_map[PropertyID.INT_SPIN])
        elif id_ == PropertyID.RECTF:
            super().setFactoryForManager(manager.subDoublePropertyManager(),
                                         self._id_factory_map[PropertyID.DOUBLE_SPIN])
        elif id_ == PropertyID.SIZE_POLICY:
            super().setFactoryForManager(manager.subIntPropertyManager(),
                                         self._id_factory_map[PropertyID.INT_SPIN])
            super().setFactoryForManager(manager.subEnumPropertyManager(),
                                         self._id_factory_map[PropertyID.ENUM])

    @property
    def display(self):
        return self._display

    @display.setter
    def display(self, display):
        self._display = DISPLAY(display)
        self.set_model(self._model)

    def model(self):
        return self._model

    def set_model(self, model, info=None, expanded=False):
        if model is not None:
            info = {} if info is None else info
            self.disconnect_signals()
            self.clear()
            self.property_values_map.clear()
            self._model = model
            property_ = self.add_property("model", model, info=info)
            property_.setPropertyName(model.__class__.__name__)
            item = self.addProperty(property_)
            if isinstance(item, QtBrowserItem):  # todo: figure out why item is sometimes a QtProperty object
                self.setExpanded(item, True)
                for child_item in item.children():
                    if isinstance(child_item, QtBrowserItem):
                        self.setExpanded(child_item, expanded)
            self.connect_signals()

    def clear(self):
        super().clear()
        for k, v in id_manager_map.items():
            self._id_manager_map[k].clear()

    def add_property(self, name, value, info=Info("untitled", write=True, check=True), parent=None):
        id_, property_, manager = None, None, None
        if isinstance(value, unsupported_types):
            return None
        for type_, id_ in type_id_map.items():
            if isinstance(value, type_):
                if isinstance(value, th.Tensor):
                    id_ = domain_id_map[info.domain]
                manager = self._id_manager_map[id_]
                while not isinstance(property_, QtProperty):
                    property_ = manager.addProperty(name)
                break
        if property_ is None:
            warn("Unsupported type: %s, found in %s.%s" % (type(value), type(parent), name))
            return None

        if id_ == PropertyID.BOOL:
            property_.setEnabled(info.write)
        elif id_ == PropertyID.FLAG:
            property_.setEnabled(info.write)
            keys, _ = flag_mapping(value)
            manager.setFlagNames(property_, keys)
        elif id_ == PropertyID.ENUM:
            property_.setEnabled(info.write)
            keys, _ = enum_mapping(value)
            manager.setEnumNames(property_, keys)
        elif id_ == PropertyID.INT_EDIT:
            property_.setEnabled(True)
            manager.setReadOnly(property_, not info.write)
            manager.setRange(property_, float(max(info.min, -2 ** 31)), float(min(info.max, 2 ** 31 - 1)))
            manager.setUnit(property_, info.unit)
        elif id_ == PropertyID.DOUBLE_EDIT:
            property_.setEnabled(True)
            manager.setReadOnly(property_, not info.write)
            manager.setAbsTol(property_, info.abs_tol)
            manager.setRelTol(property_, info.rel_tol)
            manager.setRange(property_, info.min, info.max)
            manager.setScale(property_, info.scale)
            manager.setUnit(property_, info.unit)
            manager.setFormat(property_, info.format)
            manager.setPrecision(property_, info.precision)
        elif id_ == PropertyID.COMPLEX_EDIT:
            manager.setReadOnly(property_, not info.write)
            manager.setAbsTol(property_, info.abs_tol)
            manager.setRelTol(property_, info.rel_tol)
            manager.setRange(property_, info.min, info.max)
            manager.setScale(property_, info.scale)
            manager.setUnit(property_, info.unit)
            manager.setPkAvg(property_, info.pk_avg)
            manager.setFormat(property_, info.format)
            manager.setPrecision(property_, info.precision)
        elif id_ == PropertyID.TF_EDIT:
            property_.setEnabled(True)
            size = int(np.prod(value.shape)/value.shape[-2])
            fill_ = np.ones((size,), dtype=np.float)
            manager.setReadOnly(property_, not info.write)
            manager.setSize(property_, value.shape[-1])
            manager.setScale(property_, info.scale)
            manager.setUnit(property_, info.unit)
            manager.setPkAvg(property_, info.pk_avg)
            manager.setFormat(property_, info.format)
            manager.setPrecision(property_, info.precision)
            manager.setAbsTol(property_, info.abs_tol*fill_)
            manager.setRelTol(property_, info.rel_tol*fill_)
            manager.setRange(property_, info.min*fill_, info.max*fill_)
        elif id_ == PropertyID.TF_FILE_EDIT:
            property_.setEnabled(True)
            size = int(np.prod(value._v_attrs.shape)/value._v_attrs.shape[-2])
            fill_ = np.ones((size,), dtype=np.float)
            manager.setReadOnly(property_, not info.write)
            manager.setSize(property_, value._v_attrs.shape[-1])
            manager.setScale(property_, info.scale)
            manager.setUnit(property_, info.unit)
            manager.setPkAvg(property_, info.pk_avg)
            manager.setFormat(property_, info.format)
            manager.setPrecision(property_, info.precision)
            manager.setAbsTol(property_, info.abs_tol*fill_)
            manager.setRelTol(property_, info.rel_tol*fill_)
            manager.setRange(property_, info.min*fill_, info.max*fill_)
        elif id_ == PropertyID.STRING:
            property_.setEnabled(True)
            manager.setReadOnly(property_, not info.write)
        elif id_ == PropertyID.LIST:
            for sub_index, sub_value in enumerate(value):
                if hasattr(sub_value, "shape") and len(sub_value.shape) == 0:
                    sub_value = sub_value.item()
                self.add_property("[%d]" % (sub_index,), sub_value, parent=property_)
        elif id_ == PropertyID.TUPLE:
            for sub_index, sub_value in enumerate(value):
                self.add_property("(%d)" % (sub_index,), sub_value, parent=property_)
        elif id_ == PropertyID.PY_OBJECT:
            if value is None:
                return None
            generator = model_generator(value, display=self._display)
            for sub_name in generator:
                sub_value = get_attr(value, sub_name)
                try:
                    sub_info = info[sub_name]
                except KeyError:
                    sub_info = Info("untitled", write=True, check=True)
                except TypeError:
                    sub_info = Info("untitled", write=True, check=True)
                self.add_property(sub_name, sub_value, info=sub_info, parent=property_)
        else:
            property_.setEnabled(info.write)
        self.set_value(property_, value)
        try:
            manager.setCheck(property_, info.check)
        except AttributeError:
            pass
        if parent:
            parent.addSubProperty(property_)
        return property_

    def value(self, property_):
        manager = property_.propertyManager()
        id_ = self._manager_id_map[manager]

        # Collections
        if id_ == PropertyID.LIST:
            return self.property_values_map[property_]
        if id_ == PropertyID.TUPLE:
            return self.property_values_map[property_]
        if id_ == PropertyID.PY_OBJECT:
            return self.property_values_map[property_]

        # Values
        value = manager.value(property_)
        if id_ == PropertyID.FLAG:
            _, map_ = flag_mapping(self.property_values_map[property_])
            index_flags, value_flags = value, 0
            for index, value in map_.items():
                if index & index_flags:
                    value_flags |= value.value
            value = self.property_values_map[property_].__class__(value_flags)
        elif id_ == PropertyID.ENUM:
            _, map_ = enum_mapping(self.property_values_map[property_])
            value = map_[value]
            value = self.property_values_map[property_].__class__(value)
        elif id_ == PropertyID.TF_EDIT:
            arr = value
            value = self.property_values_map[property_]
            tf.set_pk(value, arr) if manager.pkAvg(property_) is PkAvg.PK else tf.set_avg(value, arr)
        elif id_ == PropertyID.TF_FILE_EDIT:
            arr = value
            value = self.property_values_map[property_]
            tf.set_pk(value, arr) if manager.pkAvg(property_) is PkAvg.PK else tf.set_avg(value, arr)
        elif id_ == PropertyID.TB_FILE:
            value = tb.open_file(value)
            value.close()
        elif id_ == PropertyID.FILE:
            value = open(value)
            value.close()
        return value

    def set_value(self, property_, value):
        manager = property_.propertyManager()
        id_ = self._manager_id_map[manager]

        # Collections
        if id_ == PropertyID.LIST:
            self.property_values_map[property_] = value
            return
        elif id_ == PropertyID.TUPLE:
            self.property_values_map[property_] = value
            return
        elif id_ == PropertyID.PY_OBJECT:
            self.property_values_map[property_] = value
            return

        # Values
        if id_ == PropertyID.FLAG:
            self.property_values_map[property_] = value
            _, map_ = flag_mapping(value)
            index_flags, value_flags = 0, value
            for index, value in map_.items():
                if value & value_flags:
                    index_flags |= index
            value = index_flags
        elif id_ == PropertyID.ENUM:
            self.property_values_map[property_] = value
            _, map_ = enum_mapping(value)
            value = list(map_.values()).index(value)
        elif id_ == PropertyID.TF_EDIT:
            self.property_values_map[property_] = value
            value = th.as_tensor(value[...])
            arr = tf.pk(value) if manager.pkAvg(property_) is PkAvg.PK else tf.avg(value)
            value = arr.detach().flatten().numpy().astype(np.complex)
        elif id_ == PropertyID.TF_FILE_EDIT:
            self.property_values_map[property_] = value
            value = value[...]
            arr = tf.pk(value) if manager.pkAvg(property_) is PkAvg.PK else tf.avg(value)
            value = arr.detach().flatten().numpy().astype(np.complex)
        elif id_ == PropertyID.TB_FILE:
            value = value.filename
        elif id_ == PropertyID.FILE:
            value = value.name
        manager.setValue(property_, value)

    def slot_set_value(self, property_, value, model=None):

        def _sub_set_value(sub_property, sub_value,
                           count, m0, p0, prefix):
            for p1 in p0.subProperties():
                n1 = p1.propertyName()
                if sub_property is p1:
                    if n1.startswith("[") and n1.endswith("]") or n1.startswith("(") and n1.endswith(")"):
                        return int(n1[1:-1])
                    else:
                        set_attr(m0, n1, sub_value)
                        return -1
                if count < max_depth:
                    container_index = _sub_set_value(sub_property, sub_value,
                                                     count + 1, get_attr(m0, n1), p1, "%s.%s" % (prefix, n1))
                    if container_index > -1:
                        container = get_attr(m0, n1)
                        container[container_index] = sub_value
                        set_attr(m0, n1, container)
            return - 1

        if model is None:
            model = self._model
        value = self.value(property_)
        max_depth = 1
        _sub_set_value(property_, value,
                       0, model, self.properties()[0], "model")
        self.update_func(**self.update_kwargs)

    def slot_set_range(self, property_, min_, max_, model=None):

        def _sub_set_range(sub_property, _min_, _max_, count, m0, p0, prefix):
            for p1 in p0.subProperties():
                n1 = p1.propertyName()
                if sub_property is p1:
                    info = get_attr_info(m0, n1)
                    info.min = _min_
                    info.max = _max_
                    print("slot_set_range: %s.%s = %s-%s" % (prefix, n1, str(_min_), str(_max_)))
                    return
                if count < max_depth:
                    _sub_set_range(sub_property, _min_, _max_, count + 1, get_attr(m0, n1), p1, "%s.%s" % (prefix, n1))
        if model is None:
            model = self._model
        max_depth = 1
        _sub_set_range(property_, min_, max_, 0, model, self.properties()[0], "model")
        self.update_func(**self.update_kwargs)

    def slot_set_pk_avg(self, property_, pk_avg, model=None):

        def _sub_set_pk_avg(sub_property, pk_avg_, count, m0, p0, prefix):
            for p1 in p0.subProperties():
                n1 = p1.propertyName()
                if sub_property is p1:
                    info = get_attr_info(m0, n1)
                    info.pk_avg = pk_avg_
                    print("slot_set_pk_avg: %s.%s = %s" % (prefix, n1, str(pk_avg_)))
                    return
                if count < max_depth:
                    _sub_set_pk_avg(sub_property, pk_avg_, count + 1, get_attr(m0, n1), p1, "%s.%s" % (prefix, n1))
        if model is None:
            model = self._model
        max_depth = 1
        _sub_set_pk_avg(property_, pk_avg, 0, model, self.properties()[0], "model")
        self.update_func(**self.update_kwargs)

    def slot_set_check(self, property_, check, model=None):

        def _sub_set_check(sub_property, check_, count, m0, p0, prefix):
            for p1 in p0.subProperties():
                n1 = p1.propertyName()
                if sub_property is p1:
                    info = get_attr_info(m0, n1)
                    info.check = check_
                    print("slot_set_check: %s.%s = %s" % (prefix, n1, str(check_)))
                    return
                if count < max_depth:
                    _sub_set_check(sub_property, check_, count + 1, get_attr(m0, n1), p1, "%s.%s" % (prefix, n1))
        if model is None:
            model = self._model
        max_depth = 1
        _sub_set_check(property_, check, 0, model, self.properties()[0], "model")
        self.update_func(**self.update_kwargs)

    def render(self):
        name = ""
        try:
            if self.__rendering:
                raise UnboundLocalError
            self.__rendering = True
            for property_ in self.properties()[0].subProperties():
                name = property_.propertyName()
                value = get_attr(self._model, name)
                self.set_value(property_, value)
        except UnboundLocalError:
            logger.warning("Unbounded Table Numerical Value Detected in %s.%s" % (str(type(self._model)), name))
        finally:
            self.__rendering = False

    def set_update(self, func, **kwargs):
        self.update_func = func
        self.update_kwargs = kwargs


class TreePropertyBrowser(PropertyBrowserMixIn, QtTreePropertyBrowser):

    def __init__(self, parent=None, display=DISPLAY.READ):
        PropertyBrowserMixIn.__init__(self, parent=parent, display=display)
        QtTreePropertyBrowser.__init__(self, parent=parent)
        self.setRootIsDecorated(False)

        for k, v in id_manager_map.items():
            self._id_manager_map[k] = v(parent=self)
        self._manager_id_map = dict(zip(self._id_manager_map.values(), self._id_manager_map.keys()))
        for k, v in id_factory_map.items():
            self._id_factory_map[k] = v(parent=self) if v is not None else None
        for id_ in PropertyID:
            self.setFactoryForManager(id_)
        self.connect_signals()


class BoxPropertyBrowser(PropertyBrowserMixIn, QtGroupBoxPropertyBrowser):

    def __init__(self, parent=None, display=DISPLAY.READ):
        PropertyBrowserMixIn.__init__(self, parent=parent, display=display)
        QtGroupBoxPropertyBrowser.__init__(self, parent=parent)

        for k, v in id_manager_map.items():
            self._id_manager_map[k] = v(parent=self)
        self._manager_id_map = dict(zip(self._id_manager_map.values(), self._id_manager_map.keys()))
        for k, v in id_factory_map.items():
            self._id_factory_map[k] = v(parent=self) if v is not None else None
        for id_ in PropertyID:
            self.setFactoryForManager(id_)
        self.connect_signals()

    def setExpanded(self, browser_item, expanded):
        pass


class ButtonPropertyBrowser(PropertyBrowserMixIn, QtButtonPropertyBrowser):

    def __init__(self, parent=None, display=DISPLAY.READ):
        PropertyBrowserMixIn.__init__(self, parent=parent, display=display)
        QtButtonPropertyBrowser.__init__(self, parent=parent)

        for k, v in id_manager_map.items():
            self._id_manager_map[k] = v(parent=self)
        self._manager_id_map = dict(zip(self._id_manager_map.values(), self._id_manager_map.keys()))
        for k, v in id_factory_map.items():
            self._id_factory_map[k] = v(parent=self) if v is not None else None
        for id_ in PropertyID:
            self.setFactoryForManager(id_)
        self.connect_signals()


class PropertyScrollArea(QScrollArea):

    def __init__(self, parent=None, display=DISPLAY.READ, browser_type=BrowserType.TREE):
        super().__init__(parent=parent)
        if browser_type == BrowserType.TREE:
            self.property_browser = TreePropertyBrowser(parent=self, display=display)
            self.setWidgetResizable(True)
        if browser_type == BrowserType.BOX:
            self.property_browser = BoxPropertyBrowser(parent=self, display=display)
            self.setWidgetResizable(True)
        if browser_type == BrowserType.BUTTON:
            self.property_browser = ButtonPropertyBrowser(parent=self, display=display)
            self.setWidgetResizable(True)
        self.setWidget(self.property_browser)
