import sys
from PySide2 import QtCore
from PySide2.QtCore import QThread

from sknrf.settings import Settings
from sknrf.enums.runtime import RuntimeState
from sknrf.model.base import AbstractModel
from sknrf.utilities.numeric import Info


class RuntimeThread(QThread):

    error = QtCore.Signal(object, object, object)
    started_ = QtCore.Signal(object)

    def __init__(self):
        super(RuntimeThread, self).__init__()
        self._args = []
        self._model = None
        self._view = None

    def connect_signals(self, model, view):
        view.stimulus_ports = model.ports
        view.ss_stimulus_ports = model.ss_ports
        model.moveToThread(self)

        model.init_request.connect(view.initialize)
        model.update_request.connect(view.update)
        model.close_request.connect(view.close)
        view.resume_request.connect(self.resume)

        model.finished.connect(self.quit)
        model.finished.connect(model.deleteLater)
        self.finished.connect(self.deleteLater)
        self.error.connect(self.unhandled_exception)

        self._model = model
        self._view = view

    def disconnect_signals(self, model, view):
        view.resume_request.disconnect()

        self.finished.disconnect()

        model.runInThread(self.thread())
        self._model = None
        self._view = None

    def start(self):
        super(RuntimeThread, self).start()
        self.started_.emit(self._args)

    def set_args(self, *args):
        self._args = args

    def resume(self):
        self.quit()

    def deleteLater(self, *args, **kwargs):
        self.disconnect_signals(self._model, self._view)
        super().deleteLater()

    def unhandled_exception(self, *exc_info):
        sys.excepthook(*exc_info)


class RuntimeModel(AbstractModel):

    init_request = QtCore.Signal(object)
    update_request = QtCore.Signal(object, int)
    close_request = QtCore.Signal(object)
    finished = QtCore.Signal()
    error = QtCore.Signal(str)

    def __init__(self):
        super(RuntimeModel, self).__init__()
        self.background = False
        self.ports = [1, 2]
        self.ss_ports = [1, 2]
        self.save_data = True

    def __getstate__(self, state={}):
        state = super(RuntimeModel, self).__getstate__(state=state)
        # ### Manually save selected object PROPERTIES here ###
        state["background"] = self.background
        state["port_indices"] = self.ports
        state["sp_port_indices"] = self.ss_ports
        state["save_data"] = self.save_data
        return state

    def __setstate__(self, state):
        super(RuntimeModel, self).__setstate__(state)
        # ### Manually load saved object ATTRIBUTES and PROPERTIES here ###
        self.background = state["background"]
        self.ports = state["port_indices"]
        self.ss_ports = state["sp_port_indices"]
        self.save_data = state["save_data"]

    def __info__(self):
        """ Initializes the display information of a device and stores information in self.info.
        """
        super(RuntimeModel, self).__info__()
        # ### Manually generate info of ATTRIBUTES and PROPERTIES here ###
        self.info["init_request"] = Info("init_request", read=False, write=False, check=False)
        self.info["update_request"] = Info("update_request", read=False, write=False, check=False)
        self.info["close_request"] = Info("close_request", read=False, write=False, check=False)
        self.info["finished"] = Info("finished", read=False, write=False, check=False)

        self.info["background"] = Info("background", read=False, write=False, check=False)
        self.info["stimulus_ports"] = Info("stimulus_ports", read=False, write=False, check=False)
        self.info["ss_stimulus_ports"] = Info("ss_stimulus_ports", read=False, write=False, check=False)
        self.info["save_data"] = Info("save_data", read=False, write=False, check=False)

    def measure(self):
        self.runInThread(self.thread())
        self.start()
        try:
            for i in range(100):
                self.check_state()
                self.thread().msleep(1000) # Do Work
                self.update(i, Ellipsis)
        except InterruptedError:
            pass
        finally:
            self.stop()

    def check_state(self):
        while Settings().runtime_state == RuntimeState.PAUSED:
            self.thread().msleep(100)
            if Settings().runtime_state == RuntimeState.STOPPED:
                raise InterruptedError
        if Settings().runtime_state == RuntimeState.STOPPED:
            raise InterruptedError

    def start(self):
        if self.background == False:
            self.init_request.emit(self)
            self.thread().exec_()
        else:
            Settings().runtime_state = RuntimeState.RUN

    def stop(self):
        if self.background == False:
            Settings().runtime_state = RuntimeState.STOPPED
            self.close_request.emit(self)
            self.moveToThread(self.thread().thread())
            self.finished.emit()

    def update(self, batch_index=-1):
        if self.background == False:
            self.update_request.emit(self, batch_index)
            self.thread().exec_()

    def moveToThread(self, thread):
        """
        Changes the thread affinity (lifetime) for self and its children.

        When thread is deleted, self is deleted. Marshals an interface pointer from one thread to another thread in
        the same process.
        """
        try:
            self.error.disconnect()
            self.init_request.disconnect()
            self.update_request.disconnect()
            self.close_request.disconnect()
        except RuntimeError:
            pass
        super(RuntimeModel, self).moveToThread(thread)
        AbstractModel.device_model().moveToThread(thread)

    def runInThread(self, thread):
        """
        Changes the thread that is run for self and its children.

        When a method of self is executed, this thread becomes active(blocking). Each method should call self.exec_()
        when it is finished so that the thread can return to its event loop. Unmarshals a buffer containing an interface
        pointer and releases the stream when an interface pointer has been marshaled from another thread to the calling
        thread.
        """
        super(RuntimeModel, self).runInThread(thread)
        AbstractModel.device_model().runInThread(thread)
