from vinca.lib import ansi
import shutil

COLUMNS, LINES = shutil.get_terminal_size()

# A Context Manager for the terminal's alternate screen
class AlternateScreen:
	def __enter__(self):
		ansi.save_cursor()
		ansi.hide_cursor()
		ansi.save_screen()
		ansi.clear()
		ansi.move_to_top()

	def __exit__(self, *exception_args):
		ansi.restore_screen()
		ansi.restore_cursor()


class NoCursor:
	def __enter__(self):
		ansi.hide_cursor()

	def __exit__(self, *exception_args):
		ansi.show_cursor()
		

class LineWrapOff:
	def __enter__(self):
		ansi.line_wrap_off()

	def __exit__(self, *exception_args):
		ansi.line_wrap_on()

def count_screen_lines(text):
	text = ansi.strip_ansi(text)
	lines = text.splitlines()
	lines = [l.split('\r')[-1] for l in lines] # carriage return overwrites the line so we only want the text after the last carriage return on the line
	lines = [len(l) // COLUMNS for l in lines]
	return sum(lines)
