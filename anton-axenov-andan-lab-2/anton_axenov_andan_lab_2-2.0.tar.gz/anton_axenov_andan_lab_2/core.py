from typing import List, Tuple, Union
import math
import numpy as np

def fast_hist(array: List[Union[int, float]],
              bins: int) -> Tuple[List[int], List[float]]:
    
    minBin = array.min()
    binsContent = np.zeros((bins,), dtype=int)
    bin_size = int(math.ceil((array.max()-minBin)/bins))

    for element in array:
        x = (element-minBin) // bin_size
        binsContent[x]+=1
    return (np.array([int(x) for x in binsContent]), [minBin + i*bin_size for i in range(0, bins)])