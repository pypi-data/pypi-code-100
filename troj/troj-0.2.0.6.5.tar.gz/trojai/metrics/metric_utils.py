import numpy as np
import operator

def get_pred_data(preds):
    """

    :param preds: predictions from object detection model.
    :return: the boxes, labels, and scores as tensors.
    """
    boxes = preds["boxes"].detach().cpu().numpy()
    labels = preds["labels"].detach().cpu().numpy()
    scores = preds["scores"].detach().cpu().numpy()
    return boxes, labels, scores


def compute_Lp_distance(x1, x2, p=np.inf):
    """
    compute Lp distance of a collection of images against another collection.

    :param x1: image collection 1
    :param x2: image collection 2
    :param p: p norm
    :return: tensor of distances
    """
    x1 = np.reshape(x1, (x1.shape[0], -1))
    x2 = np.reshape(x2, (x2.shape[0], -1))
    difference_vect = x1 - x2
    lp_distance = np.linalg.norm(difference_vect, p, axis=1)
    return lp_distance

#TODO document
def SwapKeys(old_dict, key_dict):
    '''
    Swaps the keys in old_dict to their values in key_dict.
    :param old_dict: Dictionary to be assigned new keys.
    :param key_dict: dictionary containing the same keys as old_dict, where the values are the new key values for old_dict.
    :return: A dictionary with the new key names.
    '''
    pretty_dict = {key_dict[k]: v for k, v in old_dict.items()}
    return pretty_dict

def normalize_dicts(numer_dict, denom_dict):
    '''
    Performs elementwise division between two dictionaries.
    :param numer_dict: Dictionary to divide.
    :param denom_dict: Dictionary to divide by.
    :return: Dictionary with divided values.
    '''
    new_dict = {}
    for key in list(numer_dict.keys()):
        new_dict[key] = numer_dict[key]/denom_dict[key]
    return new_dict

def sort_dict(inp):
    '''
    Sorts dictionary alphabetically.
    :param inp: Input dictionary.
    :return: Sorted dictionary.
    '''
    sorted_dict = {}
    for key in sorted(inp):
        sorted_dict[key] = inp[key]
    return sorted_dict

def add_dicts(dict_1, dict_2):
    '''
    Performs elementwise addition between two dictionaries.
    :param dict_1: First dictionary.
    :param dict_2: Second dictionary.
    :return: Elementwise sum of the dictionaries.
    '''
    new_dict = {}
    for key in list(dict_1.keys()):
        new_dict[key] = dict_1[key]+dict_2[key]
    return new_dict

def multiply_dicts(dict_1, dict_2):
    '''
    Performs elementwise multiplication between two dictionaries.
    :param dict_1: First dictionary.
    :param dict_2: Second dictionary.
    :return: Elementwise product of the dictionaries.
    '''
    new_dict = {}
    for key in list(dict_1.keys()):
        new_dict[key] = dict_1[key]*dict_2[key]
    return new_dict

def scalar_mult_dict(scalar, dict_1):
    '''
    Multiplies all values in a dictionary by a given scalar.
    :param scalar: A scalar value.
    :param dict_1: input dictionary
    :return: A dictionary containing the same key-value pairs as dict_1 with the value multiplied by the given scalar.
    '''
    new_dict = {}
    for key in list(dict_1.keys()):
        new_dict[key] = scalar*dict_1[key]
    return new_dict

def diff(first, second):
    '''
    Returns a list of the items in first that are not in second.
    :param first: A list.
    :param second: Another list.
    :return: a list of the items in first that are not in second.
    '''
    second = set(second)
    return [item for item in first if item not in second]

def argmax_dict(vals):
    '''
    Computes an argmax function on a dictionary.
    :param vals: Input dictionary
    :return: The maximum key-value (arg, val) pair as a tuple.
    '''
    arg = max(vals.items(), key=operator.itemgetter(1))[0]
    arg_val = vals[arg]
    return (arg, arg_val)

def argmin_dict(vals):
    '''
    Computes an argmin function on a dictionary.
    :param vals: Input dictionary
    :return: The minimum key-value (arg, val) pair as a tuple.
    '''
    arg = min(vals.items(), key=operator.itemgetter(1))[0]
    arg_val = vals[arg]
    return (arg, arg_val)

def sub_dicts(dict_1, dict_2):
    '''
    Performs elementwise subtraction between two dictionaries.
    :param dict_1: First dictionary.
    :param dict_2: Second dictionary.
    :return: Elementwise difference of the dictionaries.
    '''
    new_dict = {}
    for key in list(dict_1.keys()):
        new_dict[key] = dict_1[key]-dict_2[key]
    return new_dict

def ColumnMeanStd(df, column_name):
    '''
    Computes the mean and deviation of a dataframe column which has scalar values.

    :param df: Dataframe
    :param column_name: The name of the column to compute the values for.
    :return: The mean and standard deviation.
    '''
    vals = df[column_name].tolist()
    mean = round(np.mean(vals), 3)
    dev = round(np.std(vals), 3)
    return mean, dev
