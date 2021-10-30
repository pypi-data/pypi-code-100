from numpy import zeros, math
from sympy import Symbol, expand

def progressiva(array,choice):
	order= len(array)-1
	value = zeros((order + 1, order + 2))
	for i in range(0, order + 1):
		value[0][i] = array[i]
	for i in range(0, order):
		for j in range(0, order):
			if choice == "arithmetic":
				value[i + 1][j] = value[i][j + 1] - value[i][j]
			elif choice == "geometric":
				value[i + 1][j] = value[i][j + 1] / value[i][j]
	x = Symbol("x")
	if choice=="arithmetic":
		g = 1
		f = 0
		for i in range(1, order + 1):
			g = g * (x - i)
			f = f + (g * value[i][0]) / math.factorial(i)
		f = f + value[0][0]
	if choice=="geometric":
		g = 1
		f = 1
		for i in range(1, order + 1):
			g = g * (x - i)
			f = f * (value[i][0] ** (g / math.factorial(i)))
		f = f * value[0][0]
	h = expand(f)
	return h
