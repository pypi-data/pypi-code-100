from typing import List
import uuid

class Point:
	def __init__(self, mz: float = 0.0, rt: float = 0.0, intensity: float = 0.0) -> None:
		"""[summary]

		Args:
			mz (float, optional): [description]. Defaults to 0.0.
			rt (float, optional): [description]. Defaults to 0.0.
			intensity (float, optional): [description]. Defaults to 0.0.
		"""
		self.id = uuid.uuid4()
		self.mz = mz
		self.rt = rt
		self.intensity = intensity

	def to_list(self, attributes: List[str] = ['mz', 'rt', 'intensity']) -> List[float]:
		"""[summary]

		Args:
			attributes (List[str], optional): [description]. Defaults to ['mz', 'rt', 'intensity'].

		Returns:
			List[float]: [description]
		"""
		point_as_list = []
		if 'mz' in attributes: point_as_list.append(self.mz)
		if 'rt' in attributes: point_as_list.append(self.rt)
		if 'intensity' in attributes: point_as_list.append(self.intensity)

		return point_as_list
	
	def as_string(self) -> str:
		"""[summary]

		Returns:
			str: [description]
		"""
		return f"id: {self.id}, mz: {self.mz}, rt: {self.rt}, int: {self.intensity}"