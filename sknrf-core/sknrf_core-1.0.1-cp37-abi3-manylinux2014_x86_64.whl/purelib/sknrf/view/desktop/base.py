import logging
import os
import sys
import traceback

from PySide2 import QtCore, QtGui
from PySide2.QtCore import QObject, QThread
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import QApplication, QFrame, QStyleOption, QStyle, QMessageBox

from sknrf.settings import Settings
from sknrf.model.base import AbstractModel, model_logger
from sknrf.view.desktop.runtime.QBusyFrame import Ui_busyFrame
__author__ = 'dtbespal'


class BusyFrame(QFrame, Ui_busyFrame):
    def __init__(self, parent, quit_signal, message=""):
        super(BusyFrame, self).__init__(parent)
        self.setupUi(self)
        quit_signal.connect(self.deleteLater)
        self.set_message(message)

    def __enter__(self):
        self.setGeometry(self.parent().contentsRect())
        self.busyIndicator.startAnimation()
        self.raise_()
        self.show()
        QApplication.processEvents()
        return self

    def __exit__(self, type, value, traceback):
        pass

    def set_message(self, message):
        self.label.setText(message)

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.init(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)
        super().paintEvent(event)


class QtHandlerObject(QObject):
    """A Qt Object that relays events to the Qt backend.

        See Also
        ----------
        sknrf.QtHandler
    """
    new_record = QtCore.Signal(object)

    def __init__(self):
        super(QtHandlerObject, self).__init__()


class QtHandler(logging.Handler):
    """A Python Logging Handler that transmits events to the Qt backend.

        Python logging events are broadcast to the Qt backend by emitting a QtCore.Signal. The QtHandler is
        automatically initialized when sknrf Core is launched.

        See Also
        ----------
        sknrf.QtHandlerObject
    """

    def __init__(self):
        logging.Handler.__init__(self)
        self.q_object = QtHandlerObject()

    def emit(self, record):
        """Emits a QtCore.Signal that must be handled by a slot in the Qt backend.
        """
        self.q_object.new_record.emit(record)


def desktop_logger(logger):
    log_level = logging.DEBUG if Settings().debug else logging.INFO

    model_logger(logger)
    if len(logger.handlers) == 2:
        Settings()._qt_logging_handler = QtHandler()
        qt_handler =  Settings()._qt_logging_handler
        qt_handler.setLevel(log_level)
        logger.addHandler(Settings()._qt_logging_handler)
    return logger


def unhandled_exception(exc_type, exc_value, exc_traceback):
    """ Catches all unhandled exceptions.

        Unhandled exceptions are summarized inside a message box and the logger before exiting the application with
        status=1

        Notes
        -----
        If debug mode is enabled, the application will continue to run, but may perform unexpected behaviour.

    """
    if QtGui.qApp:
        if issubclass(exc_type, KeyboardInterrupt):
            QtGui.qApp.quit()
            return
        logger = logging.getLogger(__name__)
        model_logger(logger)
        logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

        filename, line, dummy, dummy = traceback.extract_tb(exc_traceback).pop()
        filename = os.path.basename(filename)
        error = "%s: %s" % (exc_type.__name__, exc_value)

        ret = QMessageBox.critical(None, "Error",
                                         "<html>A critical error has occured.<br/> "
                                         + "<b>%s</b><br/><br/>" % error
                                         + "It occurred at <b>line %d</b> of file <b>%s</b>.<br/>" % (line, filename)
                                         + "</html>",
                                   QMessageBox.Ignore | QMessageBox.Close, QMessageBox.Close)
        if ret == QMessageBox.Close:
            QtGui.qApp.quit()
    else:
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger = logging.getLogger(__name__)
        model_logger(logger)
        logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))



def cleanup(form):
    for datagroup in AbstractModel.datagroup_model().values():
        datagroup.close()
