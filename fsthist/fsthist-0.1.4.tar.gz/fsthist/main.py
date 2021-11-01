from typing import List, Tuple, Union
import numpy as np

def fast_hist(array: List[Union[int, float]],
              bins: int) -> Tuple[List[int], List[float]]:

    value_counts = np.array([])

    a_min = min(array)
    a_max = max(array)
    bins_value = np.linspace(a_min, a_max, bins+1)

    for elem in set(np.sort(array)):
        cnt = 0
        for i in array:
            if elem == i:
                cnt += 1
        value_counts = np.append(value_counts, cnt)

    return value_counts, bins_value
