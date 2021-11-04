import re
import field.py

def parse_player(input):
	match = re.match(r"$$$ exec p(\d{1}) : [([a-zA-Z]+)]", input)
	if not match:
		raise Exception('Player input string could not be parsed')
	if not match.group(1):
		raise Exception('Player number could not be parsed from player input')
	if not match.group(2):
		raise Exception('Player name could not be parsed from player input')
	return (match.group(1), match.group(2))

def parse_field_meta(input):
	match = re.match(r"[Plateau|Piece] (\d+) (\d+):", input)
	if not match:
		raise Exception('Field input string could not be parsed')
	if not match.group(1):
		raise Exception('Field row count could not be parsed from meta input')
	if not match.group(2):
		raise Exception('Field column count could not be parsed from meta input')
	return (match.group(1), match.group(2))

def split_field_input_line(input):
	match = re.match(r"(\d+{3}) (.+)", input)
	if not match:
		raise Exception('Field row input string could not be parsed')
	if not match.group(1):
		raise Exception('Field row number could not be parsed from row input')
	if not match.group(2):
		raise Exception('Field row contents could not be parsed from row input')
	return (match.group(1), match.group(2))

def parse_field_line(line, row_index):
	col_index = 0
	player_one = []
	player_two = []
	token = []
	while col_index < len(line):
		char = line[col_index]
		match char:
			case field.Cell_State.EMPTY:
				# Nothing to do
			case field.Cell_State.TOKEN:
				token.append((row_index, col_index))
			case field.Cell_State.PLAYER_ONE_OLD:
				player_one.append((row_index, col_index))
			case field.Cell_State.PLAYER_ONE_NEW:
				player_one.append((row_index, col_index))
			case field.Cell_State.PLAYER_TWO_OLD:
				player_two.append((row_index, col_index))
			case field.Cell_State.PLAYER_TWO_NEW:
				player_two.append((row_index, col_index))
			case _:
				raise Exception('Cell contains invalid character')
		++col_index
	return ((token, player_one, player_two))