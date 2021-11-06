import numpy as np

from sknrf.tutorial.cythonext.pythonext import pythonext

if __name__ == "__main__":
    print("Comparing Fibonancii Sequency Calls")
    print(pythonext.python_fib(30))
    print(pythonext.cython_fib(30))

    print("Comparing def, cdef and cpdef Calls")
    x = np.array([2.0, 3.5, 3.2], dtype=np.float)
    y = np.array([1.0, 2.5, 3.0], dtype=np.float)
    print("def: " + str(pythonext.def_distance(x, y)))
    print("cdef cannot be called from python")
    print("cpdef: " + str(pythonext.cpdef_distance(x, y)))