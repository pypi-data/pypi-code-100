class Shape:
	def __init__(self):
		self.content = []
	
	def update_dimensions(self, row_count, column_count):
		self.add_dimensions(row_count, column_count)
		self.drop_dimensions(row_count, column_count)
	
	def add_dimensions(self, row_count, column_count):
		while len(self.content) < row_count:
			self.content.append([])
		for row_index in range(0,row_count):
			while len(self.content[row_index]) < column_count:
				self.content[row_index].append(False)
	
	def drop_dimensions(self, row_count, column_count):
		while row_count < len(self.content):
			self.content.pop()
		for row_index in range(0,row_count):
			while column_count < len(self.content[row_index]):
				self.content[row_index].pop()
	
	def update_content(self, coordinate_list):
		i = 0
		while i < len(coordinate_list):
			self.content[coordinate_list[i][0]][coordinate_list[i][1]] = True
			i += 1
	
	def get_max_dims(self):
		i = 0
		j = 0
		max_i = 0
		max_j = 0
		print('token shape y length', len(self.content))
		while i < len(self.content):
			print('token shape x length', len(self.content[i]))
			while j < len(self.content[i]):
				if self.content[i][j]:
					if i > max_i:
						max_i = i
					if j > max_j:
						max_j = j
				j += 1
			i += 1
		return (max_i+1, max_j+1)
