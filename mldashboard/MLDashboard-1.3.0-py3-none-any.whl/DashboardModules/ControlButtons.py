from MLDashboard.DashboardModules.Module import Module
from MLDashboard.MLCommunicationBackend import Message, MessageMode
import matplotlib.pyplot as pyplot
from matplotlib.widgets import Button
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition
import warnings
import copy
from typing import List


warnings.filterwarnings(action='ignore',
                        message=('This figure includes Axes that are not compatible with tight_layout, '
                                 'so results might be incorrect.')) #stops buttons from being broken

def createButtonWithingAxes(ax, x, y, width, height, text):
    button_ax = pyplot.axes([0, 0, 1, 1])
    ip = InsetPosition(ax, [x, y, width, height])
    button_ax.set_axes_locator(ip)
    return Button(button_ax, text)

class ControlButtons(Module):
    def __init__(self, ax, config):
        """Contains buttons to stop training and save model"""
        super().__init__(ax, config, "Control Buttons", noticks=True)
        self.stopbutton = createButtonWithingAxes(self.ax, 0.2, 0.2, 0.2, 0.1, "Stop Training")
        self.savebutton = createButtonWithingAxes(self.ax, 0.5, 0.2, 0.2, 0.1, "Save Model")
        self.stopbutton.on_clicked(self.stopFunc)
        self.savebutton.on_clicked(self.saveFunc)

        self.internalreturnlist: List[Message] = []

    def update(self, data: Message):
        out = copy.deepcopy(self.internalreturnlist)
        self.internalreturnlist = []
        return out

    def stopFunc(self, event):
        if event == event:
            pass
        self.internalreturnlist.append(Message(MessageMode.Command, {'command': 'stop'}))

    def saveFunc(self, event):
        if event == event:
            pass
        self.internalreturnlist.append(Message(MessageMode.Command, {'command': 'save'}))