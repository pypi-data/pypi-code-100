import hifive_filler.shape as shape

class Token:
	def __init__(self):
		self.row_count = 0
		self.column_count = 0
		self.shape = shape.Shape()
	
	def update_dimensions(self, row_count, column_count):
		self.row_count = row_count
		self.column_count = column_count
		self.shape.update_dimensions(row_count, column_count)
	
	def reset_values(self):
		y = 0
		while y < len(self.shape.content):
			x = 0
			while x < len(self.shape.content[y]):
				self.shape.content[y][x] = False
				x += 1
			y += 1
	
	def trim(self):
		(max_row, max_col) = self.shape.get_max_dims()
		self.update_dimensions(max_row, max_col)
