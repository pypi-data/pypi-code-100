from vinca.lib import ansi
from vinca.lib.terminal import COLUMNS
from vinca.lib.fancy_input import fancy_input

def edit(card):
	front_path = (card.path / 'front')
	back_path  = (card.path / 'back')
	front = front_path.read_text()
	back  =  back_path.read_text()

	# TODO multiline fancy_input using Alt+Enter
	new_front = fancy_input(text = front, prompt = 'Q: ')
	front_path.write_text(new_front)
	
	new_back = fancy_input(text = back, prompt = 'A: ')
	back_path.write_text(new_back)

