import numpy as np
from queue import Queue
from sklearn.neighbors import NearestNeighbors
import numpy.random

class MemBank:
    #TODO random instantiation
    '''
    Memory bank base class. Allows one to create and update a memory bank with parameter size being the maximum number of entries.
    '''
    def __init__(self, size=4096, input_size=4096):
        '''

        :param size:  Number of entries in the memory bank. Set to 0 for arbitrarily large memory.
        :param input_size: Size of each entry in the bank.
        '''
        self.size = size
        self.bank = Queue(maxsize = size)
        self.input_size = input_size

    def random_init(self):
        '''
        Initializes the memory bank with random vectors.
        :return:
        '''
        for i in range(self.size):
            random = np.random.rand(self.input_size)
            self.bank.put(random)

    def update(self, new_input):
        '''
        Updates the memory bank with new input.
        :param new_input: Input to add to memory bank.
        :return: Adds items to memory bank, removing the oldest entries if the bank is full.
        '''
        for new_item in new_input:
            if self.bank.full() == True:
                self.bank.get()
            self.bank.put(new_item)

    def get_all(self):
        '''

        :return: All elements in the memeory bank as a list.
        '''
        return list(self.bank.queue)


class DimReductionMemBank(MemBank):
    '''
    Memory bank for using dimensionality reduction algorithms
    '''
    def __init__(self, size=0, input_size=128):
        super().__init__(size, input_size)
        self.idx_bank = Queue(maxsize = size)

    def update(self, new_input, new_input_idx):
        '''
        Updates the memory bank with new input.
        :param new_input: Input to add to memory bank.
        :return: Adds items to memory bank, removing the oldest entries if the bank is full.
        '''
        for new_item_ind in range(new_input.shape[0]):
            if self.bank.full() == True:
                self.bank.get()
                self.idx_bank.get()
            self.bank.put(new_input[new_item_ind])
            self.idx_bank.put(new_input_idx[new_item_ind])

    def get_all(self):
        '''

        :return: All elements in the memeory bank as a list.
        '''
        return list(self.bank.queue), list(self.idx_bank.queue)