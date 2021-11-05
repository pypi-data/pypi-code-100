import random
from titania.data.data_core import TitaniaDataInterface


class RandomNList(TitaniaDataInterface):
    def __init__(self, n=10):
        self.n = n

    def fetch(self):
        return [random.random() for i in range(self.n)]
