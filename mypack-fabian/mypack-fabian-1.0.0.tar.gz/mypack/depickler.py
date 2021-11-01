import pickle

# = pickle lister

# ¤ writes object to list from file


def depickler(filename):
    pickle_file = open(filename, "rb")
    objects = []
    while True:
        try:
            objects.append(pickle.load(pickle_file))
        except EOFError:
            break
    pickle_file.close()
    return objects
