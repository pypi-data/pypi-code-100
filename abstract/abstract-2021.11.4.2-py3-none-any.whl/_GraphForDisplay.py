from ._GraphWithoutDisplay import GraphWithoutDisplay


class Graph(GraphWithoutDisplay):
	def get_svg(self, direction=None, pad=None, **kwargs):
		"""
		:type direction: NoneType or str
		:type pad: NoneType or int or float
		:rtype: str
		"""
		return self.render(direction=direction or self._direction, pad=pad, **kwargs)._repr_svg_()

	def _repr_html_(self):
		return self.get_svg()

	def get_html(self, direction=None, pad=None, **kwargs):
		from IPython.core.display import HTML
		return HTML(self.get_svg(direction=direction or self._direction, pad=pad, **kwargs))

	"""
	def display(self, p=None, pad=0.2, direction=None, path=None, height=None, width=None, dpi=300):
		try:
			from IPython.core.display import display
			to_display = self.render(
				pad=pad, dpi=dpi, direction=direction or self._direction, path=path, height=height, width=width
			)
			display(to_display)
		except ImportError:
			if p is not None:
				p.pretty(self.get_tree_str())
			else:
				print(self.get_tree_str())

	def _repr_pretty_(self, p, cycle):
		if cycle:
			p.text('Graph')
		else:
			self.display(p=p)
	"""