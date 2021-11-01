import numpy as np
import trojai.data
from trojai.data.MemoryBank import DimReductionMemBank
import torch
from trojai.estimators.PytorchClassifier import NetWrapper
from sklearn.decomposition import PCA

class LatentDimReduce:
    def __init__(self, network, latent_layer=-2, device=None, dim_reduce_class=PCA, **dim_reducer_kwargs):
        '''

        :param network: Network with which to extract latents from. Can be Pytorch network, or TrojPytorchClassifier.
        :param latent_layer: The latent layer from which to extract the representations.
        :param device: The device network is on. If None, if a GPU exists, it is used, otherwise the CPU is used.
        :param dim_reduce_class: The uninitialized class used for the dimensionality reduction. It must have a fit_transform method.
        :param dim_reducer_kwargs:`Keyword arguments for dimensionality reducer.
        '''
        if type(network).__name__==TrojPytorchClassifier:
            network = network._model
        self.device = device
        if self.device==None:
            self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.network_latent_output = NetWrapper(network, latent_layer)
        self.dim_reducer = dim_reduce_class(**dim_reducer_kwargs)
        self.memory_bank = DimReductionMemBank(size=0)

    def populate_memory(self,loader):
        '''
        #TODO allow for select number of batches.
        Populates the memorybank with latent representations as numpy arrays.
        :param loader: Troj dataloader.
        :return: Populated memory bank.
        '''
        #TODO add tracking (instances added to memory vs. instances left)
        for batch_idx, (data, target, index) in enumerate(loader):
            if type(data) is np.ndarray:
                data = torch.from_numpy(data).to(self.device)
            latents = self.network_latent_output(data)
            latents = latents.detach().cpu().numpy()
            self.memory_bank.update(latents, index)


    def fit_reducer(self):
        '''
        Fits the dimensionality reduction algorithm and transforms the latents in the memory bank.
        :return: The embedded latents and the indices of the corresponding sampels in the dataframe.
        '''
        latents, indices = self.memory_bank.get_all()
        latents = np.asarray(latents)
        reduced = self.dim_reducer.fit_transform(latents)
        return reduced, indices

    def fit_transform(self, loader):
        '''
        Populates the memory bank, then fits the dimensionality reducer and transforms the latents accordingly.
        :param loader: Dataloader
        :return: The embedded latents and the indices of the corresponding sampels in the dataframe.
        '''
        self.populate_memory(loader)
        reduced, indices = self.fit_reducer()
        return reduced, indices

    def run(self, loader, df):
        '''
        Given a dataloader and a dataframe, it populates the memory bank, fits and transforms the data, then adds the
        new representations to the dataframe accordingly.
        :param loader: Dataloader.
        :param df: Dataframe to lof the data to.
        :return: The updated dataframe.
        '''
        reduced, indices = self.fit_transform(loader)
        as_dict = {'embedding':reduced}
        df = trojai.data.log_to_dataframe(df, indices, as_dict)
        return df