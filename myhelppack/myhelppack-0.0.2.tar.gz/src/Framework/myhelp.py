from tkinter import *
from typing import Any

master = Tk()
class App(master):
    def __init__(self):
        super().__init__()
        size: Any | None = ...  

    def CreateFrame(self, size: Any | None = ...):
        # configure the root window
        self.title('My Awesome App')
        self.geometry(size)