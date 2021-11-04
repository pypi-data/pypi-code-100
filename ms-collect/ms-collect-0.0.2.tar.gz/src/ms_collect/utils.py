from typing import List, Tuple

from .point import Point

class Utils:
	def __init__(self) -> None:
		pass

	@staticmethod
	def to_mspoints(
		rawpoints: List[Tuple[float]] = [], 
		sort_by_intensity_asc: bool = False, 
		sort_by_intensity_desc: bool = False
		) -> List[Point]:
		"""[summary]

		Args:
			rawpoints (List[Tuple[float]], optional): [description]. Defaults to [].
			sort_by_intensity_asc (bool, optional): [description]. Defaults to False.
			sort_by_intensity_desc (bool, optional): [description]. Defaults to False.

		Returns:
			List[Point]: [description]
		"""

		# TODO: We could have a better sorting/ordering system here 

		points = []
		for pt in rawpoints:
			converted = Point(mz=pt[0], rt=pt[1], intensity=pt[2])
			points.append(converted)
		
		if sort_by_intensity_asc: return sorted(points, key=lambda pt: pt.intensity)
		if sort_by_intensity_desc: return sorted(points, key=lambda pt: pt.intensity, reverse=True)
		
		return points

	@staticmethod
	def to_ndarray(points: List[Point], attributes_to_include: List[str] =  ['mz', 'rt', 'intensity']) -> List[List[float]]:
		"""[summary]

		Args:
			points (List[Point], optional): [description]. Defaults to [].
			attributes_to_include (List[str], optional): [description]. Defaults to ['mz', 'rt', 'intensity'].

		Returns:
			List[List[float]]: [description]
		"""
		ndarray = []
		for pt in points:
			pt_as_list = pt.to_list(attributes=attributes_to_include)
			ndarray.append(pt_as_list)
		
		return ndarray
