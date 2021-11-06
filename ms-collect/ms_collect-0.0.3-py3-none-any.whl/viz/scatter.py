from typing import List
import matplotlib.pyplot as plt

class Scatter:
	def __init__(self) -> None:
		pass

	def plot(self) -> None:
		pass


class Scatter3D:
	def __init__(self, 
		x: List[float], 
		y: List[float], 
		z: List[float],
		) -> None:
		"""
		Constructor for Scatter3D. Basically serves as a wrapper for
		matplotlib's 3d scatter plot projection.

		Args:
			x (List[float]): Data that will be plotted with respect to the x-axis
			y (List[float]): Data that will be plotted with respect to the y-axis
			z (List[float]): Data that will be plotted with respect to the z-axis
		"""
		self.x = x
		self.y = y
		self.z = z

	def plot(self) -> None:
		"""
		Renders the 3D scatter plot projection.
		"""
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')

		ax.scatter(self.x, self.y, self.z, c=self.z)

		ax.set_xlabel('m/z')
		ax.set_ylabel('Retention Time')
		ax.set_zlabel('Signal Intensity')
		plt.show()
		