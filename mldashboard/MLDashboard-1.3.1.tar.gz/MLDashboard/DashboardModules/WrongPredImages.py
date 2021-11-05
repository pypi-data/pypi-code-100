from MLDashboard.DashboardModules.ImageModule import ImageModule
from MLDashboard.MLCommunicationBackend import MessageMode

class WrongPredImages(ImageModule):
    def __init__(self, ax, config):
        """
        Shows a set of sample incorrect predictions from the prediction set.

        :param ax: matplotlib ax
        :param config: Config info with the keys width and height for the image and rows and cols for the plot
        """
        super().__init__(ax, config, "Incorrect Predictions", MessageMode.Wrong_Pred_Sample)
        for key, value in {'correctcolor': 'green', 'incorrectcolor': 'red', 'attempts': 1000}.items():
            if key not in self.config:
                self.config[key] = value

    def update(self, data):
        if data.mode == MessageMode.Wrong_Pred_Sample:
            images = self.createImages(data.body['x'])
            text = []
            color = []
            for i in range(0, len(images)):
                text.append(str(data.body['pred'][i]) + " : " + str(data.body['y'][i]))
                color.append(self.config['incorrectcolor'])
            self.updateImageGrid(images, text, color)

        elif data.mode == MessageMode.Epoch_End:
            self.updateImageGrid()
            return self.generateRequest(attempts=self.config['attempts'])