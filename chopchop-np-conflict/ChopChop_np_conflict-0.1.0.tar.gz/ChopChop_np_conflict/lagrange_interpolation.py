import numpy as np

"""
Params: 
    x: x observed coords
    y: y observed coords
Returns:
    np.poly1d lagrange interpolation polynomial 
"""
def lagrange_interp(x, y):
    len_x = len(x)
    result = np.poly1d(0.)
    for i in range(len_x):
        y_i = np.poly1d(y[i])
        for j in range(len_x):
            if i == j:
                continue
            y_i *= np.poly1d([1., -x[j]]) / (x[i] - x[j])
        result += y_i
    return result
