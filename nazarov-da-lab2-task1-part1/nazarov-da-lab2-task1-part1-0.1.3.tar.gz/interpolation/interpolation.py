import numpy as np


def lagrange(x: np.ndarray, y: np.ndarray):
    n = len(x)
    basis_polynomial_divisors = np.empty((n, ), dtype=np.float64)

    for i in range(n):
        _divisors_vector = np.subtract(x[i], x)
        _divisors_vector[i] = 1
        basis_polynomial_divisors[i] = _divisors_vector.prod()

    def _interpolation(x_):
        L = np.empty((n, ), dtype=np.float64)
        for i in range(n):
            coefs_vector = np.subtract(x_, x)
            coefs_vector[i] = 1
            L[i] = np.divide(coefs_vector.prod(), basis_polynomial_divisors[i])
        return np.sum(np.multiply(y, L))

    return np.vectorize(_interpolation)