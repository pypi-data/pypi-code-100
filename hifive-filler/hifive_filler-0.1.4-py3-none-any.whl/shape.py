class Shape:
	def __init__(self):
		self.content = []
	
	def update_dimensions(self, row_count, column_count):
		for row_index in range(0,row_count):
			if not row_index < len(self.content):
				self.content[row_index] = []
			for col_index in range(0,column_count):
				if not col_index < len(self.content[row_index]):
					self.content[row_index][col_index] = False
		while row_count < len(self.content):
			self.content.pop()
	
	def update_content(self, coordinate_list):
		i = 0
		while i < len(coordinate_list):
			self.content[coordinate_list[i][0]][coordinate_list[i][1]] = True
			++i
	
	def get_max_set_col(self):
		i = 0
		j = 0
		max = 0
		while i < len(self.content):
			while j < len(self.content[i]):
				if self.content[i][j] and j  > max:
					max = j
		return max
	
	def get_max_set_row(self):
		i = 0
		j = 0
		max = 0
		while i < len(self.content):
			while j < len(self.content[i]):
				if self.content[i][j] and i  > max:
					max = i
		return max