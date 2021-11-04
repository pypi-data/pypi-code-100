from typing import List
from .collection import Collection
from .scope import Scope
from .trace import Trace
from .point import Point

class Envelope(Collection):
	def __init__(self, scope: Scope = None, points: List[Point] = [], traces: List[Trace] = []) -> None:
		"""[summary]

		Args:
			scope (Scope, optional): [description]. Defaults to None.
			points (List[Point], optional): [description]. Defaults to [].
			traces (List[Trace], optional): [description]. Defaults to [].
		"""
		super().__init__(scope=scope, points=points)
		self.traces = traces
	
	def charge_state(self) -> int:
		"""[summary]

		Returns:
			int: [description]
		"""
		pass

	def monoisotopic_peak(self) -> Point:
		"""[summary]

		Returns:
			Point: [description]
		"""
		pass