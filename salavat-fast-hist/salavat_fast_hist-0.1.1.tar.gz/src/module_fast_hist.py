from typing import List, Tuple, Union
import numpy as np

def fast_hist(array: List[Union[int, float]], 
              bins: int) -> Tuple[List[int], List[float]]:
    mx = max(array)
    mn = min(array)
    bin_len = (mx - mn) / bins
    result = [0] * bins
    for el in array:
        ind = min((el - mn) / bin_len,  bins - 1)
        ind = int(ind)
        result[ind]+=1;
    return result, list([i for i in np.arange(mn, mx, bin_len)])
