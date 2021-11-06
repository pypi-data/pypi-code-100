import os
from PIL import Image
from neuralstyletransfer.model import Model


class NeuralStyleTransfer():

    def __init__(self):

        self.contentPath = None
        self.stylePath = None
    
    def LoadContentImage(self, path, pathType='local'):
        self.contentPath = path
        self.contentpathType = pathType
    
    def LoadStyleImage(self, path, pathType='local'):
        self.stylePath = path
        self.stylepathType = pathType
    
    def apply(self, contentWeight=1e3, styleWeight=1e-2, epochs=500):

        model = Model()
        model.setContentImage(self.contentPath, self.contentpathType)
        model.setStyleImage(self.stylePath, self.stylepathType)
        output = model.train(contentWeight, styleWeight, epochs)
        return output
        



        