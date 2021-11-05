from MLDashboard.DashboardModules.Module import Module
from MLDashboard.MLCommunicationBackend import Message, MessageMode

class LossMetricsGraph(Module):
    """Graph showing current loss, accuracy, and other metrics."""
    def __init__(self, ax, config):
        super().__init__(ax, config, "Loss Metrics Graph")
        self.loss = []
        self.losscolor = ""
        self.metrics = {}
        self.metriccolors = {}

        self.ax.set_xlabel('Epoch')

    def update(self, data: Message):
        if data.mode == MessageMode.Epoch_End:
            self.loss.append(data.body['loss'])

            for key in data.body:
                if key not in ['loss', 'epoch']:
                    sublist = self.metrics.get(key, [])
                    sublist.append(data.body[key])
                    self.metrics[key] = sublist

            for key in self.metrics:
                if key not in self.metriccolors:
                    self.metriccolors[key] = self.ax.plot(range(1, len(self.metrics[key]) + 1),
                                                          self.metrics[key], label=key)[0].get_c()
                else:
                    self.ax.plot(range(len(self.metrics[key]) - 1, len(self.metrics[key]) + 1),
                                 self.metrics[key][-2:], color=self.metriccolors[key])

            if self.losscolor == "":
                self.losscolor = self.ax.plot(range(1, len(self.loss) +1), self.loss, label='loss')[0].get_c()
                self.ax.legend()
            else:
                self.ax.plot(range(len(self.loss) - 1, len(self.loss) + 1), self.loss[-2:], color=self.losscolor)

            ticks = list(range(0, len(self.loss), int((len(self.loss)-1)/10 + 1)))
            if len(ticks) == 1:
                ticks = [1]
            elif len(ticks) > 1 and ticks[1] == 1:
                for i in range(0, len(ticks)):
                    ticks[i] += 1
            else:
                ticks.append(ticks[-1] * 2 - ticks[-2])
            self.ax.set_xticks(ticks)
            self.ax.set_xlim(right=ticks[-1]+1)

