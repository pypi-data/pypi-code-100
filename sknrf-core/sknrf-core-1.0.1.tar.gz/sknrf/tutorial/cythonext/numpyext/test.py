import numpy as np

from sknrf.tutorial.cythonext.numpyext import numpyext

if __name__ == "__main__":
    print("Comparing Sum Calls")
    arr = np.arange(1e6, dtype=np.float)
    numpyext.numpy_sum(arr)
    numpyext.cython_sum(arr)

