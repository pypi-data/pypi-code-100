from pynput import mouse, keyboard
import time, copy, threading, atexit, os
import logging, traitlets
from traitlets.config.configurable import Configurable
logging.basicConfig(level = logging.DEBUG, format = "%(message)s")
class Boundary:
    def __init__(self, x, y, w, h):
        self.anchor = (x, y)
        self.boundary = [ (x - w, y - h), (x + w, y + h) ]
    def help():
        logging.debug("Boundary(): __init__(self, x, y, w, h)\n")
class KeyException:
    def __init__(self, keylist = None, filename = None):
        try:
            if ((keylist != None) and (type(keylist) == list)):
                self.keylist = copy.deepcopy(keylist)
            elif (filename != None):
                if (os.path.isfile(filename)):
                    with open(filename, 'r') as FILE:
                        self.keylist = eval(FILE.read())
        except:
            logging.critical("KeyException could not be initialized.")
    def help():
        logging.debug("KeyException(): __init__(self, keylist = None, filename = None)\n")
class Limiter(Configurable):
    calibrate = False
    terminate = False
    monitor = False
    _monitor = traitlets.Bool()
    position = traitlets.Tuple()
    def help():
        logging.debug("Limiter():")
        logging.debug("\t__init__(self, boundary, keyexcept = None, chances = 0, penalty = None")
        logging.debug("\tmain(self)\n")
    def __init__(self, boundary, keyexcept = None, chances = 0, penalty = None, *args, **kwargs):
        super(Limiter, self).__init__(*args, **kwargs)
        self.keyexcept = None if keyexcept == None else copy.deepcopy(keyexcept)
        self.boundary = copy.deepcopy(boundary)
        self.chances, self.penalty = chances, penalty
    def __cur_pos(self):
        return mouse.Controller().position
    def __outta_range(self, x, y):
        bound = self.boundary.boundary
        return not ((bound[0][0] <= x <= bound[1][0]) and (bound[0][1] <= y <= bound[1][1]))
    def __on_press(self, key):
        if (key == keyboard.Key.f10):
            self.terminate = True
        elif (key == keyboard.Key.f9):
            self.monitor = not self.monitor
            self._monitor = self.monitor
            time.sleep(0.01)
        elif ((self.monitor) and (self.keyexcept != None) and (self.__key_exception(key))):
            logging.debug(f"Pressed: {self.__format_key(key)}.")
            self.__penalise()
    def __format_key(self, key):
        key = str(key)
        return (key[1:-1] if len(key) == 3 else key)
    def __key_exception(self, key):
        return not (self.__format_key(key) in self.keyexcept.keylist)
    def __penalise(self):
        if (self.penalty != None):
            if not (self.chances):
                exec(self.penalty)
                time.sleep(1)
        logging.debug(f"{self.chances} more chance(s) until penalty.")
        self.chances = (self.chances - (self.chances >= 1))
    def __pos_mouse(self):
        if (self.__outta_range(*(self.__cur_pos()))):
            mouse.Controller().position = copy.deepcopy(self.boundary.anchor)
            self.__penalise()
    def __monitor(self, timesleep = 0.05):
        while not self.terminate:
            if (self.monitor):
                if (self.__outta_range(*(self.__cur_pos()))):
                    self.calibrate = True
                    while (self.__outta_range(*(self.__cur_pos()))):
                        time.sleep(timesleep)
                    self.calibrate = False
            time.sleep(timesleep)
    def main(self):
        logging.debug("Monitor State: Paused.")
        m_listener = threading.Thread(target = self.__monitor)
        k_listener = keyboard.Listener(on_press = self.__on_press)
        m_listener.start()
        k_listener.start()
        atexit.register(m_listener.join)
        atexit.register(k_listener.stop)
        while not self.terminate:
            if (self.monitor):
                self.position = self.__cur_pos()
                #logging.debug(f"Pos: {self.__cur_pos()}")
                if (self.calibrate):
                    self.__pos_mouse()
            else:
                pass
                #logging.debug("Monitor Paused.")
            time.sleep(0.05)
        k_listener.stop()
        m_listener.join()
        logging.debug("Program State: Terminated.")
    @traitlets.observe('_monitor')
    def __show_update2(self, change):
        logging.debug(f"Monitor State: {'Running' if self.monitor else 'Paused' }.")
    @traitlets.observe('position')
    def __show_update(self, change):
        logging.debug(f"Current Position: {change['new']}.")