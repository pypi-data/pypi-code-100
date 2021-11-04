import re
import hifive_filler.field as field

def parse_player(input):
	match = re.search(r"^\$\$\$ exec p(\d{1}) : \[([a-zA-Z]+)\]$", input)
	if not match:
		raise Exception('Player input string could not be parsed')
	if not match.group(1):
		raise Exception('Player number could not be parsed from player input')
	if not match.group(2):
		raise Exception('Player name could not be parsed from player input')
	return (int(match.group(1)), match.group(2))

def parse_field_meta(input):
	match = re.search(r"[Plateau|Piece] (\d+) (\d+):", input)
	if not match:
		raise Exception('Field input string could not be parsed')
	if not match.group(1):
		raise Exception('Field row count could not be parsed from meta input')
	if not match.group(2):
		raise Exception('Field column count could not be parsed from meta input')
	return (int(match.group(1)), int(match.group(2)))

def split_field_input_line(input):
	match = re.search(r"(\d{3}) (.+)", input)
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
		## Python has no siwtch statements until 3.10
		if line[col_index] == ".":
			pass
		elif line[col_index] == "*":
			token.append((row_index, col_index))
		elif line[col_index] == "O":
			player_one.append((row_index, col_index))
		elif line[col_index] == "o":
			player_one.append((row_index, col_index))
		elif line[col_index] == "X":
			player_two.append((row_index, col_index))
		elif line[col_index] == "x":
			player_two.append((row_index, col_index))
		else:
			raise Exception('Cell contains invalid character')
		col_index += 1
	return ((token, player_one, player_two))
