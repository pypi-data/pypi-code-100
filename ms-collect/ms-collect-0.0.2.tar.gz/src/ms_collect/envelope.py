from typing import List
from .collection import Collection
from .scope import Scope
from .trace import Trace
from .point import Point

class Envelope(Collection):
	def __init__(self, scope: Scope = None, points: List[Point] = [], traces: List[Trace] = []) -> None:
		"""
		Constructor for an Envelope. Represents a collection of points and traces where
		traces are also theoretically collections of points.

		In Mass Spectrometry (specifically ms 1), an Envelope is commonly referred to as a ms 1 feature.
		Where this feature signifies that some sort of compound is reacting in the sample. Based off of this feature's
		data, one can build isotopic patterns, retrieve the monoisotopic peak, and so on.

		Args:
			scope (Scope, optional): The m/z and Retention time bounds of this envelope. See Scope class for more information. Defaults to None.
			points (List[Point], optional): List of MS Points. See Point class for more information. Defaults to [].
			traces (List[Trace], optional): List of Traces associated with this envelope. See Trace class for more information. Defaults to [].
		"""
		super().__init__(scope=scope, points=points)
		self.traces = traces
	
	def add_traces(self, traces: List[Trace]) -> None:
		"""
		Add traces to this envelope's current list of traces.

		Args:
			traces (List[Trace]): The traces to add.
		"""
		for trace in traces:
			self.traces.append(trace)

	def charge_state(self) -> int:
		"""
		Computes the charge state from this envelope's current set of traces.

		Returns:
			int: The value representing the charge state of this envelope.
		"""
		pass

	def monoisotopic_peak(self) -> Point:
		"""
		Determines the monoisotopic peak from this envelope's current set of traces.

		Returns:
			Point: A Point instance representing this envelope's monoisotopic peak
		"""
		pass