import pickle
from itertools import count, takewhile


def frange(start, stop, step):
    return takewhile(lambda x: x < stop, count(start, step))


def load_pickle_file(file):
    pkl_file = open(file, 'rb')
    obj = pickle.load(pkl_file)
    pkl_file.close()

    return obj
