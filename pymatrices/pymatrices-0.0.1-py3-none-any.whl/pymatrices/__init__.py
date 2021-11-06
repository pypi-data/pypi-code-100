class matrix:
	"""Creates a Matrix using a 2-D list"""

	def __init__(self, matrix):
		self.__rows = len(matrix)
		self.__cols = len(matrix[0])

		for rows in matrix:
			if len(rows) != self.__cols:
				raise TypeError("Invalid Matrix")

		if not isinstance(matrix, list):
			tempMat = list(matrix)
		else:
			tempMat = matrix

		for i in range(len(matrix)):
			if not isinstance(matrix[i], list):
				tempMat[i] = list(matrix[i])

		self.__mat = tempMat

	@property
	def matrix(self):
		return self.__mat

	@property
	def order(self):
		return (self.__rows, self.__cols)

	@property
	def transpose(self):
		order, res = self.order, []

		for i in range(order[1]):
			temp = []

			for j in range(order[0]):
				temp.append(self.matrix[j][i])

			res.append(temp)

		return matrix(res)

	@property
	def primaryDiagonalValues(self):
		res = []

		for i in range(len(self.matrix)):
			for j in range(len(self.matrix[i])):
				if i == j:
					res.append(self.matrix[i][j])

		return res

	@property
	def secondaryDiagonalValues(self):
		order, res = self.order, []

		for i in range(len(self.matrix)):
			for j in range(len(self.matrix[i])):
				if i+j == (order[0]-1):
					res.append(self.matrix[i][j])

		return res

	def __repr__(self):
		neg, minLen, res = False, len(f"{self.matrix[0][0]}"), ""

		for row in self.matrix:
			for val in row:
				if len(f"{val}") > minLen:
					minLen = len(f"{val}")

		for row in self.matrix:
			for val in row:
				strVal = f"{val}"
				res += " "*(minLen-len(strVal)) + strVal + " "
			res += "\n"

		return res

	def __add__(self, other):
		if isinstance(other, matrix):
			if self.order == other.order:
				res, temp = [], []
				row, col = self.order

				for i in range(row):
					for j in range(col):
						sum_elem = self.matrix[i][j] + other.matrix[i][j]
						temp.append(sum_elem)

					res.append(temp)
					temp = []

				return matrix(res)
			else:
				raise ValueError("Order of the Matrices must be same")
		else:
			raise TypeError(f"can only add matrix (not '{type(other).__name__}') to matrix")

	def __sub__(self, other):
		if isinstance(other, matrix):
			if self.order == other.order:
				res, temp = [], []
				row, col = self.order

				for i in range(row):
					for j in range(col):
						sum_elem = self.matrix[i][j] - other.matrix[i][j]
						temp.append(sum_elem)

					res.append(temp)
					temp = []

				return matrix(res)
			else:
				raise ValueError("Order of the Matrices must be same")
		else:
			raise TypeError(f"can only subtract matrix (not '{type(other).__name__}') from matrix")

	def __mul__(self, other):
		assert isinstance(other, (matrix, int, float)), f"Can only multiply either matrix or int or float (not {type(other).__name__}) with matrix"

		if isinstance(other, matrix):
			sOrder, oOrder = self.order, other.order
			if sOrder[1] == oOrder[0]:
				res = []
				T_other = other.transpose
				tOrder = T_other.order

				for i in range(sOrder[0]):
					temp = []

					for j in range(tOrder[0]):
						sum_val = 0

						for k in range(tOrder[1]):
							sum_val += (self.matrix[i][k] * T_other.matrix[j][k])

						temp.append(sum_val)
					res.append(temp)
			else:
				raise ValueError("Matrices can't be multiplied.")
		elif isinstance(other, (int, float)):
			order, res = self.order, []

			for row in range(order[0]):
				temp = []

				for col in range(order[1]):
					temp.append(self.matrix[row][col]*other)

				res.append(temp)

		return matrix(res)

	def __truediv__(self, other):
		if isinstance(other, (int, float)):
			order, res = self.order, []

			for row in range(order[0]):
				temp = []

				for col in range(order[1]):
					temp.append(self.matrix[row][col]/other)

				res.append(temp)
			return matrix(res)
		else:
			raise ValueError("Matrix can only be divided by a number")

	def __eq__(self, other):
		if isinstance(other, matrix):
			sOrder = self.order

			if sOrder == other.order:
				for row in range(sOrder[0]):
					for col in range(sOrder[1]):
						if self.matrix[row][col] != other.matrix[row][col]:
							return False
				else:
					return True
			else:
				return False
		else:
			return False

	def __neg__(self):
		order, res = self.order, []

		for row in range(order[0]):
			temp = []

			for col in range(order[1]):
				temp.append(-self.matrix[row][col])

			res.append(temp)
		return matrix(res)

	def positionOf(self, value):
		row, col = self.order

		for i in range(row):
			for j in range(col):
				if self.matrix[i][j] == value:
					return (i+1, j+1)
		else:
			raise ValueError(f"There is no Element as {value} in the Matrix.")

	def minorOfValueAt(self, row, column):
		row -= 1; column -= 1

		mat = [self.matrix[i] for i in range(len(self.matrix)) if i != row]

		res = [[i[j] for j in range(len(i)) if j!=column] for i in mat]

		return matrix(res)

	def valueAt(self, row, column):
		return self.matrix[row-1][column-1]

def adjoint(matrix1):
	"""Returns the adjoint of matrix"""

	order, mat = matrix1.order, matrix1.matrix

	if order[0] == 2:
		return matrix([[mat[1][1], -mat[0][1]], [-mat[1][0], mat[0][0]]])
	else:
		res = [[((-1)**(i+j+2))*(mat[i][j])*(determinant(matrix1.minorOfValueAt(i+1, j+1))) for j in range(order[1])] for i in range(order[0])]

		return matrix(res)

def createByFilling(value, order):
	"""Creates a Matrix of order by Filling it with value"""

	rows, cols = order[0], order[1]
	res = [[value for __ in range(cols)] for _ in range(rows)]

	return matrix(res)

def createColumnMatrix(values):
	"""Creates a Column Matrix with values"""

	return matrix([[i] for i in values])

def createRowMatrix(values):
	"""Creates a Row Matrix with values"""

	return matrix([[i for i in values]])

def determinant(matrix):
	"""Returns the determinant of matrix"""

	order = matrix.order

	if order[0] == order[1]:
		mat = matrix.matrix

		if order[0] == 1:
			return mat[0][0]
		elif order[0] == 2:
			return (mat[1][1]*mat[0][0]) - (mat[1][0]*mat[0][1])
		else:
			M11 = mat[0][0]*(determinant(matrix.minorOfValueAt(1, 1)))
			M12 = mat[0][1]*(determinant(matrix.minorOfValueAt(1, 2)))
			M13 = mat[0][2]*(determinant(matrix.minorOfValueAt(1, 3)))

			return M11 + M12 + M13
	else:
		raise ValueError(f"can only find the determinant of square matrix, not '{order[0]}x{order[1]}' matrix.")

def eigenvalues(matrix):
	order = matrix.order
	S1 = sum(matrix.primaryDiagonalValues)

	assert order[0] in (1, 2, 3), "Maximum Order is 3x3"

	if order[0] == 2:
		S2 = determinant(matrix)

		a, b, c = (1, -S1, S2)

		disc = (b**2-4*a*c)**0.5

		return ((-b+disc)/2*a, (-b-disc)/2*a)
	elif order[0] == 3:
		S2 = determinant(matrix.minorOfValueAt(1, 1))+determinant(matrix.minorOfValueAt(2, 2))+determinant(matrix.minorOfValueAt(3, 3))
		S3 = determinant(matrix)

		a, b, c, d = 1, -S1, S2, -S3

		d0 = b**2 - 3*a*c
		d1 = 2*b**3 - 9*a*b*c + 27*(a**2)*d
		sqrt = (d1**2 - 4*(d0**3))**0.5

		c1 = ((d1+sqrt)/2)**0.33

		croot = (-1+3j)/2

		try:
			r1 = (-1/(3*a))*(b+c1+(d0/c1))
			r2 = (-1/(3*a))*(b+croot*c1+(d0/croot*c1))
			r3 = (-1/(3*a))*(b+(croot**2)*c1+(d0/(croot**2)*c1))

			return (r1, r2, r3)
		except ZeroDivisionError:
			return ((-b/(3*a)),)*3

def inverse(matrix):
	"""Returns the inverse of matrix"""

	det = determinant(matrix)

	if det != 0:
		return adjoint(matrix)/det
	else:
		raise TypeError("Matrix is Singular.")

def isDiagonal(matrix):
	"""Returns True if matrix is 'Diagonal Matrix' else Returns False"""

	order, mat = matrix.order, matrix.matrix

	for row in range(order[0]):
		for col in range(order[1]):
			if row != col:
				if mat[row][col] != 0:
					return False
	else:
		return True

def isOrthogonal(matrix):
	"""Returns True if matrix is 'Orthogonal Matrix' else Returns False"""

	return True if matrix*matrix.transpose == 0 else False

def isScalar(matrix):
	"""Returns True if matrix is 'Scalar Matrix' else Returns False"""

	if isDiagonal(matrix):
		order, val, mat = matrix.order, matrix.matrix[0][0], matrix.matrix

		for row in range(order[0]):
			for col in range(order[1]):
				if row == col:
					if mat[row][col] != val:
						return False
		else:
			return True
	else:
		return False

def isSingular(matrix):
	"""Returns True if matrix is 'Singular Matrix' else Returns False"""

	return True if determinant(matrix) == 0 else False

def isSquare(matrix):
	"""Returns True if matrix is 'Square Matrix' else Returns False"""
	order = matrix.order

	return True if order[0] == order[1] else False

def isSymmetric(matrix):
	"""Returns True if matrix is 'Symmetric Matrix' else Returns False"""

	return True if matrix == matrix.transpose else False

def isSkewSymmetric(matrix):
	"""Returns True if matrix is 'Skew Symmetric Matrix' else Returns False"""

	return True if matrix == -matrix.transpose else False

def isIdentity(matrix):
	"""Returns True if matrix is 'Identity Matrix' else Returns False"""

	return True if matrix == I(matrix.order[0]) else False

def I(order):
	"""Returns the Identity Matrix of the given order"""

	assert isinstance(order, int), f"order must be 'int' but got '{type(order).__name__}'"

	res = [[0 for _ in range(order)] for __ in range(order)]

	for i in range(order):
		for j in range(order):
			if i==j:
				res[i][j] = 1

	return matrix(res)