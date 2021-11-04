import field
import parse
import token
import placement

def parse_field(player_number, field):
	(row_count, column_count) = parse.parse_field_meta(input())
	field.update_dimensions(row_count, column_count)
	_ = input() # drop column number row
	for row_index in range(0,field.row_count):
		row_as_string = parse.split_field_input_line(input())[1]
		(_, player_one, player_two) = parse.parse_field_line(row_as_string, row_index)
		if player_number == 1:
			field.player.update_content(player_one)
			field.opponent.update_content(player_two)
		else:
			field.player.update_content(player_two)
			field.opponent.update_content(player_one)

def parse_token(token):
	(row_count, column_count) = parse.parse_field_meta(input())
	token.update_dimensions(row_count, column_count)
	for row_index in range(0,token.row_count):
		(token_res, _, _) = parse.parse_field_line(input(), row_index)
		token.content.update_content(token_res)
	token.trim()

def parse_input(player_number, field, token):
	parse_field(player_number, field)
	return parse_token(token)

def place_token(field, token):
	possibilites = placement.find_possible_placements(field, token)
	could_place = (len(possibilites) > 0)
	return (could_place, possibilites[0][0], possibilites[0][1])

def main() -> None:
	try:
		player_number = parse.parse_player(input())[0]
		field = field.Field()
		token = token.Token()
		could_place = True
		
		while could_place:
			parse_input(player_number, field, token)
			(could_place, x, y) = place_token(field, token)
			if could_place:
				print(x, y)
	except Exception as e:
		print(e)
		exit(1)

if __name__ == "__main__":
	main()
