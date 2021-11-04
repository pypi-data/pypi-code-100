import shape

class Token:
	def __init__(self, row_count, column_count):
		self.row_count = 0
		self.column_count = 0
		self.content = shape.Shape()
	
	def update_dimensions(self, row_count, column_count):
		self.row_count = row_count
		self.column_count = column_count
		self.content.update_dimensions(row_count, column_count)
	
	def trim(self):
		max_col = self.content.get_max_set_col()
		max_row = self.content.get_max_set_row()
		self.content.update_dimensions(max_row, max_col)
