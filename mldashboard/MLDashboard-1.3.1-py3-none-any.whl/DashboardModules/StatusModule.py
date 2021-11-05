from MLDashboard.DashboardModules.Module import Module
from MLDashboard.MLCommunicationBackend import Message, MessageMode
from matplotlib.patches import Rectangle

class StatusModule(Module):
    """Module that shows current dashboard status info. Useful for monitoring performance."""
    def __init__(self, ax, config):
        super().__init__(ax, config, "Dashboard Status", noticks=True)
        self.ax.axis([0, 10, 0, 10])
        self.modetext = self.ax.text(1, 9, "Current Mode: ")
        self.autorendertext = self.ax.text(1, 8, "Autorendering: ")
        self.timertext = self.ax.text(1, 7, "Timer: ")

        self.rects = [] #holds comparative speed rects after first update call
        self.borderrects = []

    def update(self, data: Message):
        if data.mode == MessageMode.CustomData:
            self.modetext.set_text("Current Mode: " + str(data.body["currentmode"]))

            if data.body["currentmode"] == "Live Render":
                self.autorendertext.set_text("Autorendering: " + str(data.body["autorendering"]))
                self.timertext.set_text("Timer: " + str(data.body["timer"]))

            else:
                self.autorendertext.set_text("")
                self.timertext.set_text("")
                for rect in self.borderrects + self.rects:
                    rect.remove()

            leftx = 3
            rightx = 7
            topy = 5
            bottomy = 1

            rectw = (rightx - leftx) / data.body['width']
            recth = (topy - bottomy) / data.body['height']

            if len(self.rects) == 0:
                xpos = leftx
                ypos = topy
                counter = 0
                for i in range(0, len(data.body["modulestimer"])):
                    rect = Rectangle((xpos, ypos-recth), rectw, recth)
                    rectborder = Rectangle((xpos, ypos-recth), rectw, recth, fill=False, edgecolor='black')
                    counter += 1
                    xpos += rectw
                    if counter == data.body['width']:
                        counter = 0
                        ypos -= recth
                        xpos = leftx

                    self.rects.append(rect)
                    self.borderrects.append(rectborder)
                    self.ax.add_patch(rect)
                    self.ax.add_patch(rectborder)


            maxt = max(data.body["modulestimer"])
            for i, item in enumerate(data.body["modulestimer"]):
                if maxt != 0:
                    self.rects[i].set_width(item * rectw/maxt)
                else:
                    self.rects[i].set_width(0)