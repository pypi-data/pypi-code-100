import collections


def stringify_obj(x):
    """Stringify complex built-in data structure
    """
    if isinstance(x, dict):
        return '\t'.join(f"{k}: {stringify_obj(v)}" for k, v in x.items())
    if isinstance(x, list) or isinstance(x, tuple):
        return ', '.join(stringify_obj(item) for item in x)
    if isinstance(x, int) or isinstance(x, float):
        return str(x)
    if isinstance(x, str):
        return x
    raise Exception(f'Unexpected data type {type(x)}!')



def flatten(d:dict, parent_key='', sep='.'):
    """Flatten nested dictionary and compress key

    Parameters
    ----------
    d : dict
        A nested dictionary to flatten.
    parent_key : str, optional
        Prefix to prepend to flatten dict keys, by default ''
    sep : str, optional
        Seperator between keys, by default '.'

    Returns
    -------
    dict
        A flatten dictionary
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)