from lightSOM.k_som import KSOM

class SOM():
    def __init__(self, backend="classic"):
        self.backend=backend


    def create(self, width, height, data,normalizer="var",lattice="hexa", feature_names=[], loadFile=None, pci=0, pbc=0):
        if self.backend=='classic':
            return KSOM(width, height, data, normalizer,lattice, feature_names, loadFile, pci, pbc)