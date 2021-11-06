from typing import List, Tuple

class Scope:
	def __init__(self, range: List[float] = None):
		"""Constructor for Scope Object

		Args:
			range (List[float], optional): Range to be converted into scope. Must be in the format: [minmz, maxmz, minrt, maxrt]. Defaults to None.
		"""
		self.min_mz, self.max_mz, self.min_rt, self.max_rt = self.config_mins_maxes(range)
	
	def config_mins_maxes(self, range: List[float] = None) -> Tuple[float]:
		"""[summary]

		Args:
			range (List[float], optional): [description]. Defaults to None.

		Returns:
			Tuple[float]: [description]
		"""
		if range is None:
			return 0.0, 0.0, 0.0, 0.0
		
		return range[0], range[1], range[2], range[3]
	
	def as_string(self) -> str:
		"""[summary]

		Returns:
			str: [description]
		"""
		return f"mz_{self.min_mz}_{self.max_mz}_rt_{self.min_rt}_{self.max_rt}"