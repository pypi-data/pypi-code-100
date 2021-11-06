import time

from .exception import *

class sw:
    """Stopwatch thingy"""
    def __init__(self):
        self.st = 0
        self.et = 0
        
    def start(self):
        """Starts the stopwatch"""
        self.st = time.time()
        return 0
    
    def stop(self):
        """Stops the stopwatch and return the elapsed time in ms"""
        self.et = time.time()
        return round((self.et - self.st) * 1000)

stopwatch = sw()
del sw