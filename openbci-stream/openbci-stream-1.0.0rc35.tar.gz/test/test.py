from openbci_stream.utils import HDF5Reader
from matplotlib import pyplot as plt
import numpy as np


filename = 'raspad/record-10_25_21-17_08_08.L.h5'

with HDF5Reader(filename) as reader:
    eeg = reader.eeg
    mk = reader.markers
    data = reader.get_data()
    print(reader)


eeg
