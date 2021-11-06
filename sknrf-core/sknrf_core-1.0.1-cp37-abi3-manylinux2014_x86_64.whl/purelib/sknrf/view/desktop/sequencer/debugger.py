import sys
import time
if "bdb" in sys.modules.keys():
    PyDebug = object
    debugger_enable = False
else:
    from bdb import Bdb as PyDebug
    debugger_enable = True

from sknrf.model.runtime import RuntimeThread


class DebuggerThread(RuntimeThread, PyDebug):

    def __init__(self, *args, **kwargs):
        RuntimeThread.__init__(self)
        PyDebug.__init__(self, *args, **kwargs)
        self.enable = 0
        self.quitting = False
        self.user_response = False

    def run(self, *args, **kwargs):
        self.enable = debugger_enable
        if self.enable:
            self.user_response = self.set_continue
            self.runcall(self._func, *args, **kwargs)
        else:
            self._func(*args, **kwargs)

    def do_clear(self, arg):
        pass

    def user_call(self, frame, args):
        pass
        # name = frame.f_code.co_name or "<unknown>"
        # print("call", name, args)
        # self.set_continue()  # continue

    def user_line(self, frame):
        if self.enable:  # Set Trace to Start Debugger
            self.enable = False
            self.set_trace()  # start tracing
            self.set_continue()
        else:  # Stop or Break
            # arrived at breakpoint
            # name = frame.f_code.co_name or "<unknown>"
            # filename = self.canonic(frame.f_code.co_filename)
            # print("break at", filename, frame.f_lineno, "in", name)
            self.user_response = None
            if frame.f_code.co_name == self._func.__name__:
                self.stopped.emit(frame)
            else:
                self.finished.emit()
            while not self.user_response:
                time.sleep(0.1)
            if self.user_response == self.set_next:
                self.user_response(frame)
            else:
                self.user_response()

    def user_return(self, frame, value):
        pass
        # name = frame.f_code.co_name or "<unknown>"
        # print("return from", name, value)
        # print("continue...")
        # self.set_continue()  # continue

    def user_exception(self, frame, exception):
        pass
        # name = frame.f_code.co_name or "<unknown>"
        # print("exception in", name, exception)
        # print("continue...")
        # self.set_continue()  # continue

    def runcall(self, func, *args, **kwargs):
        super(DebuggerThread, self).runcall(func, *args, **kwargs)
        self.finished.emit()


