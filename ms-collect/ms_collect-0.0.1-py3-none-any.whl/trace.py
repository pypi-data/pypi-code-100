from typing import List

from .collection import Collection
from .scope import Scope
from .point import Point

class Trace(Collection):
	def __init__(self, scope: Scope = None, points: List[Point] = []) -> None:
		"""[summary]

		Args:
			scope (Scope, optional): [description]. Defaults to None.
			points (List[Point], optional): [description]. Defaults to [].
		"""
		super().__init__(scope=scope, points=points)
	
	def peak(self) -> Point:
		"""[summary]

		Returns:
			Point: [description]
		"""
		pass
