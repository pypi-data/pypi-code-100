from numpy import poly1d


def lagrange(x, y):
    k = x.size
    result = poly1d(0.0)
    for j in range(k):
        sproduct = poly1d(1.0)
        for m in range(k):
            if m == j:
                continue
            sproduct *= poly1d([1.0, - x[m]]) / (x[j] - x[m])
        result += sproduct * y[j]
    return result
