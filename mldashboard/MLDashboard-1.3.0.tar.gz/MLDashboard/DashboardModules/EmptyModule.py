from MLDashboard.DashboardModules.Module import Module
from MLDashboard.MLCommunicationBackend import Message

class EmptyModule(Module):
    def __init__(self, ax, config):
        """Module with no functionality, used to make a grid of modules"""
        super().__init__(ax, config, "", noticks=True)
        self.ax.axis([0, 10, 0, 10])
        self.ax.text(5, 5, "This Page Intentionally Left Blank", ha='center', va='center')

    def update(self, data: Message):
        pass
