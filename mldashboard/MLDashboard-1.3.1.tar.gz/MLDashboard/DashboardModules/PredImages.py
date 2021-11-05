from MLDashboard.DashboardModules.ImageModule import ImageModule
from MLDashboard.MLCommunicationBackend import MessageMode

class PredImages(ImageModule):
    def __init__(self, ax, config):
        """
        Shows a set of sample predictions from the prediction set.

        :param ax: matplotlib ax
        :param config: Config info with the keys width and height for the image and rows and cols for the plot
        """
        super().__init__(ax, config, "Sample Predictions", MessageMode.Pred_Sample)
        if "correctcolor" not in self.config:
            self.config['correctcolor'] = 'green'
        if "incorrectcolor" not in self.config:
            self.config['incorrectcolor'] = 'red'


    def update(self, data):
        if data.mode == MessageMode.Pred_Sample:
            images = self.createImages(data.body['x'])
            text = []
            color = []
            for i in range(0, len(images)):
                text.append(str(data.body['pred'][i]) + " : " + str(data.body['y'][i]))
                if str(data.body['pred'][i]) == str(data.body['y'][i]):
                    color.append(self.config['correctcolor'])
                else:
                    color.append(self.config['incorrectcolor'])

            self.updateImageGrid(images, text, color)

        elif data.mode == MessageMode.Epoch_End:
            self.updateImageGrid()
            return self.generateRequest()