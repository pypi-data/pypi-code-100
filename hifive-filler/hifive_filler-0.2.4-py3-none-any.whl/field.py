import shape

class Field:
	def __init__(self):
		self.row_count = 0
		self.column_count = 0
		self.player = shape.Shape()
		self.opponent = shape.Shape()
	
	def update_dimensions(self, row_count, column_count):
		self.row_count = row_count
		self.column_count = column_count
		self.player.update_dimensions(row_count, column_count)
		self.opponent.update_dimensions(row_count, column_count)
	
