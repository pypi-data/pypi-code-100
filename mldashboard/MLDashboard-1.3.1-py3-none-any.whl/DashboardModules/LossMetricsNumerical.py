from MLDashboard.DashboardModules.Module import Module
from MLDashboard.MLCommunicationBackend import Message, MessageMode
import warnings

class LossMetricsNumerical(Module):
    """Shows loss, accuracy, and other metrics by listing stats. Also shows evaluation stats at end."""
    def __init__(self, ax, config):
        super().__init__(ax, config, "Loss Metrics Info", noticks=True)
        self.ax.axis([0, 10, 0, 10])
        self.epochtext = self.ax.text(1, 9, "Epoch: ")
        self.losstext = self.ax.text(1, 8, "Loss: ")
        self.othertext = []

        self.pos = 0


    def update(self, data: Message):
        if data.mode == MessageMode.Epoch_End:
            self.epochtext.set_text("Epoch: " + str(round(data.body["epoch"] + 1, 3)))
            self.losstext.set_text("Loss: " + str(round(data.body["loss"], 3)))

            self.pos = 7
            for i, key in enumerate(sorted(data.body.keys())):
                if key not in ['loss', 'epoch']:
                    if i >= len(self.othertext):
                        self.othertext.append(self.ax.text(1, self.pos, "No key: "))
                    self.othertext[i].set_text(key[0].upper() + key[1:] + ": " + str(round(data.body[key], 3)))
                    self.pos -= 1

                if self.pos <= 0:
                    warnings.warn("Too many keys in loss metrics info.")
                    break

        elif data.mode == MessageMode.Test_End:
            self.epochtext.set_text("Training stats:")
            self.pos -= 1
            self.ax.text(1, self.pos, "Testing stats:")
            self.pos -= 1
            self.ax.text(1, self.pos, "Loss: " + str(round(data.body["loss"], 3)))
            self.pos -= 1
            for key in sorted(data.body.keys()):
                if key != "loss":
                    self.ax.text(1, self.pos, key[0].upper() + key[1:] + ": " + str(round(data.body[key], 3)))
                    self.pos -= 1