from MLDashboard.MLCommunicationBackend import Message
from typing import List
import warnings

class Module:
    def __init__(self, ax, config: dict, title: str, noticks=False, reqkeys: List[str] = None):
        """
        Creates a module in a axes

        :param ax: matplotlib axes
        :param config: module specific config
        :param title: Placed above plot
        :param noticks: Should plot have tick marks
        :param reqkeys: List of required keys in config
        """
        self.ax = ax
        self.config = config
        self.ax.set_title(title)

        if noticks:
            self.ax.tick_params(axis='both', which='both', bottom=False, top=False,
                                labelbottom=False, right=False, left=False, labelleft=False)

        if reqkeys is not None:
            for key in reqkeys:
                if key not in config:
                    raise Exception("Config for module: " + str(title) + " missing key: " + str(key))

    def initialRequests(self):
        pass

    def update(self, data: Message):
        if self == self:
            pass
        warnings.warn("Update method should have been overriden, but it was not.")
        warnings.warn("Update method called with: " + str(data))