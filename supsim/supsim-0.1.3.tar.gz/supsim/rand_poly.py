import numpy as np

# random polynomial generator of a given degree and variable count
# developed by Hamid Fadishei, fadishei@yahoo.com


class Poly:

	def __init__(self, poly):
		self.poly = poly
		self.degree = poly.shape[0]-1
		self.vars = poly.shape[1]

	def eval(self, x):
		s = 0;
		for i in range(self.degree+1):
			for j in range(self.vars):
				s += self.poly[i,j]*(x[j]**i)
		return s

	def eval_all(self, xs):
		s = np.zeros(xs.shape[0])
		for i in range(len(s)):
			s[i] = self.eval(xs[i,:])
		return s
		
	def is_linear(self):
		return self.poly[2:,:].sum()==0
		
	# whether all variables exist in relation
	def is_complete(self):
		for j in range(self.vars):
			if self.poly[1:,j].sum()==0:
				return False
		return True
	
	def max_power(self):
		for i in range(self.degree, -1, -1):
			if self.poly[i,:].sum()!=0:
				return i
		return 0

	def min_power(self):
		for i in range(self.degree+1):
			if self.poly[i,:].sum()!=0:
				return i
		return self.degree
		
	def val_str(self, val):
		return f'{val:.3f}' if val<0 else f'+{val:.3f}'

	def term_str(self, coef, var, power):
		if coef==0:
			return ''
		s = self.val_str(coef)
		if power>0:
			s += f'*x{var+1}'
			if power>1:
				s += f'^{power}'
		return s

	def var_str(self, i):
		return f'x{i+1}'

	def __str__(self):
		p = ''
		p += self.val_str(self.poly[0,:].sum())
		if self.degree>0:
			for i in range(1, self.degree+1):
				for j in range(self.vars):
					p += self.term_str(self.poly[i,j], j, i)
		return p


class RandPoly(Poly):

	def __init__(self, degree, vars, min_coef, max_coef):
		self.min_coef = min_coef
		self.max_coef = max_coef
		poly = np.random.uniform(min_coef, max_coef, size=(degree+1, vars))
		super().__init__(poly)

