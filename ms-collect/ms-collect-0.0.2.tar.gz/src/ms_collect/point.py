from typing import List
import uuid

class Point:
	def __init__(self, mz: float = 0.0, rt: float = 0.0, intensity: float = 0.0) -> None:
		"""
		Constructor for the point class. Represents a single Mass Spec raw data point.
		Has primary attributes m/z, retention time, and intensity.

		Args:
			mz (float, optional): [description]. Defaults to 0.0.
			rt (float, optional): [description]. Defaults to 0.0.
			intensity (float, optional): [description]. Defaults to 0.0.
		"""
		self.id = uuid.uuid4()
		self.mz = float(mz)
		self.rt = float(rt)
		self.intensity = float(intensity)

	def to_list(self, attributes: List[str] = ['mz', 'rt', 'intensity']) -> List[float]:
		"""
		Converts this point's current attributes to a list. This is especially
		helpful in porting to other utilities that primarily interface with ndarrays or
		things of a kind.
		
		Args:
			attributes (List[str], optional): The attributes you wish to see in the converted list. Defaults to ['mz', 'rt', 'intensity'].

		Returns:
			List[float]: The Point's attributes as a list.
		"""
		point_as_list = []
		if 'mz' in attributes: point_as_list.append(self.mz)
		if 'rt' in attributes: point_as_list.append(self.rt)
		if 'intensity' in attributes: point_as_list.append(self.intensity)

		return point_as_list
	
	def as_string(self) -> str:
		"""
		Returns a string representing the information of the point.
		Particularly useful for debugging purposes.

		Returns:
			str: The Points information as a string.
		"""
		return f"id: {self.id}, mz: {self.mz}, rt: {self.rt}, int: {self.intensity}"