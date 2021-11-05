"""
Module containing functions that binary_c-python uses to modify
dictionaries.
"""
import copy
import collections
import astropy.units as u
import numpy as np
from collections import (
    OrderedDict,
)

# we need to convert keys to floats:
# this is ~ a factor 10 faster than David's
# recursive_change_key_to_float routine,
# probably because this version only does
# the float conversion, nothing else.
def keys_to_floats(json_data):
    # assumes nested dicts ...
    # new_data = {}

    # but this copies the variable type, but has some
    # pointless copying
    # new_data = copy.copy(json_data)
    # new_data.clear()

    # this adopts the type correctly *and* is fast
    new_data = type(json_data)()

    for k, v in json_data.items():
        if isinstance(v, list):
            v = [
                keys_to_floats(item)
                if isinstance(item, collections.abc.Mapping)
                else item
                for item in v
            ]
        elif isinstance(v, collections.abc.Mapping):
            # dict, ordereddict, etc.
            v = keys_to_floats(v)
        try:
            f = float(k)
            new_data[f] = json_data[k]
        except:
            new_data[k] = v
    return new_data


def recursive_change_key_to_float(input_dict):
    """
    Function to recursively change the key to float

    This only works if the dict contains just sub-dicts or numbers/strings.
    Does not work with lists as values
    """

    new_dict = collections.OrderedDict()  # TODO: check if this still works

    for key in input_dict:
        if isinstance(input_dict[key], (dict, collections.OrderedDict)):
            try:
                num_key = float(key)
                new_dict[num_key] = recursive_change_key_to_float(
                    copy.deepcopy(input_dict[key])
                )
            except ValueError:
                new_dict[key] = recursive_change_key_to_float(
                    copy.deepcopy(input_dict[key])
                )
        else:
            try:
                num_key = float(key)
                new_dict[num_key] = input_dict[key]
            except ValueError:
                new_dict[key] = input_dict[key]

    return new_dict


def recursive_change_key_to_string(input_dict):
    """
    Function to recursively change the key back to a string but this time in a format that we decide
    """

    new_dict = collections.OrderedDict()  # TODO: check if this still works

    for key in input_dict:
        if isinstance(input_dict[key], (dict, collections.OrderedDict)):
            if isinstance(key, (int, float)):
                string_key = "{:g}".format(key)
                new_dict[string_key] = recursive_change_key_to_string(
                    copy.deepcopy(input_dict[key])
                )
            else:
                new_dict[key] = recursive_change_key_to_string(
                    copy.deepcopy(input_dict[key])
                )
        else:
            if isinstance(key, (int, float)):
                string_key = "{:g}".format(key)
                new_dict[string_key] = input_dict[key]
            else:
                new_dict[key] = input_dict[key]

    return new_dict


############################################################
# code to walk a dictionary recursively based on
# https://stackoverflow.com/questions/13687924/setting-a-value-in-a-nested-python-dictionary-given-a-list-of-indices-and-value
def _nested_set(dic, keys, value):
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value


def _nested_get(dic, keys):
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    return dic[keys[-1]]


# function to walk through the dictionary, multiplying
# only float values by a const
def _recursive_normalize_floats(path, d, const, parent=None, ignore=None):
    if not parent:
        parent = d
    for k, v in d.items():
        if ignore and k in ignore:
            continue

        if isinstance(v, float):
            path.append(k)
            # must be a float, multiply by the constant
            _nested_set(parent, path, v * const)
            path.pop()
        elif isinstance(v, str) or isinstance(v, int):
            path.append(k)
            # do nothing to strings or ints
            path.pop()
        elif v is None:
            path.append(k)
            path.pop()
        # dicts
        # note: isinstance isn't enough, we need to check the Mapping
        elif isinstance(v, collections.abc.Mapping):
            path.append(k)
            # nested dict
            _recursive_normalize_floats(path, v, const, parent=parent)
            path.pop()
        else:
            print(
                "###Type {} not recognized: {}.{}={}".format(
                    type(v), ".".join(path), k, v
                )
            )


def multiply_float_values(d, const, ignore=None):
    """
    multiply_float_values : A function to recursively multiply values of a (nested) dictionary that are floats by a constant. Nested dictionaries call this function recursively.

    Args:
        d = the dictionary
        const = the constant that multiplies float values
    """
    path = []
    _recursive_normalize_floats(path, d, const, parent=d, ignore=ignore)


def subtract_dicts(dict_1: dict, dict_2: dict) -> dict:
    """
    Function to subtract two dictionaries.

    Only allows values to be either a dict or a numerical type

    For the overlapping keys (key name present in both dicts):
        When the keys are of the same type:
            - If the types are of numerical type: subtract the value at dict 2 from dict 1.
            - If the types are both dictionaries: call this function with the subdicts

        When the keys are not of the same type:
            - if the keys are all of numerical types

    For the unique keys:
        - if the key is from dict 1: adds the value to the new dict (be it numerical value or dict)
        - If the key is from dict 2: Adds the negative of its value in case of numerical type.
            if the type is a dict, the result of subtract_dicts({}, dict_2[key]) will be set

    If the result is 0, the key will be removed from the resulting dict.
    If that results in an empty dict, the dict will be removed too.

    Args:
        dict_1: first dictionary
        dict_2: second dictionary

    Returns:
        Subtracted dictionary
    """

    # Set up new dict
    new_dict = {}

    # Define allowed numerical types
    ALLOWED_NUMERICAL_TYPES = (float, int, np.float64)

    #
    keys_1 = dict_1.keys()
    keys_2 = dict_2.keys()

    # Find overlapping keys of both dicts
    overlapping_keys = set(keys_1).intersection(set(keys_2))

    # Find the keys that are unique
    unique_to_dict_1 = set(keys_1).difference(set(keys_2))
    unique_to_dict_2 = set(keys_2).difference(set(keys_1))

    # Add the unique keys to the new dict
    for key in unique_to_dict_1:
        # If these items are numerical types
        if isinstance(dict_1[key], ALLOWED_NUMERICAL_TYPES):
            new_dict[key] = dict_1[key]
            if new_dict[key] == 0:
                del new_dict[key]

        # Else, to be safe we should deepcopy them
        elif isinstance(dict_1[key], dict):
            copy_dict = copy.deepcopy(dict_1[key])
            new_dict[key] = copy_dict
        else:
            msg = "Error: using unsupported type for key {}: {}".format(
                key, type(dict_1[key])
            )
            print(msg)
            raise ValueError(msg)

    # Add the unique keys to the new dict
    for key in unique_to_dict_2:
        # If these items are numerical type, we should add the negative of the value
        if isinstance(dict_2[key], ALLOWED_NUMERICAL_TYPES):
            new_dict[key] = -dict_2[key]
            if new_dict[key] == 0:
                del new_dict[key]

        # Else we should place the negative of that dictionary in the new place
        elif isinstance(dict_2[key], dict):
            new_dict[key] = subtract_dicts({}, dict_2[key])
        else:
            msg = "Error: using unsupported type for key {}: {}".format(
                key, type(dict_2[key])
            )
            print(msg)
            raise ValueError(msg)

    # Go over the common keys:
    for key in overlapping_keys:

        # See whether the types are actually the same
        if not type(dict_1[key]) is type(dict_2[key]):
            # Exceptions:
            if (type(dict_1[key]) in ALLOWED_NUMERICAL_TYPES) and (
                type(dict_2[key]) in ALLOWED_NUMERICAL_TYPES
            ):
                # We can safely subtract the values since they are all numeric
                new_dict[key] = dict_1[key] - dict_2[key]
                if new_dict[key] == 0:
                    del new_dict[key]

            else:
                msg = "Error key: {} value: {} type: {} and key: {} value: {} type: {} are not of the same type and cannot be merged".format(
                    key,
                    dict_1[key],
                    type(dict_1[key]),
                    key,
                    dict_2[key],
                    type(dict_2[key]),
                )

                print(msg)
                raise ValueError(msg)

        # This is where the keys are the same
        else:
            # If these items are numeric types
            if isinstance(dict_1[key], ALLOWED_NUMERICAL_TYPES):
                new_dict[key] = dict_1[key] - dict_2[key]

                # Remove entry if the value is 0
                if new_dict[key] == 0:
                    del new_dict[key]

            # Else, to be safe we should deepcopy them
            elif isinstance(dict_1[key], dict):
                new_dict[key] = subtract_dicts(dict_1[key], dict_2[key])

                # Remove entry if it results in an empty dict
                # TODO: write test to prevent empty dicts from showing up
                if not new_dict[key]:
                    del new_dict[key]
            else:
                msg = "Error: using unsupported type for key {}: {}".format(
                    key, type(dict_2[key])
                )
                print(msg)
                raise ValueError(msg)

    #
    return new_dict


class AutoVivificationDict(dict):
    """
    Implementation of perl's autovivification feature, by overriding the
    get item and the __iadd__ operator (https://docs.python.org/3/reference/datamodel.html?highlight=iadd#object.__iadd__)

    This allows to set values within a subdict that might not exist yet:

    Example:
        newdict = {}
        newdict['example']['mass'] += 10
        print(newdict)
        >>> {'example': {'mass': 10}}
    """

    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

    def __iadd__(self, other):
        # if a value does not exist, assume it is 0.0
        try:
            self += other
        except:
            self = other
        return self


def inspect_dict(
    input_dict: dict, indent: int = 0, print_structure: bool = True
) -> dict:
    """
    Function to (recursively) inspect a (nested) dictionary.
    The object that is returned is a dictionary containing the key of the input_dict, but as value
    it will return the type of what the value would be in the input_dict

    In this way we inspect the structure of these dictionaries, rather than the exact contents.

    Args:
        input_dict: dictionary you want to inspect
        print_structure: (optional, default = True)
        indent: (optional, default = 0) indent of the first output

    Returns:
        Dictionary that has the same structure as the input_dict, but as values it has the
            type(input_dict[key]) (except if the value is a dict)
    """

    structure_dict = collections.OrderedDict()  # TODO: check if this still works

    #
    for key, value in input_dict.items():
        structure_dict[key] = type(value)

        if print_structure:
            print("\t" * indent, key, type(value))

        if isinstance(value, dict):
            structure_dict[key] = inspect_dict(
                value, indent=indent + 1, print_structure=print_structure
            )

    return structure_dict


def count_keys_recursive(input_dict):
    """
    Function to count the total number of keys in a dictionary
    """

    local_count = 0
    for key in input_dict.keys():
        local_count += 1
        if isinstance(input_dict[key], (dict, collections.OrderedDict)):
            local_count += count_keys_recursive(input_dict[key])
    return local_count


def merge_dicts(dict_1: dict, dict_2: dict) -> dict:
    """
    Function to merge two dictionaries in a custom way.

    Behaviour:

    When dict keys are only present in one of either:
        - we just add the content to the new dict

    When dict keys are present in both, we decide based on the value types how to combine them:
        - dictionaries will be merged by calling recursively calling this function again
        - numbers will be added
        - (opt) lists will be appended
        - In the case that the instances do not match: for now I will raise an error

    Args:
        dict_1: first dictionary
        dict_2: second dictionary

    Returns:
        Merged dictionary

    """

    # Set up new dict
    new_dict = collections.OrderedDict()  # TODO: check if this still necessary

    #
    keys_1 = dict_1.keys()
    keys_2 = dict_2.keys()

    # Find overlapping keys of both dicts
    overlapping_keys = set(keys_1).intersection(set(keys_2))

    # Find the keys that are unique
    unique_to_dict_1 = set(keys_1).difference(set(keys_2))
    unique_to_dict_2 = set(keys_2).difference(set(keys_1))

    # Add the unique keys to the new dict
    for key in unique_to_dict_1:
        # If these items are ints or floats, then just put them in
        if isinstance(dict_1[key], (float, int)):
            new_dict[key] = dict_1[key]
        # Else, to be safe we should deepcopy them
        else:
            copy_dict = copy.deepcopy(dict_1[key])
            new_dict[key] = copy_dict

    for key in unique_to_dict_2:
        # If these items are ints or floats, then just put them in
        if isinstance(dict_2[key], (float, int)):
            new_dict[key] = dict_2[key]
        # Else, to be safe we should deepcopy them
        else:
            copy_dict = copy.deepcopy(dict_2[key])
            new_dict[key] = copy_dict

    # Go over the common keys:
    for key in overlapping_keys:

        # If they keys are not the same, it depends on their type whether we still deal with them at all, or just raise an error
        if not type(dict_1[key]) is type(dict_2[key]):
            # Exceptions: numbers can be added
            if isinstance(dict_1[key], (int, float, np.float64)) and isinstance(
                dict_2[key], (int, float, np.float64)
            ):
                new_dict[key] = dict_1[key] + dict_2[key]

            # Exceptions: versions of dicts can be merged
            elif isinstance(
                dict_1[key], (dict, collections.OrderedDict, type(AutoVivificationDict))
            ) and isinstance(
                dict_2[key], (dict, collections.OrderedDict, type(AutoVivificationDict))
            ):
                new_dict[key] = merge_dicts(dict_1[key], dict_2[key])

            # If the above cases have not dealt with it, then we should raise an error
            else:
                print(
                    "Error key: {} value: {} type: {} and key: {} value: {} type: {} are not of the same type and cannot be merged".format(
                        key,
                        dict_1[key],
                        type(dict_1[key]),
                        key,
                        dict_2[key],
                        type(dict_2[key]),
                    )
                )
                raise ValueError

        # Here we check for the cases that we want to explicitly catch. Ints will be added,
        # floats will be added, lists will be appended (though that might change) and dicts will be
        # dealt with by calling this function again.
        else:
            # ints
            # Booleans (has to be the type Bool, not just a 0 or 1)
            if isinstance(dict_1[key], bool) and isinstance(dict_2[key], bool):
                new_dict[key] = dict_1[key] or dict_2[key]

            elif isinstance(dict_1[key], int) and isinstance(dict_2[key], int):
                new_dict[key] = dict_1[key] + dict_2[key]

            # floats
            elif isinstance(dict_1[key], float) and isinstance(dict_2[key], float):
                new_dict[key] = dict_1[key] + dict_2[key]

            # lists
            elif isinstance(dict_1[key], list) and isinstance(dict_2[key], list):
                new_dict[key] = dict_1[key] + dict_2[key]

            # Astropy quantities (using a dummy type representing the numpy array)
            elif isinstance(dict_1[key], type(np.array([1]) * u.m)) and isinstance(
                dict_2[key], type(np.array([1]) * u.m)
            ):
                new_dict[key] = dict_1[key] + dict_2[key]

            # dicts
            elif isinstance(dict_1[key], dict) and isinstance(dict_2[key], dict):
                new_dict[key] = merge_dicts(dict_1[key], dict_2[key])

            else:
                print(
                    "Object types {}: {} ({}), {} ({}) not supported.".format(
                        key,
                        dict_1[key],
                        type(dict_1[key]),
                        dict_2[key],
                        type(dict_2[key]),
                    )
                )
                raise ValueError

    #
    return new_dict


def update_dicts(dict_1: dict, dict_2: dict) -> dict:
    """
    Function to update dict_1 with values of dict_2 in a recursive way.

    Behaviour:

    When dict keys are only present in one of either:
        - we just add the content to the new dict

    When dict keys are present in both, we decide based on the value types how to combine them:
        - value of dict2 will be taken

    Args:
        dict_1: first dictionary
        dict_2: second dictionary

    Returns:
        New dictionary with Updated values

    """

    # Set up new dict of the same type as dict_1
    #
    # Note: setting directly to OrderedDict fails in some cases
    # so instead we take a (shallow) copy of dict_1 which will
    # have the same type as dict_1, then clear it. (There must
    # be a better way to do this...)
    new_dict = dict_1.copy()  # OrderedDict()  # TODO: check if this still works
    new_dict.clear()

    keys_1 = dict_1.keys()
    keys_2 = dict_2.keys()

    # Find overlapping keys of both dicts
    overlapping_keys = set(keys_1).intersection(set(keys_2))

    # Find the keys that are unique
    unique_to_dict_1 = set(keys_1).difference(set(keys_2))
    unique_to_dict_2 = set(keys_2).difference(set(keys_1))

    # Add the unique keys to the new dict
    for key in unique_to_dict_1:
        # If these items are ints or floats, then just put them in
        if isinstance(dict_1[key], (float, int)):
            new_dict[key] = dict_1[key]
        # Else, to be safe we should deepcopy them
        else:
            copy_dict = copy.deepcopy(dict_1[key])
            new_dict[key] = copy_dict

    for key in unique_to_dict_2:
        # If these items are ints or floats, then just put them in
        if isinstance(dict_2[key], (float, int)):
            new_dict[key] = dict_2[key]
        # Else, to be safe we should deepcopy them
        else:
            copy_dict = copy.deepcopy(dict_2[key])
            new_dict[key] = copy_dict

    # Go over the common keys:
    for key in overlapping_keys:

        # See whether the types are actually the same
        if not type(dict_1[key]) is type(dict_2[key]):
            # Exceptions:
            if (type(dict_1[key]) in [int, float]) and (
                type(dict_2[key]) in [int, float]
            ):
                new_dict[key] = dict_2[key]

            else:
                print(
                    "Error key: {} value: {} type: {} and key: {} value: {} type: {} are not of the same type and cannot be merged".format(
                        key,
                        dict_1[key],
                        type(dict_1[key]),
                        key,
                        dict_2[key],
                        type(dict_2[key]),
                    )
                )
                raise ValueError

        # Here we check for the cases that we want to explicitly catch. Ints will be added,
        # floats will be added, lists will be appended (though that might change) and dicts will be
        # dealt with by calling this function again.
        else:
            # dicts
            if isinstance(dict_1[key], dict) and isinstance(dict_2[key], dict):
                new_dict[key] = update_dicts(dict_1[key], dict_2[key])
            else:
                new_dict[key] = dict_2[key]

    #
    return new_dict


def multiply_values_dict(input_dict, factor):
    """
    Function that goes over dictionary recursively and multiplies the value if possible by a factor

    If the key equals "general_info", the multiplication gets skipped
    """

    for key in input_dict:
        if not key == "general_info":
            if isinstance(input_dict[key], (dict, collections.OrderedDict)):
                input_dict[key] = multiply_values_dict(input_dict[key], factor)
            else:
                if isinstance(input_dict[key], (int, float)):
                    input_dict[key] = input_dict[key] * factor

    return input_dict


def custom_sort_dict(input_dict):
    """
    Returns a dictionary that is ordered, but can handle numbers better than normal OrderedDict

    When the keys of the current dictionary are of mixed type, we first find all the unique types.
    Sort that list of type names. Then find the values that fit that type.
    Sort those and append them to the sorted keys list.
    This is done until all the keys are sorted.

    All objects other than dictionary types are directly return as they are
    """

    # If the new input is a dictionary, then try to sort it
    if isinstance(input_dict, (dict, collections.OrderedDict)):
        new_dict = collections.OrderedDict()

        keys = input_dict.keys()

        # Check if types are the same
        all_types_keys = []
        for key in keys:
            if not type(key) in all_types_keys:
                all_types_keys.append(type(key))

        # If there are multiple types, then we loop over them and do a piece wise sort
        if len(all_types_keys) > 1:
            msg = "Different types in the same dictionary key set"

            # Create a string repr of the type name to sort them afterwards
            str_types = {repr(el): el for el in all_types_keys}

            # Set up sorted keys list
            sorted_keys = []

            for key_str_type in sorted(str_types.keys()):
                cur_type = str_types[key_str_type]

                cur_list = [key for key in keys if isinstance(key, cur_type)]
                cur_sorted_list = sorted(cur_list)

                sorted_keys = sorted_keys + cur_sorted_list
        else:
            sorted_keys = sorted(keys)

        for key in sorted_keys:
            new_dict[key] = custom_sort_dict(copy.deepcopy(input_dict[key]))

        return new_dict
    return input_dict


def filter_dict(arg_dict: dict, filter_list: list) -> dict:
    """
    Function to filter out keys that are contains in filter_list

    Args:
        arg_dict: dictionary containing the argument + default key pairs of binary_c
        filter_list: lists of keys to be filtered out
    Returns:
        filtered dictionary
    """

    new_dict = arg_dict.copy()

    for key in filter_list:
        if key in new_dict:
            del new_dict[key]

    return new_dict


def filter_dict_through_values(arg_dict: dict, filter_list: list) -> dict:
    """
    Function to filter out keys that contain values included in filter_list

    Args:
        arg_dict: dictionary containing the argument + default key pairs of binary_c
        filter_list: lists of values to be filtered out
    Returns:
        filtered dictionary
    """

    new_dict = {}

    for key in arg_dict:
        if not arg_dict[key] in filter_list:
            new_dict[key] = arg_dict[key]

    return new_dict
