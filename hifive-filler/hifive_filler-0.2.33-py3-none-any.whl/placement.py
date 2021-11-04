def find_possible_placements(field, token):
	possibilities = []
	x = 0
	# bounds check implicit through trimmed token
	while token.column_count+x <= field.column_count:
		y = 0
		while token.row_count+y <= field.row_count:
			print('possible', x,y)
			if is_possible_placements((x,y), field, token):
				possibilities.append((x,y))
			y += 1
		x += 1
	return possibilities

def is_possible_placements(placement, field, token):
	opponent = has_no_opponent_overlap(placement, field, token)
	player = has_exactly_one_player_overlap(placement, field, token)
	print('bools',opponent, player)
	return (opponent and player)

def has_no_opponent_overlap(placement, field, token):
	return (get_overlap_count(placement, field.opponent, token) == 0)

def has_exactly_one_player_overlap(placement, field, token):
	return (get_overlap_count(placement, field.player, token) == 1)

def get_overlap_count(placement, shape, token):
	overlap_count = 0
	x = 0
	y = 0
	while y < len(token.shape.content):
		while x < len(token.shape.content[y]):
			if token.shape.content[y][x] and shape.content[y+placement[1]][x+placement[0]]:
				overlap_count += 1
			x += 1
		y += 1
	return overlap_count
	