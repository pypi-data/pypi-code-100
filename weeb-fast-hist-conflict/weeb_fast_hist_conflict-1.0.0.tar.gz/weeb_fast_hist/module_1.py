import matplotlib as plt

from typing import List, Tuple, Union

def fast_hist(array: List[Union[int, float]], 
              bins: int) -> Tuple[List[int], List[float]]:
    """
    Builds bins' labels and bins' value counts for given array
    :param array: array with numeric values
    :param bins:  number of bins in result distribution
    :return: Two lists: 
             first contains value counts of each bin,
             second contains list of bins' labels
    """
    _sorted = sorted(array)
    shift = (_sorted[-1] - _sorted[0]) / bins
    bins_names = [_sorted[0] + shift * t for t in range(bins + 1)]
    value_counts = []
    right = 0
    for left in range(len(bins_names) - 1):
        while (right < len(_sorted) and _sorted[right] < bins_names[left]):
            right = right + 1
        count = 0
        while (right < len(_sorted) and _sorted[right] < bins_names[left] + shift):
            right = right + 1
            count = count + 1
        value_counts.append(count)
    count = 0
    while (right < len(_sorted) and _sorted[right] <= bins_names[left] + shift):
        right = right + 1
        count = count + 1
    value_counts[-1] += count
    plt.bar(bins_names[:-1], value_counts, align='edge', width=shift)
    return (value_counts, bins_names)