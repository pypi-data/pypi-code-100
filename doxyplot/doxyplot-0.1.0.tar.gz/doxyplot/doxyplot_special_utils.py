import math
from operator import itemgetter

def prepare_xy_data_from_file(filename, columns=2):
    """Prepares two lists based on data in txt file"""
    with open(filename) as f:
        lines = f.readlines()
        # print(lines)
        x = [line.split()[0] for line in lines]
        try:
            y = [line.split()[1] for line in lines]
        except:
            y = [line.replace("\n", "") for line in lines]
            y = [line.split(" ")[1] for line in lines]
        if columns == 3:
            y2 = [line.split()[2] for line in lines]
    for i in range(len(x)):
        x[i] = float(x[i])

    for i in range(len(y)):
        try:
            y[i] = float(y[i])
        except:
            print(y[i])
    if columns == 3:
        for i in range(len(y2)):
            y2[i] = float(y2[i])
        return (x, y, y2)
    return (x, y)


def sort_depth_value(x, y):
    """Sorts values according to the depth, x ... value, y ... depth"""
    assert len(x) == len(y)
    list1 = [[x[i], y[i]] for i in range(len(x))]

    list1 = sorted(list1, key=itemgetter(0))
    x = [item[0] for item in list1]
    y = [item[1] for item in list1]

    return (x, y)


def logarithmic(x):
    """recalculates whole list of values to decadic logarithm - used in plots"""
    for i in range(len(x)):
        if x[i] <= 0:
            x[i] = 1e-10
        x[i] = math.log10(x[i])
    return x


def load_data(filepath, sort=False):
    x, y = prepare_xy_data_from_file(filepath)
    if sort:
        x, y = sort_depth_value(x, y)
    return (x, y)
