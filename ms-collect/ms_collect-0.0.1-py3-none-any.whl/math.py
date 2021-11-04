from typing import List

class ConvexHull:
	def __init__(self, points: List[float] = []) -> None:
		"""[summary]

		Args:
			points (List[float], optional): [description]. Defaults to [].
		"""
		# Sort the points lexicographically (tuples are compared lexicographically).
		# The 'set' here is for removal of duplicates to detect the case we have just one unique point.
		self.points = sorted(set(tuple(map(tuple, points))))
	
	def hull(self) -> List[float]:
		"""[summary]

		Returns:
			List[float]: [description]
		"""
		# Boring case: no points or a single point, possibly repeated multiple times.
		if len(self.points) <= 1:
			return self.points

		# 2D cross product of OA and OB vectors, i.e. z-component of their 3D cross product.
		# Returns a positive value, if OAB makes a counter-clockwise turn,
		# negative for clockwise turn, and zero if the points are collinear.
		def cross(o, a, b):
			return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

		# Build lower hull 
		lower = []
		for p in self.points:
			while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
				lower.pop()
			lower.append(p)

		# Build upper hull
		upper = []
		for p in reversed(self.points):
			while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
				upper.pop()
			upper.append(p)

		# Concatenation of the lower and upper hulls gives the convex hull.
		# Last point of each list is omitted because it is repeated at the beginning of the other list. 
		return lower[:-1] + upper[:-1]

