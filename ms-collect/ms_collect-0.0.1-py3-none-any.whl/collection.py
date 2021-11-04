from typing import List, Tuple
from functools import reduce
import uuid

from .scope import Scope
from .point import Point
from .math import ConvexHull
from .utils import Utils

class Collection:
	def __init__(self, id: int = None, scope: Scope = None, points: List[Point] = []) -> None:
		"""
		The constructor of the Collection class. Provides the ability to group together
		raw Mass Spec data points and have easy to access useful operations on
		this group of data points.

		Args:
			id (int, optional): Provide an id for the collection or the collection will generate one. Defaults to None.
			scope (Scope, optional): The m/z and RT limits of the collection, See Scope class for more details. Defaults to None.
			points (List, optional): A list of Point objects. Defaults to [].
		"""
		self.id = id if id is not None else uuid.uuid4()
		self.scope = scope if scope is not None else Scope()
		self.points = points
	
	def avg_mz(self) -> float:
		"""
		Computes the average m/z value from this collection's current list of points.

		Returns:
			float: The average m/z value
		"""
		return reduce(lambda pt_a, pt_b: pt_a.mz + pt_b.mz, self.points) / len(self.points)
	
	def avg_rt(self) -> float:
		"""
		Computes the average Retention Time value from this collection's current list of points.n.

		Returns:
			float: The average Retention Time value.
		"""
		return reduce(lambda pt_a, pt_b: pt_a.rt + pt_b.rt, self.points) / len(self.points)
	
	def avg_intensity(self) -> float:
		"""
		Computes the average Intensity value from this collection's current list of points.

		Returns:
			float: The average Intensity value.
		"""
		return reduce(lambda pt_a, pt_b: pt_a.intensity + pt_b.intensity, self.points) / len(self.points)

	def mz_bounds(self) -> Tuple[float]:
		"""
		Computes minimum and maximum m/z values from this collection's current list of points.

		Returns:
			Tuple[float]: The min and max m/z values e.g. [432.32, 455.43]
		"""
		if len(self.points) < 1:
			return 0, 0
		
		min_mz = self.points[0].mz
		max_mz = self.points[0].mz

		for p in self.points:
			if p.mz < min_mz: min_mz = p.mz
			if p.mz > max_mz: max_mz = p.mz

		return min_mz, max_mz

	def rt_bounds(self) -> Tuple[float]:
		"""
		Computes the minimum and maximum Retention Time values from this collection's current list of points.

		Returns:
			Tuple[float]: The min and max Retention Time values e.g. [1202.2090, 1394.3032]
		"""
		if len(self.points) < 1:
			return 0, 0
		
		min_rt = self.points[0].rt
		max_rt = self.points[0].rt

		for p in self.points:
			if p.rt < min_rt: min_rt = p.rt
			if p.rt > max_rt: max_rt = p.rt

		return min_rt, max_rt

	def add_points(self, points: List[Point]) -> None:
		"""
		Add a list of points to this collection's current list of points.

		Args:
			points (List[Point]): The list of points to add (must be instances of the Point Class).
		"""
		for pt in points:
			self.points.append(pt)

	def most_intense_point(self) -> Point:
		"""
		Computes the most intense point in this collection's current list of points.

		Returns:
			Point: The most intense point
		"""
		pass

	def cumulative_intensity(self) -> float:
		"""
		Computes the cumulative intensity from this collection's current list of points.

		Returns:
			float: [description]
		"""
		pass

	def convex_hull(self) -> ConvexHull:
		"""
		Builds a ConvexHull instance from this collection's current list of points.
		See ConvexHull class for more details.

		Returns:
			ConvexHull: an instance of the ConvexHull class
		"""
		points_as_ndarray = Utils.to_ndarray(attributes_to_include=['mz', 'rt'])
		return ConvexHull(points=points_as_ndarray)
