import pickle

# = pickle saver

# ¤ Saves object to file


def picklify(obj_list, filename):
    with open(filename, "wb") as file:  # ¤ Overwrites any existing file.
        for i in range(len(obj_list)):
            pickle.dump(obj_list[i], file, pickle.HIGHEST_PROTOCOL)
        file.close()

