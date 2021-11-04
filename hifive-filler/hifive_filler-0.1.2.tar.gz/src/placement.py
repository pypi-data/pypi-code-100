def find_possible_placements(field, token):
	possibilities = []
	i = 0
	j = 0
	# bounds check implicit through trimmed token
	while token.col_count+i <= field.col_count:
		while token.row_count+j <= field.row_count:
			if is_possible_placements((i,j), field, token):
				possibilities.append((i,j))
			++j
		++i
	return possibilities

def is_possible_placements(placement, field, token):
	opponent = has_no_opponent_overlap(placement, field, token)
	player = has_exactly_one_player_overlap(placement, field, token)
	return (opponent and player)

def has_no_opponent_overlap(placement, field, token):
	return (get_overlap_count(placement, field.opponent, token) == 0)

def has_exactly_one_player_overlap(placement, field, token):
	return (get_overlap_count(placement, field.player, token) == 1)

def get_overlap_count(placement, shape, token):
	overlap_count = 0
	for token_y in token.content:
		for token_x in token.content[token_y]:
			if shape[token_y+placement[0]][token_x+placement[1]]:
				++overlap_count
	return overlap_count
	