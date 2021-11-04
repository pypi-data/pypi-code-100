from typing import List

from .collection import Collection
from .scope import Scope
from .point import Point

class Trace(Collection):
	def __init__(self, scope: Scope = None, points: List[Point] = []) -> None:
		"""
		Constructor for a trace. Represents an isotopic trace which theoretically,
		is just a collection of ms1 raw points.

		Args:
			scope (Scope, optional): The m/z and Retention Time bounds. See Scope class for more information. Defaults to None.
			points (List[Point], optional): List of points associated with this trace. See Point class for more information,. Defaults to [].
		"""
		super().__init__(scope=scope, points=points)
	
	def peak(self) -> Point:
		"""
		Determines the peak of this isotopic trace.

		Returns:
			Point: Point instance representing the peak of this trace.
		"""
		return self.most_intense_point()
