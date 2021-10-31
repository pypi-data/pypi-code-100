#TODO d2w not just 2dw
import re
import string

from vinca.lib import ansi
from vinca.lib import terminal
from vinca.lib.readkey import readkey, keys

# by making the line_history and the yank history module level variables
# they are preserved for the duration of the python session
# this is good enough for browsing and obviates the need of more complicated file reading
# if the user really needs to something like that they can begin an add session
# or they can just drag copy and paste


class VimEditor:
	line_history = []
	yank = ''
	MODES = ('normal','insert','motion_pending')
	OPERATORS = ['d','c','y','~','z']
	MOTIONS = ['w','e','b','f','t','F','T',';',',','h','l','(',')','0','$','_','^',keys.LEFT, keys.RIGHT]  # TODO capital letters
	ACTIONS = ['s','S','r','u','.','x','X','D','C','p','P','Y','a','i','A','I','j','k']
	BOW = re.compile(	# BEGINNING OF WORD
		'((?<=\s)|^)'	# pattern is preceded by whitespace or the beginning of the line
		'\w')		# the beginning of the word is any alphanumeric character.
	EOW = re.compile(	# END OF WORD
		'\w'		# any alphanumeric character
		'(\s|$)')	# succeeded by whitespace or the end of the line.
	EOS = re.compile('[.!?]')  # EDGE OF SENTENCE

	def __init__(self, text, mode, pos, completions):
		self.text = text
		self.mode = mode
		self.pos = pos
		self.completions = completions
		self.multiplier = 1
		self.undo_stack = self.redo_stack = []
		self.operator = None
		self.current_insertion = ''
		self.prev_insertion = ''
		self.prev_multiplier = 1
		self.prev_action = None
		self.prev_operation = None
		self.line_history_idx = 0
		self.search_char = ''
		# make the start and end of the selection part of state

	def process_key(self, key):
		if self.mode == 'insert':
			if key == keys.ESC:
				self.prev_insertion = self.current_insertion
				self.current_insertion = ''
				self.mode = 'normal'
			self.do_insert(key)
			return
		if key in string.digits:
			self.multiplier = int(key)
			return
		elif self.mode == 'normal':
			if key in self.ACTIONS:
				for _ in range(self.multiplier):
					self.do_action(key)
				self.reset_multiplier()
			if key in self.OPERATORS:
				self.mode = 'motion_pending'
				self.operator = key
			if key in self.MOTIONS:
				for _ in range(self.multiplier):
					self.do_motion(key)
				self.reset_multiplier()
		elif self.mode == 'motion_pending':
			motion = key
			for _ in range(self.multiplier):
				start = self.pos
				self.do_motion(motion)
				end = self.pos
				self.pos = start
				self.do_operation(self.operator, start, end)
			self.reset_multiplier()
			self.operator = None
			self.prev_action = self.prev_insertion = None
			self.prev_operation = (self.operator, motion)

	def reset_multiplier(self):
		self.prev_multiplier = self.multiplier
		self.multiplier = 1

	def idx(self, pattern, back = False):
		'''Return the index of the next match of the pattern in the text.
		If we find no match we return the current pos.'''
		indices = [m.start() for m in re.finditer(pattern, self.text)]  # list of matching indices
		if not back:
			return min([i for i in indices if i > self.pos], default = self.pos)
		if back:
			return max([i for i in indices if i < self.pos], default = self.pos)

	def do_insert(self, key):
		if key == '\t' and self.completions:
			raise NotImplementedError
		if key not in string.printable:
			if key in (keys.LEFT, keys.RIGHT):
				self.do_motion(key)
				self.current_insertion = ''
			elif key == keys.BACK:
				self.text = self.text[:self.pos - 1] + self.text[self.pos:]
				self.pos -= 1
				self.current_insertion = ''
			# TODO deletion in insert mode
			return
		self.text = self.text[:self.pos] + key + self.text[self.pos:]
		self.current_insertion += key
		self.pos += 1
		
		

	def do_operation(self, key, start, end):
		if key in ('d','c'):
			self.text = self.text[:start] + self.text[end+1:]
		if key == 'y':
			self.yank = self.text[start:end]
		if key == '~':
			self.text = self.text[:start] + self.text[start:end].swapcase() + self.text[end+1:]
		if key == 'z':
			self.yank = self.text[start:end]
			self.text = self.text[:start] + '_'*(end-start) + self.text[end+1:]
		self.mode = 'insert' if key =='c' else 'normal'

	def do_motion(self, key):
		# jump to character
		if key in ('f','F','t','T'):
			sc = self.search_char = readkey()
			self.pos = {'f': self.idx(sc),
				    'F': self.idx(sc, back = True),
				    't': self.idx(f'.(?={sc})'),
				    'T': self.idx(f'(?<={sc}).', back = True)}[key]
			return
		# other motions
		self.pos = {
			# jump by word
			'w': self.idx(self.BOW), 'e': self.idx(self.EOW), 'b': self.idx(self.BOW, back = True),
			# repeat character jumps
			';': self.idx(self.search_char), ',': self.idx(self.search_char, back = True),
			# left / right navigation
			'h': max(0, self.pos-1), keys.LEFT: max(0, self.pos-1),
			'l': min(len(self.text), self.pos+1), keys.RIGHT: min(len(self.text), self.pos+1),
			# sentence jumping
			')': self.idx(self.EOS), '(': self.idx(self.EOS, back = True),
			# jump to beginning or end of line
			'0': 0, '^': 0, '_': 0, '$': len(self.text)}[key]

	def do_action(self, key): 
		text, pos = self.text, self.pos
		k = key
		# substitution
		if k in ('s','S','C'):
			self.mode = 'insert'
			text = {'S': '', 's': text[:pos] + text[pos+1:], 'C': text[:pos]}[k]
		# reversion and redoing
		if k == 'u' and self.undo_stack:
			self.redo_stack.append({'text': text, 'pos': pos})  # save current state
			prev_state = self.undo_stack.pop() # retrieve previous state
			text, pos = prev_state['text'], prev_state['pos']
		if k == keys.CTRL_R and self.redo_stack:
			self.undo_stack.append({'text': text, 'pos': pos})
			new_state = self.redo_stack.pop()
			text, pos = new_state['text'], new_state['pos']
		if k == '.' and (self.prev_action or self.prev_operation):
			if self.prev_action:
				for _ in range(self.prev_multiplier):
					self.do_action(self.prev_action)
					if self.mode == 'insert':
						self.text = self.text[:self.pos] + self.prev_insertion + self.text[self.pos:]
					self.mode = 'normal'
			elif self.prev_operation:
				operator, motion = self.prev_operation
				for _ in range(self.prev_multiplier):
					self.do_operation(operator, motion)
		# deletion
		if k in ('x','X','D'):
			text = {'D': text[:pos],
				'x': text[:pos] + text[pos+1:],
				'X': text[:pos-1] + text[pos:]}[k]
			pos -= (k == 'X')
		# copy and paste
		if k == 'Y': self.yank = text[pos:]
		if k == 'p': text = text[:pos+1] + self.yank + text[pos+1:]
		if k == 'P': text = text[:pos] + self.yank + text[pos:]; pos += len(self.yank)
		# enter insert mode
		if k in ('i','I','a','A'):
			self.mode = 'insert'
			pos = 0 if k=='I' else pos+1 if k=='a' else len(text) if k=='A' else pos
		# history scrolling
		if k in ('j','k',keys.DOWN, keys.UP):
			self.line_history_idx -= 1 if k in ('k', keys.UP) else -1
			lhi = self.line_history_idx
			if lhi == 0: text = ''
			elif lhi <= -len(text): text = self.line_history[0]
			else: text = self.line_history[lhi]
		self.text, self.pos = text, pos
	

normal_prompt = f'{ansi.codes["red"]}[N]{ansi.codes["reset"]} '
insert_prompt = f'{ansi.codes["green"]}[I]{ansi.codes["reset"]} '

# TODO: refactor
# move the representation of the vim session into a display(self) method
# move the loop viz. "run" into a function which returns the text or self
def fancy_input(starting_mode = 'insert', multiline = False, prompt = '', text = '', completions = None):

	vim = VimEditor(text = text, mode = starting_mode, pos = 0, completions = completions)
	with terminal.NoCursor(), terminal.LineWrapOff():
		while True:
			text = vim.text
			pos = vim.pos
			prefix = (normal_prompt if vim.mode == 'normal' else insert_prompt) + prompt
			cursor = ansi.codes['reverse'] + (text[pos] if pos<len(text) else ' ') + ansi.codes['reset']
			end_buffer = ' '*terminal.COLUMNS
			print('\r', prefix, text[:pos], cursor, text[pos+1:], end_buffer, end='', sep='', flush=True)

			key = readkey()
			if key in ('\n','\r'):
				vim.line_history.append(vim.text)
				return vim.text
			else:
				vim.process_key(key)
