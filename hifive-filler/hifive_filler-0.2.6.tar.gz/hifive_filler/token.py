import hifive_filler.shape

class Token:
	def __init__(self):
		self.row_count = 0
		self.column_count = 0
		self.shape = shape.Shape()
	
	def update_dimensions(self, row_count, column_count):
		self.row_count = row_count
		self.column_count = column_count
		self.shape.update_dimensions(row_count, column_count)
	
	def trim(self):
		(max_row, max_col) = self.shape.get_max_dims()
		self.shape.update_dimensions(max_row, max_col)
