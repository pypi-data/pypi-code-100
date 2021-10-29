import math, numpy
def get_square_root(x):
	return math.sqrt(x)
def sigmoid(x):
	return 1 / (1 + (math.e ** -x))
def get_zeros(dim):
	return numpy.zeros(shape = dim)