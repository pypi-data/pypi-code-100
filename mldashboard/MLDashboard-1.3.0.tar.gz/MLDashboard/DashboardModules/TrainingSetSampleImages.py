from MLDashboard.DashboardModules.ImageModule import ImageModule
from MLDashboard.MLCommunicationBackend import MessageMode

class TrainingSetSampleImages(ImageModule):
    def __init__(self, ax, config):
        """
        Shows a set of sample images from the training set.

        :param ax: matplotlib ax
        :param config: Config info with the keys width and height for the image and rows and cols for the plot
        """
        super().__init__(ax, config, "Training Set Sample Images", MessageMode.Train_Set_Sample)

    def initialRequests(self):
        return self.generateRequest()

    def update(self, data):
        if data.mode == MessageMode.Train_Set_Sample:
            images = self.createImages(data.body['x'])
            text = data.body['y']
            self.updateImageGrid(images, text)

        elif data.mode == MessageMode.Epoch_End:
            self.updateImageGrid()
            return self.generateRequest()
